
import argparse
from pathlib import Path
import json
import webdataset as wds
import os
from lulutils.utils.utils import caesar_cipher
from collections import defaultdict
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_manifest", "-i", type=str)
    parser.add_argument("--output_folder", "-o", type=str, required=True)
    parser.add_argument("--data_root", type=str, required=True)
    parser.add_argument("--ext", type=str, default="wav")
    parser.add_argument("--maxcount", type=int, default=100000)
    parser.add_argument("--filename_prefix", type=str, default="output")
    parser.add_argument("--shift", type=int, default=13)
    return parser.parse_args()

def readfile(fname):
    "Read a binary file from disk."
    with open(fname, "rb") as stream:
        return stream.read()

def main(args):
    output_folder = Path(args.output_folder)
    output_folder = output_folder.parent / (output_folder.stem[:3] + caesar_cipher(output_folder.stem[3:], args.shift, mode="encode"))
    filename_prefix = args.filename_prefix[:3] + caesar_cipher(args.filename_prefix[3:], args.shift, mode="encode")

    if not Path(output_folder).exists():
        Path(output_folder).mkdir(parents=True)

    if args.input_manifest is None:
        iterator = [{"audio_filepath": path} for path in Path(args.data_root).glob(f"**/*.{args.ext}")]
    else:
        with open(args.input_manifest, "r") as f:
            iterator = [json.loads(line.strip()) for line in f.readlines()]

    tar_name2keys = defaultdict(list)
    with wds.ShardWriter(os.path.join(str(output_folder), f"{filename_prefix}-%06d.tar"), maxcount=args.maxcount) as sink:
        for data in iterator:
            rel_path = Path(data["audio_filepath"]).relative_to(args.data_root)
            file = readfile(data["audio_filepath"])
            audio_id = str(rel_path).replace(rel_path.suffix, "")
            sample = {
                "__key__": audio_id,
                "wav": file,
            }
        
            sink.write(sample)
            
            data["__key__"] = audio_id
            data["audio_filepath"] = str(rel_path)
            tar_name2keys[sink.pattern % sink.shard].append(data)

    for tar_name, samples in tar_name2keys.items():
        print("processing", tar_name)
        with open(tar_name.replace(".tar", ".jsonl"), "w") as f:
            for sample in samples:
                f.write(json.dumps(sample) + "\n")

if __name__ == "__main__":
    args = parse_args()
    main(args)
