from enum import Enum

class KnownModel(str, Enum):
    none = None,
    openHermes = "OpenHermes",
    llama7b = "LLaMA",
    llava1pt57b = "LLaVA",
    llava1pt513b = "LLaVA13",
    bakllava = "BakLLaVA",
    qwen2pt5500m = "Qwen25Small"
    hermes33pt5 = "Hermes3Small",
    hermesVision = "HermesVision",
    codeLlama7b = "CodeLLaMA",
    leetCode7b = "LeetCodeWizard",
    

