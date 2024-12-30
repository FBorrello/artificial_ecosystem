import time


class RateLimiter:
    def __init__(self, limit: int, interval: int):
        self.limit = limit
        self.interval = interval
        self.last_call_time = None
        self.calls = 0

    def limit_calls(self, func: callable) -> callable:
        def wrapper(*args, **kwargs):
            if self.last_call_time is None:
                self.last_call_time = time.time()
                self.calls += 1
                return func(*args, **kwargs)
            elif time.time() - self.last_call_time < self.interval and self.calls >= self.limit:
                print(f"Rate limit of {self.limit} calls within max {self.interval} seconds exceeded. Waiting...")
            elif time.time() - self.last_call_time < self.interval and self.calls < self.limit:
                self.calls += 1
                return func(*args, **kwargs)
            elif time.time() - self.last_call_time >= self.interval:
                self.calls = 1
                self.last_call_time = time.time()
                return func(*args, **kwargs)
        return wrapper


rate_limiter = RateLimiter(limit=3, interval=5)


@rate_limiter.limit_calls
def test_function():
    print("Function executed.")


# Call the test function multiple times.
test_function()  # Executes normally
test_function()  # Executes normally
test_function()  # Executes normally
test_function()  # Output: "Rate limit exceeded."
time.sleep(10)
test_function()