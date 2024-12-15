from qtpy import QtCore, QtGui
from gui import StringData, NumberData, PixmapData

def string_to_number_converter(data: StringData) -> NumberData:
    try:
        return NumberData(float(data.value))
    except Exception:
        return None

def number_to_string_converter(data: NumberData) -> StringData:
    return StringData(f"{data.value}")

def image_to_string_converter(data: PixmapData) -> StringData:
    if data is not None and data.pixmap is not None:
        img = data.pixmap.toImage()
        ba = QtCore.QByteArray()
        buff = QtCore.QBuffer(ba)
        buff.open(QtCore.QIODevice.WriteOnly)
        img.save(buff, "PNG")
        import base64
        v = base64.b64encode(buff.data().data())
        return StringData(str(v, "utf-8"))
    return None

def string_to_image_converter(data: StringData) -> PixmapData:
    "TODO: this is not working"
    import base64
    by = base64.b64decode(data.value)
    ba = QtCore.QByteArray(by)
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(ba)
    return PixmapData(pixmap)
