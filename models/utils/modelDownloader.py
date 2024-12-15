import os
from models.knownModel import KnownModel
from models.utils import ModelRegistry
from utils import console, promptIntRange
from rich.progress import Progress
from rich.table import Table

class ModelDownloader():
    temp_directory = "model_data"

    def __init__(self):
        os.makedirs(self.temp_directory, exist_ok=True)

    def downloadModel(self, model: KnownModel) -> bool:
        import requests # throws a warning on import, only import when using it 

        modelInfo = ModelRegistry.models[model]
        
        try:
            block_size = 1024
            filesSuccess =  0

            index = 0
            for file in modelInfo.files:
                model_filepath = self.getPath(model, index)
                index += 1

                response = requests.get(file, stream=True)
                total_length = int(response.headers.get('content-length'))

                if os.path.exists(model_filepath):
                    if os.path.getsize(model_filepath) == total_length:
                        console.print(f"File {index} for model '{model}' is already downloaded.")
                        continue

                with Progress(console=console) as progress:
                    download = progress.add_task(f"Downloading file {index} for {model.value}...", total=total_length)

                    with open(model_filepath, "wb") as model_file:
                        for data in response.iter_content(chunk_size=block_size):
                            progress.update(download, advance=len(data))
                            model_file.write(data)
                            model_file.flush()
                            filesSuccess += 1
 
            if filesSuccess == modelInfo.files:
                console.print(f"Model '{model}' downloaded successfully to {model_filepath}")
                return True
            
            return False

        except Exception as e:
            console.print(f"Failed to download model '{model}' - {e}")
            return False

    def getPath(self, model: KnownModel, fileIndex: int = 0) -> str:
        return  os.path.join(ModelDownloader.temp_directory, f"{model}.{fileIndex}.llm")
    
    def isDownloaded(self, model: KnownModel) -> bool:
        return os.path.exists(self.getPath(model))
    
    def selectModel(self) -> KnownModel:
        console.print()

        table = Table(title="Available models")
        table.add_column("Id", justify="left")
        table.add_column("Name", justify="left")
        table.add_column("Description", justify="full")

        total = 0
        for model in ModelRegistry.models:
            table.add_row(f"{total}", f"{model.value}", f"{ModelRegistry.models[model].description}")
            total = total+1
    
        console.print(table)

        modelIndex = promptIntRange("Select model", 0, len(ModelRegistry.models)-1)
        return list(ModelRegistry.models.keys())[modelIndex]
 