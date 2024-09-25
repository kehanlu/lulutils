
import argparse
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor, pipeline
from datasets import load_dataset, Dataset
from tqdm import tqdm
import json

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run ASR")
    
    # Add arguments
    parser.add_argument("--input_filelist", "-i", help="input filelist. A txt file, each line contains absolute audio filepath.", type=str, required=True)
    parser.add_argument("--output_path", "-o", help="output file path. In jsonl format.", type=str, required=True)
    parser.add_argument("--whisper_id", default="openai/whisper-large-v3", type=str)
    parser.add_argument("--batch_size", default=16, type=int)
    return parser.parse_args()


def main(args):
    print(args)

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = args.whisper_id

    model = WhisperForConditionalGeneration.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True,
    )
    model.to(device)
    processor = WhisperProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        chunk_length_s=30,
        batch_size=args.batch_size,
        return_timestamps=False,
        torch_dtype=torch_dtype,
        device=device,
    )

    filelist = [{"path": line.strip()} for line in open(args.input_filelist).readlines()]

    dataset = Dataset.from_list(filelist)

    def iterate_data(dataset):
        for i, item in enumerate(dataset):
            yield item["path"]


    for path, out in tqdm(zip(iterate_data(dataset), pipe(iterate_data(dataset), batch_size=args.batch_size, return_timestamps=True))):
        
        with open(args.output_path, "a") as fo:
            fo.write(json.dumps(
                {"path": str(path), "text": out["text"].strip(), "chunks": out["chunks"]}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    args = parse_arguments()
    main(args)