import sys


def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")

    # Wait for user input
    user_input = input()

    sys.stdout.write(f"{user_input}: command not found")


if __name__ == "__main__":
    main()
