import argparse
from huggingface_hub import HfApi


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_or_fileobj", "-f", type=str, required=True)
    parser.add_argument("--repo", "-r", type=str, required=True)
    parser.add_argument("--path_in_repo", type=str, required=True)
    parser.add_argument("--repo_type", type=str, required=True)
    parser.add_argument("--revision", type=str, default="main")
    return parser.parse_args()

def main(args):
    api = HfApi()
    api.upload_file(
        path_or_fileobj=args.path_or_fileobj,
        path_in_repo=args.path_in_repo,
        repo_id=args.repo,
        repo_type=args.repo_type,
        revision=args.revision,
    )

if __name__ == "__main__":
    args = parse_args()
    main(args)