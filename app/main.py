import sys


def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        parsed_input = input().split(" ")
        command = parsed_input[0]
        params = parsed_input[1:]

        match command:
            case "exit":
                exit_code = int(params[0])
                sys.exit(exit_code)
            case "echo":
                sys.stdout.write(" ".join(params) + "\n")
            case _:
                sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
