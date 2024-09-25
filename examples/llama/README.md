## Run llama3 generation

- `--input_jsonl`, `-i` (required): Path to the input JSONL file.
- `--output_path`, `-o` (required): Path for the output JSONL file.
- `--model_id` (optional): ID of the LLM model to use. Default: "meta-llama/Meta-Llama-3-8B-Instruct"
- `--batch_size` (optional): Number of items to process in each batch. Default: 16
- `--max_new_tokens` (optional): Maximum number of new tokens to generate. Default: 256

```
python examples/llama/run_llama3_generation.py -i examples/llama/llama3_input.jsonl -o examples/llama/outputs.jsonl --batch_size 32 --max_new_tokens 512
```


## Input and output format
- Input: JSONL
  - messages(required)
  - other keys
- Output: JSONL
  - response
  - Other keys from input jsonl

```
{"id": "1", "messages": [{"role": "system", "content": "You are a helpful AI."}, {"role": "user", "content": "Who are you?"}]}
```