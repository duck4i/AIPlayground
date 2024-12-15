from utils import log
from commands import Command
from models import LlavaModelLoader, LLavaChatSession, LLMResponse, KnownModel
from models.utils import ModelDownloader
from gui import StringData, MainWindowCss
from qtpynodeeditor.node_data import NodeData
from qtpynodeeditor import NodeData, NodeDataModel, NodeDataType, NodeValidationState, Port, PortType
from qtpy.QtWidgets import QPlainTextEdit, QWidget, QFrame
from qtpy.QtCore import QObject, QThread, Signal, QRunnable, QThreadPool
from .nodeLLM import ModelSingleton, ThreadPoolSingleton, LlamaWorkerSignals

class LlavaWorker(QRunnable):
    def __init__(self, question: str, system: str, image_content:str, model: KnownModel = KnownModel.llava1pt57b):
        super(LlavaWorker, self).__init__()
        log.debug(f"{self} Worker created...")
        self.signals = LlamaWorkerSignals()
        self._session = None
        self._question = question
        self._system = system
        self._image = image_content
        self._canceled = False
        self._model = model

    def run(self):
        if not self._canceled:
            log.info(f"{self} Generating answer...")
            self.signals.started.emit()
            question = self._question
            if self._system is not None:
                question = f"{self._system}\n{question}"
            self._session = LLavaChatSession(ModelSingleton().instance(self._model), tokens=512)#, streamFunction=self._on_chunk_recieved)
            response = self._session.answer(question, image_content_base64=self._image)
            if not self._canceled:
                log.info(f"{self} Done...")
                self.signals.response_generated.emit(response.text)
            else:
                log.info(f"{self} Canceled...")
        self.signals.finished.emit()

    def cancel(self):
        log.debug(f"{self} Job canceled. {self}")
        if self._session is not None:
            self._session.cancel()
        self._canceled = True

    def _on_chunk_recieved(self, text: str):
        self.signals.chunk_recieved.emit(text)


class LlavaTargetDataModel(NodeDataModel):
    caption_visible = True
    num_ports = { PortType.input : 3, PortType.output: 1}
    port_caption = {
        "input": {0: "Image", 1: "System", 2: "Question"},
        "output": {0 : StringData.data_type.name},
    }
    port_caption_visible = True
    data_type = StringData.data_type

    def __init__(self, model: KnownModel, style=None, parent=None):
        super().__init__(style, parent)
        self._value = None
        self._model = model
        self._system_message = None
        self._image = None
        self._output = None
        self._state = NodeValidationState.error
        self._widget = QPlainTextEdit()
        self._widget.setStyleSheet(MainWindowCss.css)
        self._widget.setMaximumSize(self._widget.sizeHint())
        self._widget.setReadOnly(True)
        self._worker = None

    def refresh_ai(self) -> bool:
        if self._value is None or self._image is None:
            log.warn("input values null...")
            return False
        
        self._state = NodeValidationState.warning
        
        sysm = None 
        if self._system_message is not None and self._system_message.value:
            sysm = self._system_message.value

        self._worker = LlavaWorker(self._value.value, system=sysm, image_content=self._image.value, model=self._model)
        self._worker.signals.started.connect(self.on_llm_started)
        self._worker.signals.response_generated.connect(self.on_llm_finished)
        self._worker.signals.chunk_recieved.connect(self.on_llm_chunk_recieved)
        ThreadPoolSingleton().instance().start(self._worker)
    
    def on_llm_started(self):
        log.debug(f"{self} on_llm_started signal...")
        self._widget.setPlainText("")
        self._output = None
        self._state = NodeValidationState.warning
        self.data_updated.emit(0)

    def on_llm_chunk_recieved(self, result: str):
        plain = self._widget.toPlainText()
        plain += result
        self._widget.setPlainText(plain)
        self._widget.adjustSize()

    def on_llm_finished(self, result: str):
        log.debug(f"{self} on_llm_finished signal...")
        if not result:
            return
        self._output = StringData(result)
        self._widget.setPlainText(result)
        self._widget.adjustSize()
        self._state = NodeValidationState.valid
        self.data_updated.emit(0)

    def set_error(self):
        self._state = NodeValidationState.error
        self._widget.setPlainText("")
        self._output = None
    
    def set_in_data(self, node_data: NodeData, port: Port):
        if self._worker is not None:
            self._worker.cancel()
        if port.index == 0:
            self._image = node_data
            if self._image is not None:
                self.refresh_ai()
            else:
                self.set_error()
        if port.index == 1:
            self._system_message = node_data
            self.refresh_ai()
        if port.index == 2:
            self._value = node_data
            if self._value is not None:
                self.refresh_ai()
            else:
                self.set_error()
        self.data_updated.emit(0)

    def out_data(self, port: int) -> NodeData:
        return self._output
    
    def validation_state(self) -> NodeValidationState:
        return self._state
    
    def validation_message(self) -> str:
        if self._state == NodeValidationState.error:
            return "Missing input"
        else:
            if not self._value or not self._value.value:
                return "Empty input..."
        return "Running inference..."
    
    def resizable(self) -> bool:
        return True

    def embedded_widget(self) -> QWidget:
        return self._widget


class LLavaTargetModel(LlavaTargetDataModel):
    name = "LLaVA 1.5 7B 4bit"
    caption = name
    def __init__(self, style=None, parent=None):
        super().__init__(KnownModel.llava1pt57b, style, parent)

class BakllavaTargetModel(LlavaTargetDataModel):
    name = "BaKLLaVA 1.0 7B 4bit"
    caption = name
    def __init__(self, style=None, parent=None):
        super().__init__(KnownModel.bakllava, style, parent)
