#!/usr/bin/env python3
"""
Script to reset the circuit breaker for embedding generation
"""

import os

# Set the API keys as environment variables
os.environ['GEMINI_API_KEYS'] = 'AIzaSyCEerwHVrPXswY8P5nc8O-_p7xD-GZdK24,AIzaSyBLciY3gyPM58jTpzR6T5wVolpNPgWFTMI,AIzaSyCMWWcj-rb93ldri33KQU-K5Gz_XCxVXtg'

print("🔧 Resetting circuit breaker...")

try:
    from core.circuit_breaker import get_circuit_breaker, CircuitBreakerConfig
    
    # Get the circuit breaker and reset it
    circuit_breaker = get_circuit_breaker(
        'embedding_generation',
        CircuitBreakerConfig(
            failure_threshold=5,
            recovery_timeout=60.0,
            expected_exception=Exception,
            name='embedding_generation'
        )
    )
    
    # Force reset the circuit breaker
    circuit_breaker._state = 'CLOSED'
    circuit_breaker._failure_count = 0
    circuit_breaker._last_failure_time = 0
    
    print("✅ Circuit breaker reset successfully!")
    print(f"State: {circuit_breaker._state}")
    print(f"Failure count: {circuit_breaker._failure_count}")
    
    # Also reset the API key manager failures
    try:
        from gemini import api_key_manager
        api_key_manager.key_failures.clear()
        print("✅ API key failures cleared!")
    except Exception as e:
        print(f"⚠️  Could not clear API key failures: {e}")
    
except Exception as e:
    print(f"❌ Error resetting circuit breaker: {e}")

print("\n📝 Circuit breaker has been reset.")
print("The application should now be able to try the API keys again.")
