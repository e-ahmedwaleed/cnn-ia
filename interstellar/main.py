from cli.utils import read_int
from cli.testing import run_pythons
from cli.sampling import run_dataflow_samples

if __name__ == "__main__":
    print("\nAvailable options:")
    print("_________________\n")

    print("(1) interstellar correctness tests")
    print("(2) interstellar samples (dataflow exploration)")

    print("\n(0) exit\n")

    choice = read_int("Enter your choice (0-2): ", 0, 2)

    if choice == 1:
        run_pythons("correctness/")
    elif choice == 2:
        timeout = read_int("Set time limit (in-secs): ", 0)
        run_dataflow_samples(timeout)
