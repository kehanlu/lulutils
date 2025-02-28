from transformers import AutoTokenizer, MllamaForCausalLM, MllamaForMaskedLM
import torch
import os



class LlmWrapper():
    def __init__(self, model_id, device, cache_dir=None):
        if cache_dir is None:
            cache_dir = os.getenv("HF_HOME")

        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = MllamaForCausalLM.from_pretrained(model_id, device_map=device, torch_dtype=torch.bfloat16, cache_dir=cache_dir)
        self.tokenizer.padding_side = "left"

    def generate(self, input_ids):
        pass
        