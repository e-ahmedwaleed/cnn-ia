print("\nAvailable Options:")
print("_________________\n")

print("(1) cnn-model parameters extractor")
print("(2) interstellar correctness tests")

print("\n(0) Exit\n")

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
    print("cnn-model parameters extractor...")
elif choice == 2:
    print("interstellar correctness tests...")
