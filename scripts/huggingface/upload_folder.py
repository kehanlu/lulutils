from huggingface_hub import HfApi
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--path_in_repo", type=str, required=True)
    parser.add_argument("--repo_id", type=str, required=True)
    parser.add_argument("--revision", type=str, default="main")

    parser.add_argument("--mode", type=str, default="normal")

    return parser.parse_args()

def main(args):
    api = HfApi()

    print("================ Start Uploading ================")
    if args.mode == "normal":
        assert args.path_in_repo is not None

        api.create_branch(
            repo_id=args.repo_id,
            repo_type="dataset",
            branch=args.revision,
            exist_ok=True  # Won't error if branch already exists
        )

        api.upload_folder(
            folder_path=args.folder,
            path_in_repo=args.path_in_repo,
            repo_id=args.repo_id,
            repo_type="dataset",
            revision=args.revision,
        )
    elif args.mode == "large":
        api.upload_large_folder(
            folder_path=args.folder,
            repo_id=args.repo_id,
            repo_type="dataset",
            revision=args.revision,
        )
    else:
        raise ValueError(f"Invalid mode: {args.mode}")
    
    print("================ Done ================")

if __name__ == "__main__":
    args = parse_args()
    main(args)