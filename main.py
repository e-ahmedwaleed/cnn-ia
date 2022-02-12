from utils import run_python, run_pythons

print("\nAvailable options:")
print("_________________\n")

print("(1) cnn-model parameters extractor")
print("(2) interstellar correctness tests")

print("\n(0) exit\n")

choice = 0

while True:
    try:
        choice = int(input("Enter your choice (0-2): ")[0])
        if choice <= 2:
            break
    except ValueError:
        continue
    except IndexError:
        continue

if choice == 1:
    run_python("./phase-1-extractor/main.py")
elif choice == 2:
    run_pythons("./interstellar/test-correctness/")
