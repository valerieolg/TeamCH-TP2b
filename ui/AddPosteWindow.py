from PyQt6.QtWidgets import QWidget

class AddPosteWindow(QWidget):
    def __init__(self, poste_data=None, on_save_callback=None):
        super().__init__()