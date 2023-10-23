def file_name_type(str) -> (str, str):
    domains = str.split(".")
    return ".".join(domains[:-1]), domains[-1]


