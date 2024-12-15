from threading import RLock
from qtpynodeeditor.node_data import NodeData, NodeDataType

class LockableData(NodeData):
    def __init__(self) -> None:
        self._lock = RLock()

    @property
    def lock(self):
        return self._lock


class NumberData(LockableData):
    data_type = NodeDataType("float", "Number")

    def __init__(self, number: int = 0):
        self._number = number
    
    @property
    def value(self) -> int:
        return self._number


class StringData(LockableData):
    data_type = NodeDataType("string", "Text")

    def __init__(self, value: str = ""):
        self._value = value

    @property
    def value(self) -> str:
        return self._value


class PixmapData(LockableData):
    data_type = NodeDataType(id='pixmap', name='Pixmap')

    def __init__(self, pixmap = None):
        self.pixmap = pixmap
