
import argparse
from pathlib import Path
import json
import webdataset as wds
import os
from lulutils import caesar_name
from collections import defaultdict
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_manifest", "-i", type=str)
    parser.add_argument("--dataset_name", "-n", type=str, required=True)
    parser.add_argument("--output_folder", "-o", type=str, required=True)
    parser.add_argument("--data_root", type=str, nargs="+", required=True)
    parser.add_argument("--ext", type=str, default="wav")
    parser.add_argument("--maxcount", type=int, default=100000)
    parser.add_argument("--maxsize", type=int, default=1e9)
    parser.add_argument("--shift", type=int, default=0)
    return parser.parse_args()

def extract_rel_path(path, roots):
    if isinstance(roots, str):
        roots = [roots]
    
    for root in roots:
        root_path = Path(root)
        if path.is_relative_to(root_path):
            rel_path = path.relative_to(root_path)
            break

    return rel_path

def readfile(fname):
    "Read a binary file from disk."
    with open(fname, "rb") as stream:
        return stream.read()

def main(args):
    output_folder = Path(args.output_folder) / args.dataset_name
    output_folder = output_folder.parent / caesar_name(output_folder.stem, args.shift, mode="encode")
    filename_prefix = caesar_name(args.dataset_name, args.shift, mode="encode")

    if not Path(output_folder).exists():
        Path(output_folder).mkdir(parents=True)

    if args.input_manifest is None:
        iterator = [{"audio_filepath": path} for path in Path(args.data_root).glob(f"**/*.{args.ext}")]
    else:
        with open(args.input_manifest, "r") as f:
            iterator = [json.loads(line.strip()) for line in f.readlines()]

    tar_name2keys = defaultdict(list)
    with wds.ShardWriter(os.path.join(str(output_folder), f"{filename_prefix}-%06d.tar"), maxcount=args.maxcount, maxsize=args.maxsize) as sink:
        for data in iterator:
            rel_path = extract_rel_path(Path(data["audio_filepath"]), args.data_root)
            file = readfile(data["audio_filepath"])
            audio_id = str(rel_path).replace(rel_path.suffix, "")
            
            data["__key__"] = audio_id
            data["audio_filepath"] = str(rel_path)
            sample = {
                "__key__": audio_id,
                "wav": file,
                "json": json.dumps(data)
            }
            sink.write(sample)
            
            tar_name2keys[sink.pattern % sink.shard].append(data)

    for tar_name, samples in tar_name2keys.items():
        print("processing", tar_name)
        with open(tar_name.replace(".tar", ".jsonl"), "w") as f:
            for sample in samples:
                f.write(json.dumps(sample) + "\n")

if __name__ == "__main__":
    args = parse_args()
    main(args)
