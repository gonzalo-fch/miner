import re


def extract_python_functions(code):

    pattern = r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\("

    return re.findall(pattern, code)


def extract_java_methods(code):

    pattern = r"(public|private|protected)?\s+[a-zA-Z0-9_<>\[\]]+\s+([a-zA-Z0-9_]+)\s*\("

    matches = re.findall(pattern, code)

    return [m[1] for m in matches]