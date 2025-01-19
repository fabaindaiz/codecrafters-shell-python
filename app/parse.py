import sys

SCAPED_CHARS = ['\\', '$', '"', 'n']
REDIRECT_OPERATORS = ["2>>", "2>", "1>>", "1>", ">>", ">"]
DEFAULT_REDIRECT = sys.stdout.write

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
                if actual != "":
                    params.append(actual)
                    actual = ""
                continue
            case _:
                actual += char
    
    if actual != "":
        params.append(actual)
    return params, tab


def out_redirect(func, path: str, mode: str):
    def wrapper(text: str):
        with open(path, mode) as file:
            file.write(func(text))
            return text
    return wrapper

def parse_params(params: str):
    is_default_stdout = True
    is_default_stderr = True
    custom_stdout = lambda out: out
    custom_stderr = lambda err: err

    command = params[0]
    args: list[str] = []

    skip_param = False

    is_stdout = False
    is_stderr = False
    mode = "w"
    for param in params[1:]:
        match param:
            case _ if skip_param:
                continue

            case _ if is_stdout:
                custom_stdout = out_redirect(custom_stdout, path=param, mode=mode)
            
            case _ if is_stderr:
                custom_stderr = out_redirect(custom_stderr, path=param, mode=mode)

            case "1>" | ">":
                is_default_stdout = False
                is_stdout = True
                mode = "w"
                continue
            case "1>>" | ">>":
                is_default_stdout = False
                is_stdout = True
                mode = "a"
                continue

            case "2>":
                is_default_stderr = False
                is_stderr = True
                mode = "w"
                continue
            case "2>>":
                is_default_stderr = False
                is_stderr = True
                mode = "a"
                continue

            case _:
                args.append(param)

    stdout = DEFAULT_REDIRECT if is_default_stdout else custom_stdout
    stderr = DEFAULT_REDIRECT if is_default_stderr else custom_stderr
    return command, args, stdout, stderr

def filter_redirect(user_input: str):
    for operator in REDIRECT_OPERATORS:
        user_input = user_input.split(operator, 1)[0]
    return user_input