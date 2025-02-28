
import argparse
from pathlib import Path
import json
import webdataset as wds
import os
from lulutils import caesar_name
from collections import defaultdict
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_manifest", "-i", type=str, help="Input manifest file")
    parser.add_argument("--dataset_name", "-n", type=str, required=True, help="Dataset name")
    parser.add_argument("--output_folder", "-o", type=str, required=True, help="Output folder")
    parser.add_argument("--data_root", type=str, nargs="+", required=True, help="Data root")
    parser.add_argument("--ext", type=str, default="wav", help="Extension of the audio file")
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
    """
    This script creates webdataset shards from a manifest file or from a data root.
    
    Example (if you have a prepared manifest file with audio_filepath and metadata):

    manifest.jsonl:
    ```JSONL
    {"audio_filepath": "/path/to/data_root/audio.wav", "duration": 1.0, "emotion": "happy"}
    {"audio_filepath": "/path/to/data_root/audio2.wav", "duration": 2.0, "emotion": "sad"}
    ```
    
    ```bash
    python create_shards_from_manifest.py \
        -i /path/to/manifest.jsonl \
        -n cool_dataset \
        -o /path/to/output_folder \
        --data_root /path/to/data_root
    ```


    Example (if you want to create audio_filepath from data root, without any metadata):
    
    ```bash
    python create_shards_from_manifest.py \
        --data_root /path/to/data_root \
        --ext wav \
        -n cool_dataset \
        -o /path/to/output_folder \
    ```

    """
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


    # check all lines are valid
    data_keys = set(iterator[0].keys())
    for data in iterator:
        # check if all data have same keys
        if data.get("audio_filepath") is None:
            raise ValueError(f"File {data['audio_filepath']} does not have audio_filepath key")
        
        # check if all data have same keys
        if set(data.keys()) != data_keys:
            raise ValueError(f"File {data['audio_filepath']} has different keys")
        
        # check if not absolute path
        if not Path(data["audio_filepath"]).is_absolute():
            raise ValueError(f"File {data['audio_filepath']} is not an absolute path")

        # check if file exists
        if not Path(data["audio_filepath"]).exists():
            raise FileNotFoundError(f"File {data['audio_filepath']} does not exist")
        
        # check all files comes from one of the data_root
        for root in args.data_root:
            if Path(data["audio_filepath"]).is_relative_to(Path(root)):
                break
        else:
            raise ValueError(f"File {data['audio_filepath']} is not in any of the data_root")
        

    # sort by audio_filepath    
    iterator = sorted(iterator, key=lambda x: x["audio_filepath"])
    
    # Write to shards in webdataset format
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
            tar_name2keys[sink.fname].append(data)

    # Write to jsonl
    # (this is additional text-based information for better understanding of the dataset without downloading the whole webdataset)
    for tar_name, samples in tar_name2keys.items():
        print("Processing", tar_name)
        jsonl_name = tar_name.replace(".tar", ".jsonl")
        print("Writing", jsonl_name)
        with open(jsonl_name, "w") as f:
            for sample in samples:
                f.write(json.dumps(sample) + "\n")

if __name__ == "__main__":
    args = parse_args()
    main(args)
