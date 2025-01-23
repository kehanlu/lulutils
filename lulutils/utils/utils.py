import os

def get_filename(filepath):
    """
    Get the filename of a file. If the file already exists, increment the filename.
    """
    if not os.path.exists(filepath):
        return filepath
    base, ext = os.path.splitext(filepath)
    i = 1
    while os.path.exists(f"{base}.{i}{ext}"):
        i += 1
    return f"{base}.{i}{ext}"


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