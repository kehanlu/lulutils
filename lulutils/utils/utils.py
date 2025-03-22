import os
import json
from collections.abc import Iterable
from huggingface_hub import hf_hub_download
from lulutils.utils.huggingface import get_hf_file_info
import builtins

def get_unique_filepath(filepath):
    """
    Generate a unique filepath by incrementing the filename.
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
    Resolve the filepath from the uri.
    If the file is not local, download the file from huggingface.
    """
    # Downloadable link
    if uri.startswith("hf://") or uri.startswith("https://huggingface.co"):
        info = get_hf_file_info(uri)
        return hf_hub_download(repo_type=info["repo_type"], repo_id=info["repo_id"], filename=info["filename"], revision=info["revision"], cache_dir=os.getenv("HF_HOME"))
    else:
        return uri

def check_consecutive_words(long_string, short_string):
    """
    Check if the short string is consecutive in the long string.
    """
    # Convert text to lowercase and split into a list of words
    long_string_words = long_string.lower().split()
    
    # Convert words to check to lowercase
    short_string_words = short_string.lower().split()
    
    # Check for consecutive sequence
    for i in range(len(long_string_words) - len(short_string_words) + 1):
        if long_string_words[i:i+len(short_string_words)] == short_string_words:
            return True
    return False


def normalize_text(text):
    from whisper_normalizer.basic import BasicTextNormalizer
    normalizer = BasicTextNormalizer()
    return normalizer(text).strip()


def calculate_accuracy(preds, labels) -> list[int]:
    """
    Calculate the accuracy of the predictions.
    """
    assert len(preds) == len(labels)
    correct = []
    for pred, label in zip(preds, labels):
        pred = normalize_text(pred)
        label = normalize_text(label)
        if check_consecutive_words(pred, label):
            correct.append(1)
        else:
            correct.append(0)
    
    return correct

def read_jsonl(filepaths) -> list[dict]:
    """
    read jsonl files to list of dictionaries
    """
    if isinstance(filepaths, str):
        return read_jsonl([filepaths])
    elif isinstance(filepaths, Iterable):
        return [json.loads(line) for filepath in filepaths for line in open(filepath, "r")]


def print(text, color=None, bold=False):
    """
    Print colored and/or bold text to the terminal.
    
    Args:
        text: The text to print
        color: Color name (red, green, blue, yellow, magenta, cyan)
        bold: Whether to make the text bold
    """
    # ANSI escape code components
    colors = {
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37'
    }
    
    reset = '\033[0m'
    
    # Start with empty formatting
    formatting = '\033['
    
    # Add bold if requested
    if bold:
        formatting += '1'
        # Add separator if we're also adding color
        if color:
            formatting += ';'
    
    # Add color if requested
    if color and color.lower() in colors:
        formatting += colors[color.lower()]
    
    # Complete the escape sequence
    formatting += 'm'
    
    # If no formatting requested, don't add codes
    if formatting == '\033[m':
        formatting = ''
        reset = ''
    
    # Use the built-in print function
    __builtins__['print'](formatting + str(text) + reset)