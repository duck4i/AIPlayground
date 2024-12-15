from llama_cpp import Llama

class ModelLoader():
    def load(self, modelPath: str) -> bool:
        ...

    def model(self) -> Llama:
        ...