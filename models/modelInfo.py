from enum import Enum

class ModelFamily(str, Enum):
    none = None,
    llama = "LLaMA",
    llava = "LLaVA",
    mistral = "Mistral"
    qwen = "Qwen"

class ModelInfo():
    def __init__(self, description: str, family: ModelFamily, files: list):
        self.description = description
        self.family = family
        self.files = files