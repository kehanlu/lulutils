from huggingface_hub import HfApi
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True)
    # parser.add_argument("--path_in_repo", type=str, required=True)
    parser.add_argument("--repo_id", type=str, required=True)
    parser.add_argument("--revision", type=str, default="main")
    parser.add_argument("--shift", type=int, default=0)

    return parser.parse_args()

def main(args):
    api = HfApi()

    api.upload_large_folder(
        folder_path=args.folder, # Path to the folder to upload
        # path_in_repo=args.path_in_repo, # Upload to a specific folder
        repo_id=args.repo_id, # ID of the repo to upload to
        repo_type="dataset",
        revision=args.revision,
    )

if __name__ == "__main__":
    args = parse_args()
    main(args)