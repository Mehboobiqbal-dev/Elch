import google.generativeai as genai
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

# Load .env files to populate environment variables
# Prefer root .env, then backend/.env (if they exist), mirroring core/config.py behavior
project_root = Path(__file__).resolve().parent
root_env = project_root / ".env"
backend_env = project_root / "backend" / ".env"

if load_dotenv:
    if root_env.exists():
        load_dotenv(dotenv_path=root_env)
    if backend_env.exists():
        load_dotenv(dotenv_path=backend_env)

# Load keys from env: prefer GEMINI_API_KEYS (comma-separated), fall back to GEMINI_API_KEY
raw_keys = os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY", "")
api_keys = [k.strip() for k in raw_keys.split(",") if k.strip()]

if not api_keys:
    print("No Gemini API keys configured in environment.")
    print("Checked .env at:", root_env, "and", backend_env)
    exit(1)

# Deduplicate while preserving order
seen = set()
keys = []
for k in api_keys:
    if k not in seen:
        keys.append(k)
        seen.add(k)

MODEL = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-pro")


def try_key(k: str) -> bool:
    try:
        genai.configure(api_key=k)
        model = genai.GenerativeModel(MODEL)
        resp = model.generate_content("ping")
        text = getattr(resp, "text", "<no text>") or "<empty>"
        print("OK:", text[:120].replace("\n", " ") + ("..." if len(text) > 120 else ""))
        return True
    except Exception as e:
        print("ERR:", str(e))
        return False


def main():
    print(f"Testing {len(keys)} Gemini keys against model '{MODEL}'...")
    success = 0
    for idx, k in enumerate(keys, 1):
        print(f"[{idx}/{len(keys)}] Trying key prefix {k[:10]}...")
        if try_key(k):
            success += 1
    print(f"Done. Success {success}/{len(keys)}.")


if __name__ == "__main__":
    main()
