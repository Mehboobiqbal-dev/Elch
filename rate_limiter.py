import time
import threading
from collections import defaultdict, deque
from typing import Dict, Optional
import logging

class RateLimiter:
    """
    Simple rate limiter to prevent API quota exhaustion.
    Implements a sliding window rate limiter with circuit breaker functionality.
    """

    def __init__(self):
        self.requests: Dict[str, deque] = defaultdict(deque)
        self.lock = threading.Lock()
        # Circuit breaker state
        self.circuit_breaker_failures: Dict[str, int] = defaultdict(int)
        self.circuit_breaker_last_failure: Dict[str, float] = {}
        self.circuit_breaker_open: Dict[str, bool] = defaultdict(bool)
        
    def is_allowed(self, key: str, max_requests: int = 60, window_seconds: int = 60) -> bool:
        """
        Check if a request is allowed based on rate limits.
        
        Args:
            key: Identifier for the rate limit (e.g., 'gemini', 'groq')
            max_requests: Maximum requests allowed in the window
            window_seconds: Time window in seconds
            
        Returns:
            True if request is allowed, False otherwise
        """
        current_time = time.time()
        
        with self.lock:
            # Clean old requests outside the window
            while (self.requests[key] and 
                   current_time - self.requests[key][0] > window_seconds):
                self.requests[key].popleft()
            
            # Check if we're under the limit
            if len(self.requests[key]) < max_requests:
                self.requests[key].append(current_time)
                return True
            
            return False
    
    def wait_if_needed(self, key: str, max_requests: int = 60, window_seconds: int = 60) -> Optional[float]:
        """
        Wait if rate limit would be exceeded.
        
        Returns:
            None if no wait needed, otherwise the wait time in seconds
        """
        if not self.is_allowed(key, max_requests, window_seconds):
            # Calculate wait time until oldest request expires
            with self.lock:
                if self.requests[key]:
                    oldest_request = self.requests[key][0]
                    wait_time = window_seconds - (time.time() - oldest_request) + 1
                    if wait_time > 0:
                        logging.info(f"Rate limit hit for {key}. Waiting {wait_time:.1f} seconds...")
                        time.sleep(wait_time)
                        return wait_time
        return None
    
    def get_remaining_requests(self, key: str, max_requests: int = 60, window_seconds: int = 60) -> int:
        """
        Get the number of remaining requests in the current window.
        """
        current_time = time.time()
        
        with self.lock:
            # Clean old requests
            while (self.requests[key] and 
                   current_time - self.requests[key][0] > window_seconds):
                self.requests[key].popleft()
            
            return max_requests - len(self.requests[key])

    def handle_success(self, key: str):
        """
        Handle successful request - reset circuit breaker failures.
        """
        with self.lock:
            if key in self.circuit_breaker_failures:
                self.circuit_breaker_failures[key] = 0
                self.circuit_breaker_open[key] = False
                logging.info(f"Circuit breaker reset for {key}")

    def handle_429_error(self, key: str):
        """
        Handle rate limit error - increment circuit breaker failures.
        """
        with self.lock:
            self.circuit_breaker_failures[key] += 1
            self.circuit_breaker_last_failure[key] = time.time()

            # Open circuit breaker after 3 consecutive failures
            if self.circuit_breaker_failures[key] >= 3:
                self.circuit_breaker_open[key] = True
                logging.warning(f"Circuit breaker opened for {key} after {self.circuit_breaker_failures[key]} failures")

    def get_circuit_breaker_status(self, key: str) -> Dict:
        """
        Get circuit breaker status for monitoring.
        """
        current_time = time.time()
        with self.lock:
            # Reset failure count if it's been more than 5 minutes
            if (key in self.circuit_breaker_last_failure and
                current_time - self.circuit_breaker_last_failure[key] > 300):
                self.circuit_breaker_failures[key] = 0
                self.circuit_breaker_open[key] = False

            return {
                "failures": self.circuit_breaker_failures[key],
                "is_open": self.circuit_breaker_open[key],
                "last_failure": self.circuit_breaker_last_failure.get(key, 0)
            }

# Global rate limiter instance
rate_limiter = RateLimiter()

def with_rate_limit(provider: str, max_requests: int = 50, window_seconds: int = 60):
    """
    Decorator to add rate limiting to API calls.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Wait if rate limit would be exceeded
            wait_time = rate_limiter.wait_if_needed(provider, max_requests, window_seconds)
            if wait_time:
                logging.info(f"Rate limited {provider} for {wait_time:.1f}s")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator