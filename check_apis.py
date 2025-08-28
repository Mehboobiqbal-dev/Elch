#!/usr/bin/env python3
"""
API Health Check script for the Elch FastAPI service.

Features:
- Auth flow: attempts login, falls back to signup, then login
- Exercises key endpoints with proper Authorization header
- Handles 429 Too Many Requests by backing off and retrying
- Summarizes results and returns non-zero exit code on failures

Usage:
  python check_apis.py --base-url http://127.0.0.1:8000 \
    --email test@example.com --password mypass

Environment variables (optional):
  BASE_URL, TEST_EMAIL, TEST_PASSWORD
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import json
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

import requests

DEFAULT_BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

@dataclass
class CheckResult:
    name: str
    ok: bool
    status: int
    detail: str = ""

class APIClient:
    def __init__(self, base_url: str, email: str, password: str, verbose: bool = False):
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.password = password
        self.verbose = verbose
        self.session = requests.Session()
        # Reasonable default timeouts
        self.timeout = 20

    def _log(self, msg: str):
        if self.verbose:
            print(msg)

    def _abs(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        if not path.startswith("/"):
            path = "/" + path
        return f"{self.base_url}{path}"

    def request_with_backoff(self, method: str, path: str, *, json_body: Optional[dict] = None,
                              expected: Optional[List[int]] = None, max_retries: int = 2,
                              backoff_seconds: float = 5.0) -> requests.Response:
        url = self._abs(path)
        expected = expected or [200]
        for attempt in range(max_retries + 1):
            try:
                resp = self.session.request(method.upper(), url, json=json_body, timeout=self.timeout)
            except requests.RequestException as e:
                if attempt == max_retries:
                    raise
                self._log(f"Network error on {method} {url}: {e}. Retrying in {backoff_seconds}s...")
                time.sleep(backoff_seconds)
                continue

            if resp.status_code == 429 and attempt < max_retries:
                retry_after = resp.headers.get("Retry-After")
                wait = float(retry_after) if retry_after and retry_after.isdigit() else backoff_seconds
                self._log(f"429 on {method} {url}. Backing off {wait}s then retrying...")
                time.sleep(wait)
                continue

            if resp.status_code not in expected and attempt < max_retries:
                self._log(f"Unexpected status {resp.status_code} for {method} {url}. Retrying in {backoff_seconds}s...")
                time.sleep(backoff_seconds)
                continue

            return resp

        return resp  # type: ignore

    def authenticate(self) -> Tuple[bool, str]:
        """Obtain JWT via /token, creating the user with /signup if necessary.
        Returns (ok, token_or_error).
        """
        # Try login
        token = self._login_for_token()
        if token:
            return True, token

        # Try signup
        self._log("Login failed, attempting signup...")
        signup_payload = {"email": self.email, "password": self.password, "name": "HealthCheck"}
        resp = self.request_with_backoff("POST", "/signup", json_body=signup_payload, expected=[200, 201, 400])
        if resp.status_code == 400:
            # Likely already registered; continue
            self._log("User already registered. Proceeding to login.")
        elif resp.status_code not in (200, 201):
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text
            return False, f"Signup failed: {resp.status_code} {detail}"

        # Login again
        token = self._login_for_token()
        if not token:
            return False, "Unable to obtain access token after signup"
        return True, token

    def _login_for_token(self) -> Optional[str]:
        # FastAPI OAuth2PasswordRequestForm expects form-encoded fields
        url = self._abs("/token")
        data = {"username": self.email, "password": self.password}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            resp = self.session.post(url, data=data, headers=headers, timeout=self.timeout)
        except requests.RequestException as e:
            self._log(f"Login error: {e}")
            return None
        if resp.status_code != 200:
            self._log(f"Login failed: {resp.status_code} {resp.text[:200]}")
            return None
        try:
            token = resp.json().get("access_token")
        except Exception:
            token = None
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        return token


def run_checks(client: APIClient) -> List[CheckResult]:
    results: List[CheckResult] = []

    def add_result(name: str, resp: requests.Response, ok: bool, detail: str = ""):
        try:
            status = resp.status_code
        except Exception:
            status = -1
        results.append(CheckResult(name=name, ok=ok, status=status, detail=detail))

    # 1) Root health
    resp = client.request_with_backoff("GET", "/", expected=[200])
    ok = resp.status_code == 200 and "healthy" in resp.text.lower()
    add_result("GET /", resp, ok, detail=resp.text[:200])

    # 2) /me (auth required)
    resp = client.request_with_backoff("GET", "/me", expected=[200])
    try:
        data = resp.json()
        ok = resp.status_code == 200 and isinstance(data, dict) and data.get("email") == client.email
    except Exception:
        ok = False
    add_result("GET /me", resp, ok, detail=str(resp.text)[:200])

    # 3) credentials list
    resp = client.request_with_backoff("GET", "/credentials", expected=[200])
    try:
        data = resp.json()
        ok = resp.status_code == 200 and isinstance(data, list)
    except Exception:
        ok = False
    add_result("GET /credentials", resp, ok, detail=str(resp.text)[:200])

    # 4) chat message
    resp = client.request_with_backoff("POST", "/chat/message", json_body={"message": "ping"}, expected=[200])
    try:
        data = resp.json()
        ok = resp.status_code == 200 and data.get("status") == "ok"
    except Exception:
        ok = False
    add_result("POST /chat/message", resp, ok, detail=str(resp.text)[:200])

    # 5) prompt (rate-limited 10/min): accept 200; if 429 after retries, mark soft-fail
    soft_fail = False
    resp = client.request_with_backoff("POST", "/prompt", json_body={"prompt": "Say hello"}, expected=[200, 429], max_retries=2, backoff_seconds=6)
    if resp.status_code == 200:
        ok = True
    elif resp.status_code == 429:
        ok = False
        soft_fail = True
    else:
        ok = False
    add_result("POST /prompt", resp, ok, detail=str(resp.text)[:200])

    # 6) tasks results (two routes exist)
    for name, path in [("GET /api/tasks/results", "/api/tasks/results"), ("GET /tasks/results", "/tasks/results")]:
        resp = client.request_with_backoff("GET", path, expected=[200, 404])
        # Allow 404 for older deployments missing one of the paths
        ok = resp.status_code in (200, 404)
        add_result(name, resp, ok, detail=str(resp.text)[:200])

    # 7) chat history
    resp = client.request_with_backoff("GET", "/chat/history", expected=[200])
    try:
        data = resp.json()
        ok = resp.status_code == 200 and isinstance(data, list)
    except Exception:
        ok = False
    add_result("GET /chat/history", resp, ok, detail=str(resp.text)[:200])

    # Mark soft-fail note if rate-limited
    if soft_fail:
        results.append(CheckResult(name="note", ok=True, status=429, detail="/prompt returned 429 after retries (rate limited)."))

    return results


def summarize(results: List[CheckResult]) -> int:
    failed = [r for r in results if not r.ok and r.name != "note"]
    print("\nAPI Health Check Summary:")
    for r in results:
        status = "PASS" if r.ok else "FAIL"
        print(f"- {r.name}: {status} (status={r.status})")
        if r.detail:
            # indent detail lightly
            detail = r.detail.replace("\n", " ")
            print(f"  detail: {detail[:160]}")
    print(f"\nTotal: {len(results)}  Passed: {len(results)-len(failed)}  Failed: {len(failed)}")
    return 0 if not failed else 1


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Elch API health checker")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Base URL of the API service (default: %(default)s)")
    parser.add_argument("--email", default=os.getenv("TEST_EMAIL"), help="User email for auth (default: $TEST_EMAIL or autogenerated)")
    parser.add_argument("--password", default=os.getenv("TEST_PASSWORD"), help="User password for auth (default: $TEST_PASSWORD or autogenerated)")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args(argv)

    email = args.email
    password = args.password

    # If credentials not provided, generate ephemeral account
    if not email or not password:
        import uuid
        email = f"healthcheck+{uuid.uuid4().hex[:8]}@example.com"
        password = uuid.uuid4().hex
        if args.verbose:
            print(f"Generated ephemeral account: {email}")

    client = APIClient(args.base_url, email, password, verbose=args.verbose)

    ok, token_or_error = client.authenticate()
    if not ok:
        print(f"Auth failed: {token_or_error}")
        return 2

    results = run_checks(client)
    return summarize(results)


if __name__ == "__main__":
    sys.exit(main())
