import uvicorn, sys, multiprocessing
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QApplication
from fastapi_app import main
from fastapi_app.models.errors import SiteExistingError


class InitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.correct_host, self.correct_port = '127.0.0.1', '8000'

    def initUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('Signalis')

        self.name = QLabel('Elster theatre', self)
        self.name.setStyleSheet('font-size: 26pt;')
        self.name.resize(self.name.sizeHint())
        self.name.move(300, 100)

        self.working = QLabel(self)
        self.working.move(400, 465)

        self.site_host = QLineEdit(self)
        self.site_host.setText('127.0.0.1:8000')
        self.site_host.move(400, 400)

        self.run_site_button = QPushButton('Apply', self)
        self.run_site_button.resize(self.run_site_button.sizeHint())
        self.run_site_button.move(400, 450)
        self.run_site_button.clicked.connect(self.create_site_process)

    def create_site_process(self):
        self.correct_host, self.correct_port = self.site_host.text().split(':')
        try:
            site = multiprocessing.Process(target=run_site, args=(self.correct_host, int(self.correct_port)))
            site.start()
            self.working.setStyleSheet('color: green')
            self.working.setText('Site successfully raised!')
            self.working.resize(self.name.sizeHint())

        except SiteExistingError:
            self.working.setStyleSheet('color: red')
            self.working.setText(SiteExistingError)
            self.working.resize(self.name.sizeHint())


def run_site(host: str, port: int):
    uvicorn.run(
        'fastapi_app.main:app',
        host=host,
        port=port,
        reload=True,
    )

def create_window():
    app = QApplication(sys.argv)
    ex = InitWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    correct_qt_app = multiprocessing.Process(target=create_window)
    correct_qt_app.start()