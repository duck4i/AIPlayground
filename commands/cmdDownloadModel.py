from commands import Command
from models.utils import ModelDownloader
from models.knownModel import KnownModel
from utils import console, promptIntRange

class CmdDownloadModel(Command):
    def __init__(self, model: KnownModel):
        self.model = model
    
    def run(self) -> None:
        super().run()

        if (self.model == KnownModel.none):
            self.model = ModelDownloader().selectModel()

        console.print(f"Model selected: {self.model}")
        ModelDownloader().downloadModel(self.model)
