import os
import json
from huggingface_hub import hf_hub_download
from .huggingface import get_hf_file_info

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

def load_jsonl(filepath):
    return [json.loads(line) for line in open(filepath, "r")]

