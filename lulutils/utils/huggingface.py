import re

def get_hf_file_info(uri) -> dict:
    """
    Parse a huggingface file url or a defined schema of the url to file info.
    # hf://repo_id@repo_type@revision@filename
    # https://huggingface.co/repo_id/resolve/revision/filename

    Params:
      input a downloadable huggingface file url or a defined schema of the url
    Returns:
      a dict of the file info {
        "repo_id": str,
        "repo_type": str or None,
        "revision": str,
        "filename": str
      }
    Raises:
      ValueError: if the url is invalid
    """

    if uri.startswith("hf://"):
        pattern = re.compile(r"^hf://(?P<repo_id>[^@]+)@(?P<repo_type>[^@]*)@(?P<revision>[^@]+)@(?P<filename>.+)$")
        match = pattern.match(uri)
    elif uri.startswith("https://huggingface.co/"):
        pattern = re.compile(r"^https://huggingface\.co/(?:(?P<repo_type>datasets|models)/)?(?P<repo_id>[^/]+/[^/]+)/resolve/(?P<revision>[^/]+)/(?P<filename>.+)$")
        match = pattern.match(uri)

    if match:
        match = match.groupdict()

        if not match["repo_type"]:
            match["repo_type"] = "model"
        if match["repo_type"] == "datasets":
            match["repo_type"] = "dataset"
        return match
    else:
        raise ValueError(f"Invalid uri: {uri}")
