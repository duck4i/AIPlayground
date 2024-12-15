
import qtpynodeeditor as nodeeditor
from qtpynodeeditor.type_converter import TypeConverter
from gui import NumberData, NumberSourceDataModel, NumberTargetDataModel
from gui import StringData, StringSourceDataModel, StringTargetDataModel
from gui import ImageShowModel, ImageLoaderModel, PixmapData
from gui import OpenHermesTargetModel, LLama2TargetModel, LLavaTargetModel, BakllavaTargetModel, QwenSmallTargetModel, Hermes3SmallTargetModel
from gui import string_to_number_converter, number_to_string_converter, string_to_image_converter, image_to_string_converter
from qtpy.QtWidgets import QMainWindow, QToolBar, QAction

class MainWindow():
    def __init__(self, width: int, height: int):
        self.main_window = QMainWindow()
        self.main_window.resize(width, height)
        self.main_window.setWindowTitle("AI Playground")

        [node_graph, node_scene] = self.create_node_graph()
        self.main_window.setCentralWidget(node_graph)

        toolbar = self.create_toolbar(
            window=self.main_window,
            actionNew=lambda: node_scene.clear_scene(),
            actionSave=lambda: node_scene.save(),
            actionLoad=lambda: node_scene.load()
        )
        self.main_window.addToolBar(toolbar)

    def show(self):
        self.main_window.show()

    def create_node_graph(self, style = None):
        registry = nodeeditor.DataModelRegistry()
        scene = nodeeditor.FlowScene(registry, style=style)
        node_graph = nodeeditor.FlowView(scene)
        
        for input in [NumberSourceDataModel, StringSourceDataModel, ImageLoaderModel]:
            registry.register_model(input, category="Inputs", style=style)

        for target in [NumberTargetDataModel, StringTargetDataModel, ImageShowModel]:
            registry.register_model(target, category="Display", style=style)

        for ai in [OpenHermesTargetModel, LLama2TargetModel, QwenSmallTargetModel, Hermes3SmallTargetModel]:
            registry.register_model(ai, "LLMs", style=style)

        for vision in [LLavaTargetModel, BakllavaTargetModel,]:
            registry.register_model(vision, "LLM Vision", style=style)
        
        s_to_num = TypeConverter(StringData.data_type, NumberData.data_type, string_to_number_converter)
        num_to_s = TypeConverter(NumberData.data_type, StringData.data_type, number_to_string_converter)
        img_to_s = TypeConverter(PixmapData.data_type, StringData.data_type, image_to_string_converter)
        #s_to_img = TypeConverter(StringData.data_type, PixmapData.data_type, string_to_image_converter)

        for converter in [s_to_num, num_to_s, img_to_s]:
            registry.register_type_converter(converter.type_in, converter.type_out, converter)

        return node_graph, scene

    def create_toolbar(self, window, actionNew, actionSave, actionLoad):
        toolbar = QToolBar("Main toolbar")
        toolbar.setFixedHeight(40)
        
        new_action = QAction("New", window)
        save_action = QAction("Save", window)
        load_action = QAction("Load", window)

        new_action.triggered.connect(actionNew)
        save_action.triggered.connect(actionSave)
        load_action.triggered.connect(actionLoad)

        toolbar.addAction(new_action)
        toolbar.addSeparator()
        toolbar.addAction(save_action)
        toolbar.addAction(load_action)
        return toolbar
