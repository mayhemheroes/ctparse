#! /usr/bin/env python3
import atheris
import datetime
import io
import sys
import fuzz_helpers
from contextlib import contextmanager

with atheris.instrument_imports(include=['ctparse']):
    import ctparse

@contextmanager
def nostdout():
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    yield
    sys.stdout = save_stdout
    sys.stderr = save_stderr

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    yr = fdp.ConsumeIntInRange(1, 9999)
    mo = fdp.ConsumeIntInRange(1, 12)
    dy = fdp.ConsumeIntInRange(1, 31)
    hr = fdp.ConsumeIntInRange(1, 23)
    mn = fdp.ConsumeIntInRange(0, 59)
    sc = fdp.ConsumeIntInRange(0, 59)
    try:
        mcs = fdp.ConsumeIntInRange(0, 999999)
        ts = datetime.datetime(yr, mo, dy, hr, mn, sc, mcs)
        with nostdout():
            ctparse.ctparse(fdp.ConsumeRemainingString(), ts=ts)
    except ValueError as e:
        if 'out of range' in str(e):
            return -1
        raise e


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
