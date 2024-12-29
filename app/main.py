import os
import sys

HOME = os.getenv("HOME")
PATH = os.getenv("PATH").split(":")

def search_file_in_path(file_name):
    for path in PATH:
        if os.path.exists(f"{path}/{file_name}"):
            return f"{path}/{file_name}"
    return None


def _exit(params: list[str]):
    exit_code = int(params[0])
    sys.exit(exit_code)

def _echo(params: list[str]):
    echo_str = " ".join(params) + "\n"
    sys.stdout.write(echo_str)

def _type(params: list[str]):
    command = params[0]
    if command in BUILTIN:
        sys.stdout.write(f"{command} is a shell builtin\n")
        return
    
    command_file = search_file_in_path(command)
    if command_file:
        sys.stdout.write(f"{command} is {command_file}\n")
        return
    
    sys.stdout.write(f"{command}: not found\n")

def _pwd(params: list[str]):
    cwd_str = os.getcwd() + "\n"
    sys.stdout.write(cwd_str)

def _cd(params: list[str]):
    folder = params[0] if len(params) > 0 else HOME
    folder.replace("~", HOME)

    if os.path.exists(folder):
        os.chdir(folder)
    else:
        sys.stdout.write(f"cd: {folder}: No such file or directory\n")


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
    
    command_file = search_file_in_path(command)
    if command_file:
        params_str = " ".join(params)
        os.system(f"{command_file} {params_str}")
        return
    
    sys.stdout.write(f"{command}: command not found\n")


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
