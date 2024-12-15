from utils import log
from models import KnownModel
from models.utils import ModelDownloader

class Command():
    def run(self) -> None:
        log.debug(f"Starting command {self}")
        pass

    def select_model(self, model: KnownModel) -> KnownModel:
        downloader = ModelDownloader()
        if model == KnownModel.none:
            nm = downloader.selectModel() # < -- selects the model by prompting user
            downloader.downloadModel(nm)
            return nm
        return model

    def get_model_path(self, model: KnownModel, fileIndex: int = 0) -> str:
        downloader = ModelDownloader()
        model = self.select_model(model)
        return downloader.getPath(model, fileIndex)