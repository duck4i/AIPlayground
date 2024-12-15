
from commands import Command
from gui import App, MainWindow

class CmdShowUI(Command):
    def __init__(self):
        self.app = App()
        self.window = MainWindow(width=2556, height=1400)

    def run(self) -> None:
        self.window.show()
        self.app.run()