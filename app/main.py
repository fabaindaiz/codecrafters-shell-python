import os
import sys

BUILTIN = ["type", "exit", "echo"]
ENV = os.getenv("PATH")

env_paths = ENV.split(":")

def search_file_in_path(file_name):
    for path in env_paths:
        if os.path.exists(f"{path}/{file_name}"):
            return f"{path}/{file_name}"
    return None

def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        parsed_input = input().split(" ")
        command = parsed_input[0]
        params = parsed_input[1:]

        match command:
            case "type":
                # hardcoded for now
                path_location = search_file_in_path(params[0])
                if params[0] in BUILTIN:
                    sys.stdout.write(f"{params[0]} is a shell builtin\n")
                elif path_location:
                    sys.stdout.write(f"{params[0]} is {path_location}\n")
                else:
                    sys.stdout.write(f"{params[0]}: not found\n")
            case "exit":
                exit_code = int(params[0])
                sys.exit(exit_code)
            case "echo":
                sys.stdout.write(" ".join(params) + "\n")
            case _:
                path_location = search_file_in_path(command)
                if path_location:
                    os.system(f"{path_location} {' '.join(params)}")
                else:
                    sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
