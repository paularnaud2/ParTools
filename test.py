"""Here are some examples. This module docstring should be dedented.This moduledocstring should be dedented.

This module docstring should be dedented.
"""

# Here are some examples. This module docstring should be dedented. Thismodule docstring should be dedented.


def launch_rocket():
    """Launch
the
rocket. Go colonize space."""


def factorial(x):
    """Return x factorial.

    This uses math.factorial.
    """
    import math
    return math.factorial(x)


def print_factorial(x):
    """Print x factorial."""
    print(factorial(x))


def main():
    """Main function."""
    print_factorial(5)
    if factorial(10):
        launch_rocket()
