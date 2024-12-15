import os
from commands import Command
from models import KnownModel, LlavaModelLoader, LLavaChatSession
from utils import console

class CmdLLava(Command):
    
    def __init__(self, question: str, imageFile: str, model: KnownModel, verbose: bool):
        self.question = question
        self.imageFile = imageFile
        self.model = model 
        self.verbose = verbose

    def run(self) -> None:
        super().run()

        if not os.path.exists(self.imageFile):
            raise Exception(f"Image file not found {self.imageFile}")
        
        model = self.select_model(self.model)
        model_path = self.get_model_path(model)
        clip_path = self.get_model_path(model, 1)

        loader = LlavaModelLoader()
        loader.load(model_path, clip_path)

        model = LLavaChatSession(loader)
        
        response = model.answer_with_file(self.question, self.imageFile)
        console.print(f"{response.text}")

