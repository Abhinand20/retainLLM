import requests
import os
import google.generativeai as genai
import warnings
warnings.filterwarnings('ignore')


HF_MODEL_TO_URL = {
    "mistral": "mistralai/Mistral-7B-Instruct-v0.3",
    "phi_lc": "microsoft/Phi-3-mini-128k-instruct",
    "phi": "microsoft/Phi-3-mini-4k-instruct"
}

class BaseModel:
    def __init__(self, name: str, system_prompt: str | None):
        self.name = name
        self.api_token = self.get_api_token()
        self.system_prompt = system_prompt
        self.qualified_name = name

    def get_api_token(self):
        raise NotImplementedError

    def query(self, content):
        raise NotImplementedError

class GeminiModel(BaseModel):
    _generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
        
    def __init__(self, name: str, system_prompt: str | None):
        super().__init__(name=name, system_prompt=system_prompt)
        genai.configure(api_key=self.api_token)
        self.qualified_name="gemini-1.5-flash"
        self.model = genai.GenerativeModel(
            model_name=self.qualified_name,
            generation_config=self._generation_config,
            system_instruction=system_prompt
        )
    
    def get_api_token(self):
        api_token = os.getenv("GEMINI_API_TOKEN")
        if not api_token:
            raise ValueError("Please populate env variable 'GEMINI_API_TOKEN' with the access token")
        return api_token
    
    def query(self, content):
        response = self.model.generate_content(content)
        return response.text
    
class HuggingFaceModel(BaseModel):
    _api_prefix = "https://api-inference.huggingface.co/models/" 
    _model_to_prompt = {
        "phi": "<|user|>\n{summary_prompt}\n{content}<|end|>\n<|assistant|>",
        "phi_lc": "<|user|>\n{summary_prompt}\n{content}<|end|>\n<|assistant|>",
        "mistral": "[INST] {summary_prompt}\n\n[/INST]{content}"
    }
    
    def __init__(self, name, system_prompt):
        super().__init__(name=name, system_prompt=system_prompt)
        self.qualified_name=HF_MODEL_TO_URL[name]
        
    def get_api_token(self):
        api_token = os.getenv("HF_API_TOKEN")
        if not api_token:
            raise ValueError("Please populate env variable 'HF_API_TOKEN' with the access token")
        return api_token
        
    def generate_model_url(self):
        if self.name not in HF_MODEL_TO_URL:
            raise ValueError
        return self._api_prefix + HF_MODEL_TO_URL[self.name]
        
    def query(self, content):
        prompt = self._model_to_prompt[self.name]
        prompt = prompt.format(summary_prompt = self.system_prompt, content = content)
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 2000,
                "return_full_text": False,
                "num_return_sequences": 1000,
            }
        }
        headers = {"Authorization": f"Bearer {self.api_token}"}
        model_url = self.generate_model_url()
        response = requests.post(model_url, headers=headers, json=payload)
        if response.status_code == 503:
            print("Waiting for model to load...")
            payload["options"] = {"wait_for_model": True, "use_cache": False}
            response = requests.post(self.model_url, headers=headers, json=payload)
        return response.json()[0]['generated_text']

def model_factory(model_name: str, system_prompt: str) -> BaseModel:
    if model_name in HF_MODEL_TO_URL:
        return HuggingFaceModel(model_name, system_prompt)
    if model_name.lower().startswith('gemini'):
        return GeminiModel(model_name, system_prompt)
    
    raise NotImplementedError("Model type {} not implemented.".format(model_name))