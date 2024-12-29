import sys


def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        user_input = input().split(" ")

        command = user_input[0]

        match command:
            case "exit":
                exit_code = int(user_input[1])
                sys.exit(exit_code)
            case _:
                sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
