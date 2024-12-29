import sys

BUILTIN = ["type", "exit", "echo"]

def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        parsed_input = input().split(" ")
        command = parsed_input[0]
        params = parsed_input[1:]

        if command in BUILTIN:
            match command:
                case "type":
                    # hardcoded for now
                    if params[0] in BUILTIN:
                        sys.stdout.write(f"{params[0]} is a shell builtin\n")
                    else:
                        sys.stdout.write(f"{params[0]}: not found\n")
                case "exit":
                    exit_code = int(params[0])
                    sys.exit(exit_code)
                case "echo":
                    sys.stdout.write(" ".join(params) + "\n")
        else:
            sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
