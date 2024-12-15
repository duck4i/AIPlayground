from gui import NumberData, MainWindowCss
from qtpynodeeditor import NodeData, NodeDataModel, NodeValidationState, Port, PortType
from qtpy.QtGui import QDoubleValidator
from qtpy.QtWidgets import QLabel, QLineEdit, QWidget

class NumberSourceDataModel(NodeDataModel):
    name = "Number"
    caption_visible = True
    num_ports = { PortType.input: 0, PortType.output: 1 }
    data_type = NumberData.data_type

    def __init__(self, style=None, parent=None):
        super().__init__(style=style, parent=parent)
        self._number = None
        self._state = NodeValidationState.warning
        self._widget = QLineEdit()
        self._widget.setStyleSheet(MainWindowCss.css)
        self._widget.setValidator(QDoubleValidator())
        self._widget.setMaximumSize(self._widget.sizeHint())
        self._widget.textChanged.connect(self.on_text_edited)
        self._widget.setText("0.0")

    def save(self) -> dict:
        doc = super().save()
        if self._number is not None:
            doc["number"] = self._number.value
        return doc

    def restore(self, state: dict):
        try:
            value = float(state["number"])
        except Exception:
            ...
        else:
            self._number = NumberData(value)
            self._widget.setText(f"{self._number.value}")

    def out_data(self, port: int) -> NodeData:
        return self._number

    def embedded_widget(self) -> QWidget:
        'The number source has a line edit widget for the user to type in'
        return self._widget
    
    def validation_state(self) -> NodeValidationState:
        return self._state
    
    def validation_message(self) -> str:
        return "Not a valid number"

    def on_text_edited(self, string: str):
        try:
            number = float(self._widget.text())
            self._state = NodeValidationState.valid
        except ValueError:
            self._state = NodeValidationState.warning
            self.data_invalidated.emit(0)
        else:
            self._number = NumberData(number)
            self.data_updated.emit(0)

class NumberTargetDataModel(NodeDataModel):
    name = "Number Display"
    caption_visible = True
    num_ports = { PortType.input : 1, PortType.output : 1}
    data_type = NumberData.data_type

    def __init__(self, style=None, parent=None):
        super().__init__(style=style, parent=parent)
        self._value = None 
        self._output = None
        self._state = NodeValidationState.warning
        self._widget = QLabel()
        self._widget.setStyleSheet(MainWindowCss.css)

    def embedded_widget(self) -> QWidget:
        return self._widget

    def set_in_data(self, node_data: NodeData, port: Port):
        self._value = node_data
        self._output = node_data
        if node_data is not None:
            self._state = NodeValidationState.valid
            self._widget.setText(f"{self._value.value}")
        else:
            self._state = NodeValidationState.warning
            self._widget.setText("")

        self.data_updated.emit(0)
        self._widget.adjustSize()

    def out_data(self, port: int) -> NodeData:
        return self._output

    def validation_state(self) -> NodeValidationState:
        return self._state
    
    def validation_message(self) -> str:
        return "Missing input"

