# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull

# References for suppress_stdout_stderr (Unchanged)
# https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
# https://creativecommons.org/licenses/by-sa/3.0/
@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)