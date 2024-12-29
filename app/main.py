import os
import sys

def _exit(params: list[str]):
    sys.exit(int(params[0]))

def _echo(params: list[str]):
    sys.stdout.write(" ".join(params) + "\n")

def _type(params: list[str]):
    if params[0] in BUILTIN:
        sys.stdout.write(f"{params[0]} is a shell builtin\n")
        return
    
    path_location = search_file_in_path(params[0])
    if path_location:
        sys.stdout.write(f"{params[0]} is {path_location}\n")
        return
    
    sys.stdout.write(f"{params[0]}: not found\n")

def _pwd(params: list[str]):
    sys.stdout.write(f"{os.getcwd()}\n")

def _cd(params: list[str]):
    if os.path.exists(params[0]):
        os.chdir(params[0])
    else:
        sys.stdout.write(f"cd: {params[0]}: No such file or directory\n")


BUILTIN = {
    "exit": _exit,
    "echo": _echo,
    "type": _type,
    "pwd": _pwd,
    "cd": _cd,
}

def execute_command(command: str, params: list[str]):
    if command in BUILTIN:
        BUILTIN[command](params)
        return
    
    path_location = search_file_in_path(params[0])
    if path_location:
        os.system(f"{path_location} {' '.join(params)}")
        return
    
    sys.stdout.write(f"{command}: command not found\n")


ENV = os.getenv("PATH")

env_paths = ENV.split(":")

def search_file_in_path(file_name):
    for path in env_paths:
        if os.path.exists(f"{path}/{file_name}"):
            return f"{path}/{file_name}"
    return None


def parse_input(input: str):
    splited = input.split(" ")
    return splited[0], splited[1:]


def main():
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        user_input = input()

        command, params = parse_input(user_input)
        execute_command(command, params)

if __name__ == "__main__":
    main()
