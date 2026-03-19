import os
import json
from collections.abc import Iterable
from huggingface_hub import hf_hub_download
from lulutils.huggingface import get_hf_file_info

def get_unique_filepath(filepath):
    """
    Generate a unique filepath by appending an index if the file already exists.

    Args:
        filepath (str): The desired output filepath.

    Returns:
        str: A filepath that does not currently exist on disk.

    Example:
        >>> get_unique_filepath("output/result.json")
        "output/result.json"      # if it doesn't exist
        "output/result.1.json"    # if result.json already exists
        "output/result.2.json"    # if result.1.json also exists
    """
    if not os.path.exists(filepath):
        return filepath
    base, ext = os.path.splitext(filepath)
    i = 1
    while os.path.exists(f"{base}.{i}{ext}"):
        i += 1
    return f"{base}.{i}{ext}"


def resolve_filepath(uri) -> str:
    """
    Resolve a URI to a local filepath.
    If the URI points to a HuggingFace file, it will be downloaded and cached.

    Args:
        uri (str): A local path or a HuggingFace URI.

    Returns:
        str: An absolute local filepath.

    Supported formats:
        - Local path:
            resolve_filepath("/data/train.jsonl")
            → "/data/train.jsonl"

        - HuggingFace URL:
            resolve_filepath("https://huggingface.co/kehanlu/my-dataset/resolve/main/data/train.jsonl")
            → "/home/user/.cache/huggingface/hub/.../train.jsonl"

        - HuggingFace schema: hf://<repo_id>@<repo_type>@<revision>@<filename>
            resolve_filepath("hf://kehanlu/my-dataset@@main@data/train.jsonl")
            → "/home/user/.cache/huggingface/hub/.../train.jsonl"
    """
    # Downloadable link
    if uri.startswith("hf://") or uri.startswith("https://huggingface.co"):
        info = get_hf_file_info(uri)
        return hf_hub_download(repo_type=info["repo_type"], repo_id=info["repo_id"], filename=info["filename"], revision=info["revision"], cache_dir=os.getenv("HF_HOME"))
    else:
        return uri

def read_jsonl(filepaths) -> list[dict]:
    """
    Read one or more JSONL files into a list of dicts.

    Args:
        filepaths (str | list[str]): A single filepath or a list of filepaths.

    Returns:
        list[dict]: All records from the file(s) concatenated in order.

    Example:
        >>> read_jsonl("data/train.jsonl")
        [{"id": 1, "text": "hello"}, ...]

        >>> read_jsonl(["data/train.jsonl", "data/dev.jsonl"])
        [{"id": 1, ...}, {"id": 2, ...}, ...]
    """
    if isinstance(filepaths, str):
        return read_jsonl([filepaths])
    elif isinstance(filepaths, Iterable):
        return [json.loads(line) for filepath in filepaths for line in open(filepath, "r")]


def print(*args, color=None, bold=False, sep=' ', end='\n'):
    """
    Print colored and/or bold text to the terminal.

    Args:
        *args: Values to print (same as built-in print).
        color (str): Color name. Options: red, green, yellow, blue, magenta, cyan, white.
        bold (bool): Whether to bold the text. Default: False.
        sep (str): Separator between values. Default: ' '.
        end (str): String appended after the last value. Default: newline.

    Example:
        >>> print("done", color="green")
        >>> print("A", "B", "C", color="red")
        >>> print("warning", color="yellow", bold=True)
        >>> print("x", "y", sep="-", color="cyan", end="")
    """
    colors = {
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37'
    }

    text = sep.join(str(a) for a in args)
    reset = '\033[0m'
    formatting = '\033['

    if bold:
        formatting += '1'
        if color:
            formatting += ';'

    if color and color.lower() in colors:
        formatting += colors[color.lower()]

    formatting += 'm'

    if formatting == '\033[m':
        formatting = ''
        reset = ''

    __builtins__['print'](formatting + text + reset, end=end)
