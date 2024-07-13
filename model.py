import requests
import os


MODEL_TO_URL = {
    "mistral": "mistralai/Mistral-7B-Instruct-v0.3",
    # "mistral": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "phi_lc": "microsoft/Phi-3-mini-128k-instruct",
    "phi": "microsoft/Phi-3-mini-4k-instruct"
}
MODEL_TO_PROMPT = {
    "phi": "<|user|>\n{summary_prompt}\n{content}<|end|>\n<|assistant|>",
    "phi_lc": "<|user|>\n{summary_prompt}\n{content}<|end|>\n<|assistant|>",
    "mistral": "[INST] {summary_prompt}\n\n[/INST]{content}"
}
API_PREFIX = "https://api-inference.huggingface.co/models/"


class Model:
    def __init__(self, name: str):
        self.name = name
        try:
            self.model_url = self.generate_model_url()
        except ValueError:
            raise ValueError("Model not supported")
        self.qualified_name = MODEL_TO_URL[name]
        self.api_token = os.getenv("HF_API_TOKEN")
        if not self.api_token:
            raise ValueError("Please populate env variable 'HF_API_TOKEN' with the access token")
    
    def generate_model_url(self):
        if self.name not in MODEL_TO_URL:
            raise ValueError
        return API_PREFIX + MODEL_TO_URL[self.name]
        
    def query(self, content, instruction_prompt):
        prompt = MODEL_TO_PROMPT[self.name]
        prompt = prompt.format(summary_prompt = instruction_prompt, content = content)
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 2000,
                "return_full_text": False,
                "num_return_sequences": 1000,
            }
        }
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.post(self.model_url, headers=headers, json=payload)
        if response.status_code == 503:
            print("Waiting for model to load...")
            payload["options"] = {"wait_for_model": True, "use_cache": False}
            response = requests.post(self.model_url, headers=headers, json=payload)
        return response.json()[0]