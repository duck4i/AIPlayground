import typing
from qtpy.QtWidgets import QApplication

class App():
    def __init__(self, args: typing.List[str] = []):
        self.app = QApplication(args)
        pass
    
    def run(self) -> int:
        return self.app.exec()