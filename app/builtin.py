import os
import sys

from app.utils import search_file_in_path, HOME

def _exit(args: list[str]):
    exit_code = int(args[0])
    sys.exit(exit_code)

def _echo(args: list[str]):
    return (" ".join(args) + "\n", "")

def _type(args: list[str]):
    command = args[0]
    if command in BUILTIN:
        return (f"{command} is a shell builtin\n", "")
    
    command_file = search_file_in_path(command)
    if command_file:
        return (f"{command} is {command_file}\n", "")
    
    return ("", f"{command}: not found\n")

def _pwd(args: list[str]):
    return (os.getcwd() + "\n", "")

def _cd(args: list[str]):
    folder = args[0] if len(args) > 0 else HOME
    folder = folder.replace('~', HOME)

    if os.path.exists(folder):
        os.chdir(folder)
        return ("", "")
    
    return ("", f"cd: {folder}: No such file or directory\n")

BUILTIN = {
    "exit": _exit,
    "echo": _echo,
    "type": _type,
    "pwd": _pwd,
    "cd": _cd,
}