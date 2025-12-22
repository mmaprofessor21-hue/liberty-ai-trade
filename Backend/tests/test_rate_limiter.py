import pytest
from core import rate_limiter
from fastapi import HTTPException


def test_rate_limiter_allows_then_blocks():
    # Reset internal store
    rate_limiter._STORE.clear()

    key = "test-key"
    max_calls = 5
    period = 1  # short window for test

    # Should allow max_calls times
    for _ in range(max_calls):
        assert rate_limiter.check_rate_for_key(key, max_calls=max_calls, period_seconds=period)

    # Next call should raise HTTPException
    with pytest.raises(HTTPException):
        rate_limiter.check_rate_for_key(key, max_calls=max_calls, period_seconds=period)
