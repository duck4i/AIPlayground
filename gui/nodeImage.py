
import os.path
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtCore import Qt
from qtpynodeeditor import NodeDataModel, PortType
from gui import PixmapData, MainWindowCss
from qtpynodeeditor import NodeValidationState

class ImageLoaderModel(NodeDataModel):
    name = "Image"
    caption = 'Image'
    num_ports = {PortType.input: 0, PortType.output: 1}
    data_type = PixmapData

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pixmap = None
        self._state = NodeValidationState.warning
        self._label = QtWidgets.QLabel('Click to load image')
        self._label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self._label.setStyleSheet(MainWindowCss.css)
        self._label.setFixedSize(200, 200)
        self._label.installEventFilter(self)

    def eventFilter(self, obj, event):
        label = getattr(self, "_label", None)

        if label is None or obj is not label:
            return False

        def set_pixmap():
            w, h = label.width(), label.height()
            label.setPixmap(self._pixmap.scaled(w, h, Qt.KeepAspectRatio))

        if event.type() == QtCore.QEvent.MouseButtonPress:
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
                None, "Open Image", None,
                "Image files (*.png *.jpg *.bmp)")
            try:
                if os.path.isfile(file_name):
                    self._pixmap = QtGui.QPixmap(file_name)
                    set_pixmap()
                    self.data_updated.emit(0)
                    self._state = NodeValidationState.valid
                else:
                    raise Exception("Action canceled.")
            except Exception as ex:
                print(f'Failed to load image {file_name}: {ex}')
                return False
            return True

        elif event.type() == QtCore.QEvent.Resize:
            if self._pixmap is not None:
                set_pixmap()

        return False

    def resizable(self):
        return True

    def out_data(self, port):
        return PixmapData(self._pixmap)

    def validation_state(self) -> NodeValidationState:
        return self._state
    
    def validation_message(self) -> str:
        return "Missing input"
    
    def embedded_widget(self):
        return self._label


class ImageShowModel(NodeDataModel):
    name = "Image Display"
    caption = 'Image Display'
    caption_visible = True
    num_ports = { PortType.input: 1, PortType.output: 1 }
    data_type = PixmapData

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._node_data = None
        self._label = QtWidgets.QLabel('Image will appear here')
        self._label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self._label.setStyleSheet(MainWindowCss.css)
        self._label.setFixedSize(200, 200)
        self._label.installEventFilter(self)

    def resizable(self):
        return True

    def eventFilter(self, obj, event):
        if obj is self._label and event.type() == QtCore.QEvent.Resize:
            if (self._node_data and
                    self._node_data.data_type == PixmapData.data_type and
                    self._node_data.pixmap):
                w, h = self._label.width(), self._label.height()
                pixmap = self._node_data.pixmap
                self._label.setPixmap(pixmap.scaled(w, h, Qt.KeepAspectRatio))

        return False

    def set_in_data(self, node_data, port):
        self._node_data = node_data
        if (self._node_data and
                self._node_data.data_type == PixmapData.data_type and
                self._node_data.pixmap):
            w, h = self._label.width(), self._label.height()
            pixmap = node_data.pixmap.scaled(w, h, Qt.KeepAspectRatio)
        else:
            pixmap = None

        self._label.setPixmap(pixmap)
        self.data_updated.emit(0)

    def out_data(self, port):
        return self._node_data

    def embedded_widget(self):
        return self._label

