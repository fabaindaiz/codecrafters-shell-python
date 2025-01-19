import sys
import subprocess

from app.builtin import BUILTIN
from app.complete import autocomplete
from app.parse import parse_input, parse_params, filter_redirect
from app.utils import search_file_in_path

def main():
    autocomplete = ""

    while True:
        sys.stdout.write(f"$ {autocomplete}")
        autocomplete = ""

        user_input = input()
        tab, user_input = autocomplete(user_input)
        if tab:
            autocomplete = user_input
            continue

        params = parse_input(user_input)
        command, args, stdout, stderr = parse_params(params)
        
        if command in BUILTIN:
            output, error = BUILTIN[command](args)
            stdout(output)
            stderr(error)
            continue
        
        command_file = search_file_in_path(command)
        if command_file:
            process_args = filter_redirect(user_input).replace(command, command_file)
            process = subprocess.Popen(args=process_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            stdout(output.decode())
            stderr(error.decode() if error else "")
            process.wait()
            continue
        
        sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
