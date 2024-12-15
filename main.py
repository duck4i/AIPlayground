from __init__ import __version__
import typer
import logging
from models import KnownModel
from commands import CmdLlama, CmdDownloadModel, CmdLLava

app = typer.Typer()

def menu_main():
    @app.command(help="Prints CLI app version.")
    def version():
        print(f"{__version__}")

    @app.command(name="download", help="Download the models")
    def downloadModel(model: KnownModel = KnownModel.none):
        CmdDownloadModel(model).run()


def menu_llama():
    llms = typer.Typer()
    app.add_typer(llms, name="llama", help="LLaMA based models loader")

    @llms.command(name="run", help="Single pass inference for LLAMA")
    def run_llama(question:str, model: KnownModel = KnownModel.none, verbose: bool = False):
        CmdLlama(model=model, question=question, chatMode=False, verbose=verbose).run()

    @llms.command(name="chat", help="Chat with LLAMA")
    def chat_llama(question:str, model: KnownModel = KnownModel.none, verbose: bool = False):
        CmdLlama(model=model, question=question, chatMode=True, verbose=verbose).run()

def menu_llava():
    llmv = typer.Typer()
    app.add_typer(llmv, name="llava", help="LLaVA family of models")

    @llmv.command(name="run", help="Run image inference for LLaVA")
    def run_llava(question: str, image=str, model: KnownModel = KnownModel.none, verbose: bool = False):
        CmdLLava(question, image, model, verbose).run()

def menu_ui():
    ui = typer.Typer()
    app.add_typer(ui, name="UI", help="Show UI")

    @ui.command(name="show", help="Displays main window")
    def show_ui():
        from commands.cmdShowUI import CmdShowUI
        CmdShowUI().run()


#   API ENTRY
if __name__ == "__main__":
    menu_main()
    menu_llama()
    menu_llava()
    menu_ui()
    app()   # run