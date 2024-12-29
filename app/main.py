import os
import sys
import subprocess


HOME = os.getenv("HOME")
PATH = os.getenv("PATH").split(":")

def search_file_in_path(file_name):
    for path in PATH:
        if os.path.exists(f"{path}/{file_name}"):
            return f"{path}/{file_name}"
    return None


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
        return ("", None)
    
    return ("", f"cd: {folder}: No such file or directory\n")


DEFAULT_REDIRECT = sys.stdout.write
SCAPED_CHARS = ['\\', '$', '"', 'n']
BUILTIN = {
    "exit": _exit,
    "echo": _echo,
    "type": _type,
    "pwd": _pwd,
    "cd": _cd,
}   

def parse_input(input: str):
    actual = ""
    params: list[str] = []
    is_scaped = False
    in_single = False
    in_double = False

    for char in input:
        match char:
            case _ if is_scaped:
                if in_double and char not in SCAPED_CHARS:
                    actual += '\\'

                is_scaped = False
                actual += char
                continue

            case "'" if not in_double:
                in_single = not in_single
                continue
            case _ if in_single:
                actual += char
                continue

            case "\\":
                is_scaped = True
                continue
            case "\"":
                in_double = not in_double
                continue

            case " " if not in_double:
                if in_single:
                    actual += char
                elif actual != "":
                    params.append(actual)
                    actual = ""
                continue
            case _:
                actual += char
    
    if actual != "":
        params.append(actual)
    return params

def parse_params(params: str):
    is_default_stdout = True
    is_default_stderr = True
    custom_stdout = lambda out: out
    custom_stderr = lambda err: err

    command = params[0]
    args: list[str] = []

    is_stdout = False
    is_stderr = False
    for param in params[1:]:
        match param:
            case _ if is_stdout:
                def stdout_redirect(func):
                    def wrapper(text: str):
                        with open(param, "w") as file:
                            file.write(func(text))
                            return text
                    return wrapper
                custom_stdout = stdout_redirect(custom_stdout)
            
            case _ if is_stderr:
                def stderr_redirect(func):
                    def wrapper(text: str):
                        with open(param, "w") as file:
                            file.write(func(text))
                            return text
                    return wrapper
                custom_stderr = stderr_redirect(custom_stderr)

            case ">":
                is_default_stdout = False
                is_stdout = True
                continue
            case "1>":
                is_default_stdout = False
                is_stdout = True
                continue

            case "2>":
                is_default_stderr = False
                is_stderr = True
                continue

            case _:
                args.append(param)

    stdout = DEFAULT_REDIRECT if is_default_stdout else custom_stdout
    stderr = DEFAULT_REDIRECT if is_default_stderr else custom_stderr
    return command, args, stdout, stderr

def filter_redirect(user_input: str):
    return user_input.split("1>", 1)[0].split(">", 1)[0]

def main():
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        user_input = input()
        params = parse_input(user_input)
        command, args, stdout, stderr = parse_params(params)
        
        if command in BUILTIN:
            out, err = BUILTIN[command](args)
            stdout(out)
            stderr(err)
            continue
        
        command_file = search_file_in_path(command)
        if command_file:
            process_args = filter_redirect(user_input)
            process = subprocess.Popen(args=process_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            stdout(output.decode())
            stderr(error.decode() if error else "")
            process.wait()
            continue
        
        sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
