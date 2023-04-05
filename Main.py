from Pdf_to_csv import pdf_to_csv
import os
import sys
from PyQt5.QtWidgets import QApplication,  QFileDialog, QWidget, QGridLayout, QListWidget, QPushButton, QLabel, QMessageBox
from pathlib import Path



# input('Нажмите ENTER чтобы начать')

# def main():


#     files_in_dir = os.listdir(r"requests")

#     for file in files_in_dir:
#         print(f'Файл {file} найден, начинаю обработку...')
#         pdf_to_csv(file)

#     print()    
#     print(f'Обработано {len(files_in_dir)} файлов')

#     input('Готово, нажмите ENTER, чтобы закрыть окно')

# if __name__ == '__main__':
#     main()


class MainWindow(QWidget):

    filelist = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Zapros reader')
        self.setGeometry(100, 100, 400, 100)

        layout = QGridLayout()
        self.setLayout(layout)

        # file selection
        self.file_browse = QPushButton('Выбрать файлы')
        self.file_browse.clicked.connect(self.open_file_dialog)

        self.run_files_btn = QPushButton('Запустить обработку')
        self.run_files_btn.setDisabled(True)
        self.run_files_btn.clicked.connect(self.run_files)

        self.file_list = QListWidget(self)

        layout.addWidget(QLabel('Выбранные файлы:'), 0, 0)
        layout.addWidget(self.file_list, 1, 0)
        layout.addWidget(self.file_browse, 2, 0)
        layout.addWidget(self.run_files_btn, 3, 0)

        self.show()
    
    
    def open_file_dialog(self):
        global filelist
        self.run_files_btn.setDisabled(False)
        
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            r"requests",
            "PDF (*.pdf)"
        )
        if filenames:
            self.file_list.addItems( [str(Path(filename)) for filename in filenames] )
            filelist = filenames     
                 
    def run_files(self, filenames):
        global filelist
        filenames = filelist   
        
        self.run_files_btn.setDisabled(True)

        for filename in filenames:
            print(f'Файл {filename} найден, начинаю обработку...')
            pdf_to_csv(filename)
        filelist = []
        

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Уведомление")
        dlg.setText("Обработка закончена")
        dlg.setIcon(QMessageBox.Icon.Information)
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            self.close()    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

