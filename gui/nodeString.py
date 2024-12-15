# Nodes
from gui import StringData, MainWindowCss
from qtpynodeeditor.enums import NodeValidationState
from qtpynodeeditor.node_data import NodeData
from qtpynodeeditor import (NodeData, NodeDataModel, NodeDataType, NodeValidationState, Port, PortType)
from qtpy.QtWidgets import QPlainTextEdit, QWidget

class StringSourceDataModel(NodeDataModel):
    name = "Text"
    caption_visible = True
    num_ports = { PortType.input: 0, PortType.output : 1 }
    data_type = StringData.data_type

    def __init__(self, style=None, parent=None):
        super().__init__(style=style, parent=parent)
        self._value = None 
        self._widget = QPlainTextEdit()
        self._widget.setStyleSheet(MainWindowCss.css)
        self._widget.setMaximumSize(self._widget.sizeHint())
        self._widget.textChanged.connect(self.on_text_edited)
        self._widget.setPlainText("")
    
    def on_text_edited(self):
        self._value = StringData(self._widget.toPlainText())
        self.data_updated.emit(0)
    
    def out_data(self, port: int) -> NodeData:
        return self._value
    
    def embedded_widget(self) -> QWidget:
        return self._widget

    def save(self) -> dict:
        doc = super().save()
        if self._value:
            doc["text"] = self._value.value
        return doc
    
    def restore(self, state: dict) -> None:
        try:
            tmp = state["text"]
        except Exception:
            ...
        else:
            self._value = StringData(tmp)
            self._widget.setPlainText(self._value.value)


class StringTargetDataModel(NodeDataModel):
    name = "Text Display"
    caption_visible = True
    num_ports = { PortType.input: 1, PortType.output : 1}
    data_type = StringData.data_type

    def __init__(self, style=None, parent=None):
        super().__init__(style=style, parent=parent)
        self._value = None
        self._output = None
        self._state = NodeValidationState.warning
        self._widget = QPlainTextEdit()
        self._widget.setStyleSheet(MainWindowCss.css)
        self._widget.setMaximumSize(self._widget.sizeHint())
        self._widget.setReadOnly(True)

    def set_in_data(self, node_data: NodeData, port: Port):
        self._value = node_data
        self._output = node_data
        if self._value is not None:
            self._state = NodeValidationState.valid
            self._widget.setPlainText(self._value.value)
        else:
            self._state = NodeValidationState.warning
            self._widget.setPlainText("")

        self.data_updated.emit(0)
        self._widget.adjustSize()

    def out_data(self, port: int) -> NodeData:
        return self._output

    def validation_state(self) -> NodeValidationState:
        return self._state
    
    def validation_message(self) -> str:
        return "Missing input"
    
    def resizable(self) -> bool:
        return True
    
    def embedded_widget(self) -> QWidget:
        return self._widget
