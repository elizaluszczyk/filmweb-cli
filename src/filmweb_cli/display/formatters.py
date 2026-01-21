import re


def prettify_camel_case(text: str) -> str:
    spaced = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    return spaced.lower()
