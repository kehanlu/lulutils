import argparse
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor, pipeline
from datasets import load_dataset, Dataset
from tqdm import tqdm
import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm

from lulutils.check_filename import check_filename

HF_TOKEN = os.getenv("HF_TOKEN") # export HF_TOKEN='your_token'

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run Llama generation. Just prepare your \"messages\".")
    
    # Add arguments
    parser.add_argument("--input_jsonl", "-i", help="A jsonl file.", type=str, required=True)
    parser.add_argument("--output_path", "-o", help="output file path. In jsonl format.", type=str, required=True)
    parser.add_argument("--model_id", default="meta-llama/Meta-Llama-3-8B-Instruct", type=str)
    parser.add_argument("--batch_size", default=16, type=int)

    parser.add_argument("--temperature", default=1, type=float)
    parser.add_argument("--top_p", default=1, type=float)
    parser.add_argument("--max_new_tokens", default=256, type=int)
    parser.add_argument("--do_sample", default=True, type=bool)

    parser.add_argument("--cache_dir", default=None, type=str, help="Directory to store the pretrained models downloaded from huggingface.co")
    return parser.parse_args()

def split_into_batches(input_list, batch_size):
    return [input_list[i:i + batch_size] for i in range(0, len(input_list), batch_size)]

def main(args):
    tokenizer = AutoTokenizer.from_pretrained(args.model_id, token=HF_TOKEN, cache_dir=args.cache_dir)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_id,
        torch_dtype=torch.bfloat16, device_map="auto",
        token=HF_TOKEN,
        cache_dir=args.cache_dir
    )

    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"

    datas = [json.loads(line) for line in open(args.input_jsonl).readlines()]
    batches = split_into_batches(datas, args.batch_size)
    
    output_path = check_filename(args.output_path)
    with open(output_path, "a") as fo:
        for batch in tqdm(batches):
            batch_messages = [data["messages"] for data in batch]
            input_ids = tokenizer.apply_chat_template(
                batch_messages, add_generation_prompt=True, return_tensors="pt", padding=True
            ).to(model.device)

            outputs = model.generate(
                input_ids,
                max_new_tokens=args.max_new_tokens,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.eos_token_id,
                attention_mask=None,
                do_sample=args.do_sample,
                temperature=args.temperature,
                top_p=args.top_p,
            )


            for data, output in zip(batch, outputs):
                new_data = {
                    "response": tokenizer.decode(output[input_ids.shape[-1]:], skip_special_tokens=True),
                }
                new_data.update(data)

                fo.write(json.dumps(new_data, ensure_ascii=False) + "\n")

    print(f"Done! Results are saved to\n\n {output_path}")



if __name__ == "__main__":
    args = parse_arguments()
    main(args)