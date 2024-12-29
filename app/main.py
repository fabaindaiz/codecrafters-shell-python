import sys


def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        user_input = input().split(" ")

        command = user_input[0]

        match user_input:
            case "exit":
                exit_code = int(command[1])
                sys.exit(exit_code)

        sys.stdout.write(f"{user_input}: command not found\n")

if __name__ == "__main__":
    main()
