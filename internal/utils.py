def file_name_type(file: str) -> (str, str):
    tokens = file.split(".")
    return ".".join(tokens[:-1]), tokens[-1]


def comand_text(text: str) -> (str, str):
    tokens = text.split()
    return tokens[0], ' '.join(tokens[1:])
