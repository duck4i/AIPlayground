from commands import Command
from utils import log, console, promptText
from models import KnownModel, LlamaModelLoader, LLamaChatSession

class CmdLlama(Command):
    def __init__(self, model: KnownModel, question: str, chatMode: bool, verbose = False):
        self.model = model
        self.question = question
        self.chatMode = chatMode
        self.verbose = verbose

    def run(self) -> None:
        super().run()

        log.debug(f"Model: {self.model}")
        log.debug(f"Question: {self.question}")

        file_path = self.get_model_path(self.model)
        
        model = LlamaModelLoader(verbose=self.verbose)
        engine = LLamaChatSession(model, streamFunction=self.chatStreamFunction)

        with console.status(f"Loading model... {file_path}") as status:
            log.info(f"Loading model {file_path}...")
            model.load(file_path)
            log.info(f"Model loaded.")
    
        while True:
            log.info(f"Generating answer...")
            answer = engine.answer(question=self.question)
            console.print(answer.text, new_line_start=True)
        
            if not self.chatMode:
                break
            
            self.question = promptText("Question", default="exit")
            if self.question == "exit" or self.question is None:
                break
    
    def chatStreamFunction(self, text: str) -> None:
        if self.chatMode:
            console.print(text, end="")


