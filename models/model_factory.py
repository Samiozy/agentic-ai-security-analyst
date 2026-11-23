"""Two real OpenAI-compatible backends: self-hosted Jetstream2 and paid API.

No fake outputs: if credentials or model endpoint are missing, fail explicitly.
Host the open-source model with an OpenAI-compatible endpoint (e.g., Ollama
/v1 or vLLM). Keep model settings and keys outside Git.
"""
import json
import os
import urllib.request

class ModelConfigurationError(RuntimeError): pass

class ChatModel:
    def __init__(self, prefix):
        self.url=os.getenv(prefix+"_BASE_URL", "").rstrip("/")
        self.key=os.getenv(prefix+"_API_KEY", "")
        self.model=os.getenv(prefix+"_MODEL", "")
        self.prefix=prefix
        if not self.url or not self.model:
            raise ModelConfigurationError(f"Set {prefix}_BASE_URL and {prefix}_MODEL in .env")
        if not self.url.startswith(("http://127.0.0.1:","http://localhost:","https://")):
            raise ModelConfigurationError("Model endpoints must use HTTPS or local loopback")
    def complete(self, system, user):
        payload=json.dumps({"model":self.model,"temperature":0,
            "messages":[{"role":"system","content":system},{"role":"user","content":user}]}).encode()
        request=urllib.request.Request(self.url+"/chat/completions",data=payload,
            headers={"Content-Type":"application/json",**({"Authorization":"Bearer "+self.key} if self.key else {})})
        with urllib.request.urlopen(request,timeout=180) as r:
            result=json.load(r)
        return result['choices'][0]['message']['content'],result.get('usage',{})

def get_model(name):
    if name not in ('HOSTED','API'):
        raise ValueError("Choose HOSTED or API")
    return ChatModel(name)
