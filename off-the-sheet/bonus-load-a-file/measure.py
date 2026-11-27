# Runs each level-3 script in a fresh process and prints its time and peak memory.
# Peak memory uses the "resource" module, so this works on Mac and Linux, not Windows.
import subprocess, sys

RUNNER = (
    "import resource, runpy, sys, time\n"
    "start = time.perf_counter()\n"
    "runpy.run_path(sys.argv[1])\n"
    "seconds = time.perf_counter() - start\n"
    "peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss\n"
    "peak_mb = peak / 1024 / (1024 if sys.platform == 'darwin' else 1)\n"
    "print(f'{seconds:.2f} s, peak memory {peak_mb:.0f} MB', file=sys.stderr)\n"
)

for script in ["level3_pandas.py", "level3_polars.py"]:
    done = subprocess.run([sys.executable, "-c", RUNNER, script],
                          capture_output=True, text=True)
    print(f"{script}: answer {done.stdout.strip()}, {done.stderr.strip()}")
