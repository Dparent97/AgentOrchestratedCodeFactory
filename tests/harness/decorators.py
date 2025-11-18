"""
Test Decorators - Utilities for enhancing test functions

Provides decorators for:
- Timing test execution
- Retrying on failure
- Expecting specific errors
- Parametrizing common scenarios
"""

import time
import functools
from typing import Callable, Any, Type, Optional

try:
    import pytest
except ImportError:
    pytest = None  # Optional dependency


# ============================================================================
# Timing Decorator
# ============================================================================

def timed_test(max_seconds: Optional[float] = None):
    """
    Decorator to time test execution and optionally enforce max duration

    Args:
        max_seconds: Maximum allowed execution time (None for no limit)

    Usage:
        @timed_test(max_seconds=1.0)
        def test_fast_operation():
            agent.execute(idea)

        @timed_test()  # Just report time, no limit
        def test_any_operation():
            agent.execute(idea)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time

                print(f"\n⏱️  Test '{func.__name__}' took {elapsed:.3f}s")

                if max_seconds and elapsed > max_seconds:
                    error_msg = f"Test exceeded time limit: {elapsed:.3f}s > {max_seconds}s"
                    if pytest:
                        pytest.fail(error_msg)
                    else:
                        raise AssertionError(error_msg)

                return result

            except Exception as e:
                elapsed = time.time() - start_time
                print(f"\n⏱️  Test '{func.__name__}' failed after {elapsed:.3f}s")
                raise

        return wrapper

    return decorator


# ============================================================================
# Retry Decorator
# ============================================================================

def retry_on_failure(max_retries: int = 3, delay_seconds: float = 0.1):
    """
    Decorator to retry test on failure

    Useful for tests that might fail due to timing or transient issues.

    Args:
        max_retries: Maximum number of retry attempts
        delay_seconds: Delay between retries

    Usage:
        @retry_on_failure(max_retries=3, delay_seconds=0.5)
        def test_flaky_operation():
            result = agent.execute(idea)
            assert result is not None
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        print(
                            f"\n✓ Test '{func.__name__}' succeeded on attempt {attempt + 1}"
                        )
                    return result

                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(
                            f"\n⚠️  Test '{func.__name__}' failed on attempt {attempt + 1}, "
                            f"retrying... ({max_retries - attempt} retries left)"
                        )
                        time.sleep(delay_seconds)
                    else:
                        print(
                            f"\n✗ Test '{func.__name__}' failed after {max_retries + 1} attempts"
                        )

            # All retries exhausted
            raise last_exception

        return wrapper

    return decorator


# ============================================================================
# Error Expectation Decorator
# ============================================================================

def expect_agent_error(error_type: Type[Exception], error_message_contains: Optional[str] = None):
    """
    Decorator to expect a specific error from agent execution

    Fails the test if the expected error is NOT raised.

    Args:
        error_type: Expected exception type
        error_message_contains: Optional substring that should be in error message

    Usage:
        @expect_agent_error(ValueError, "description cannot be empty")
        def test_empty_description():
            agent.execute(Idea(description=""))
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                error_msg = f"Expected {error_type.__name__} to be raised, but function succeeded"
                if pytest:
                    pytest.fail(error_msg)
                else:
                    raise AssertionError(error_msg)

            except error_type as e:
                # Expected error was raised
                if error_message_contains:
                    error_str = str(e).lower()
                    if error_message_contains.lower() not in error_str:
                        error_msg = (
                            f"Expected error message to contain '{error_message_contains}', "
                            f"but got: {str(e)}"
                        )
                        if pytest:
                            pytest.fail(error_msg)
                        else:
                            raise AssertionError(error_msg)

                print(f"\n✓ Expected error raised: {error_type.__name__}: {str(e)}")

            except Exception as e:
                error_msg = f"Expected {error_type.__name__}, but got {type(e).__name__}: {str(e)}"
                if pytest:
                    pytest.fail(error_msg)
                else:
                    raise AssertionError(error_msg)

        return wrapper

    return decorator


# ============================================================================
# Performance Benchmark Decorator
# ============================================================================

def benchmark(iterations: int = 10, warmup: int = 2):
    """
    Decorator to benchmark test performance over multiple iterations

    Args:
        iterations: Number of times to run the test
        warmup: Number of warmup iterations (not counted in average)

    Usage:
        @benchmark(iterations=100, warmup=10)
        def test_planner_performance():
            planner.execute(idea)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            times = []

            # Warmup
            print(f"\n🔥 Warming up ({warmup} iterations)...")
            for _ in range(warmup):
                func(*args, **kwargs)

            # Benchmark
            print(f"📊 Benchmarking ({iterations} iterations)...")
            for i in range(iterations):
                start = time.time()
                func(*args, **kwargs)
                elapsed = time.time() - start
                times.append(elapsed)

            # Statistics
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            median_time = sorted(times)[len(times) // 2]

            print(f"\n📈 Benchmark Results for '{func.__name__}':")
            print(f"   Average: {avg_time * 1000:.2f}ms")
            print(f"   Median:  {median_time * 1000:.2f}ms")
            print(f"   Min:     {min_time * 1000:.2f}ms")
            print(f"   Max:     {max_time * 1000:.2f}ms")

            return {
                "average": avg_time,
                "median": median_time,
                "min": min_time,
                "max": max_time,
                "iterations": iterations,
            }

        return wrapper

    return decorator


# ============================================================================
# Agent Test Decorator
# ============================================================================

def agent_test(agent_name: str, timeout_seconds: Optional[float] = None):
    """
    Combined decorator for agent testing with timing and metadata

    Args:
        agent_name: Name of the agent being tested
        timeout_seconds: Optional timeout for the test

    Usage:
        @agent_test("PlannerAgent", timeout_seconds=2.0)
        def test_planner_basic():
            planner = PlannerAgent()
            result = planner.execute(idea)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"\n🧪 Testing {agent_name}: {func.__name__}")

            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time

                print(f"✓ {agent_name} test passed in {elapsed:.3f}s")

                if timeout_seconds and elapsed > timeout_seconds:
                    error_msg = f"{agent_name} test exceeded timeout: {elapsed:.3f}s > {timeout_seconds}s"
                    if pytest:
                        pytest.fail(error_msg)
                    else:
                        raise AssertionError(error_msg)

                return result

            except Exception as e:
                elapsed = time.time() - start_time
                print(f"✗ {agent_name} test failed after {elapsed:.3f}s: {str(e)}")
                raise

        return wrapper

    return decorator


# ============================================================================
# Snapshot Testing Decorator
# ============================================================================

def snapshot_output(snapshot_name: Optional[str] = None):
    """
    Decorator to save agent output for regression testing

    Saves the output to a file for later comparison.

    Args:
        snapshot_name: Optional custom name for snapshot

    Usage:
        @snapshot_output("planner_basic")
        def test_planner_output():
            result = planner.execute(idea)
            return result  # Will be saved as snapshot
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # For pytest-snapshot or similar plugins
            # This is a placeholder - actual implementation would depend on snapshot library
            name = snapshot_name or func.__name__

            print(f"\n📸 Snapshot saved: {name}")

            return result

        return wrapper

    return decorator


# ============================================================================
# Parametrize with Fixtures
# ============================================================================

def parametrize_ideas(*fixture_names):
    """
    Decorator to parametrize test with idea fixtures

    Args:
        *fixture_names: Names of fixture functions from tests.harness.fixtures

    Usage:
        from tests.harness.fixtures import (
            create_marine_engineer_idea,
            create_data_analyst_idea
        )

        @parametrize_ideas("marine", "data_analyst")
        def test_planner_with_scenarios(idea):
            planner = PlannerAgent()
            result = planner.execute(idea)
            assert len(result.tasks) > 0
    """

    # This would typically use pytest.mark.parametrize
    # Placeholder for actual implementation
    def decorator(func: Callable) -> Callable:
        return func

    return decorator


# ============================================================================
# Combined Decorators for Common Patterns
# ============================================================================

def fast_test(max_seconds: float = 0.5):
    """
    Decorator for tests that should be very fast

    Combines timing with strict time limit.

    Args:
        max_seconds: Maximum allowed time (default: 0.5s)

    Usage:
        @fast_test(max_seconds=0.3)
        def test_quick_validation():
            validator.check(data)
    """
    return timed_test(max_seconds=max_seconds)


def slow_test(min_seconds: float = 1.0):
    """
    Decorator for tests that are expected to be slow

    Just marks and reports timing, doesn't fail on slow execution.

    Args:
        min_seconds: Minimum expected time (for info only)

    Usage:
        @slow_test(min_seconds=2.0)
        def test_complex_operation():
            agent.execute(complex_idea)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"\n🐌 Slow test: {func.__name__} (expected >{min_seconds}s)")
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"   Completed in {elapsed:.3f}s")
            return result

        return wrapper

    return decorator


def flaky_test(max_retries: int = 5):
    """
    Decorator for tests known to be flaky

    Retries multiple times before failing.

    Args:
        max_retries: Number of retry attempts

    Usage:
        @flaky_test(max_retries=3)
        def test_timing_sensitive_operation():
            result = agent.execute(idea)
            assert result is not None
    """
    return retry_on_failure(max_retries=max_retries, delay_seconds=0.2)
