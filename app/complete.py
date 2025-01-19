
def autocomplete(input: str):
    tab = input.endswith("\t")
    input = input.rstrip("\t")

    if input.startswith("ech"):
        return "echo"
    if input.startswith("exi"):
        return "exit"

    return tab, input