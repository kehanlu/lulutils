import argparse
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor, pipeline
from datasets import load_dataset, Dataset
from tqdm import tqdm
import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM


HF_TOKEN = os.getenv("HF_TOKEN") # export HF_TOKEN='your_token'

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run ASR")
    
    # Add arguments
    parser.add_argument("--input_jsonl", "-i", help="A jsonl file.", type=str, required=True)
    parser.add_argument("--output_path", "-o", help="output file path. In jsonl format.", type=str, required=True)
    parser.add_argument("--model_id", default="meta-llama/Meta-Llama-3-8B-Instruct", type=str)
    parser.add_argument("--batch_size", default=16, type=int)

    parser.add_argument("--max_new_tokens", default=256, type=int)
    return parser.parse_args()

def split_into_batches(input_list, batch_size):
    return [input_list[i:i + batch_size] for i in range(0, len(input_list), batch_size)]

def main(args):
    tokenizer = AutoTokenizer.from_pretrained(args.model_id, token=HF_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_id,
        torch_dtype=torch.bfloat16, device_map="auto",
        token=HF_TOKEN,
    )

    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"

    datas = [json.loads(line) for line in open(args.input_jsonl).readlines()]
    batches = split_into_batches(datas, args.batch_size)
    
    
    for batch in batches:
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
        )


        for data, output in zip(batch, outputs):
            new_data = {
                "response": tokenizer.decode(output[input_ids.shape[-1]:], skip_special_tokens=True),
            }
            new_data.update(data)

            with open(args.output_path, "a") as fo:
                fo.write(json.dumps(new_data, ensure_ascii=False) + "\n")





if __name__ == "__main__":
    args = parse_arguments()
    main(args)