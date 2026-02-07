import time
import tracemalloc
from contextlib import contextmanager


@contextmanager
def profile_block(label: str):
    """
    Lightweight performance profiler for edge systems.
    Measures wall-clock latency and peak memory usage.
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    try:
        yield
    finally:
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(
            f"[PERF] {label} | "
            f"latency={(end_time - start_time)*1000:.2f} ms | "
            f"peak_memory={peak / (1024 * 1024):.2f} MB"
        )
