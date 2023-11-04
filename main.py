import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLabel, QSpinBox, QStackedWidget
import PyPDF2
from PIL import Image
from pdf2image import convert_from_path

class PDFTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.pdf_path = None  # Store the selected PDF path

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Stacked widget to switch between different functions
        self.stacked_widget = QStackedWidget(self)
        layout.addWidget(self.stacked_widget)

        # Create pages for different functions
        self.create_select_pdf_page()
        self.create_split_pdf_page()
        self.create_join_pdf_page()
        self.create_convert_to_image_page()

        # Set the window properties
        self.setWindowTitle('PDF Tool')
        self.setGeometry(100, 100, 400, 300)

    def create_select_pdf_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)

        label = QLabel("1. Select a PDF file")
        layout.addWidget(label)

        btn_select_pdf = QPushButton('Select PDF', self)
        btn_select_pdf.clicked.connect(self.select_pdf)
        layout.addWidget(btn_select_pdf)

        self.stacked_widget.addWidget(page)

    def create_split_pdf_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)

        label = QLabel("2. Split PDF")
        layout.addWidget(label)

        self.start_page_label = QLabel("Start Page:")
        layout.addWidget(self.start_page_label)
        self.spinBox_start_page = QSpinBox(self)
        layout.addWidget(self.spinBox_start_page)

        self.end_page_label = QLabel("End Page:")
        layout.addWidget(self.end_page_label)
        self.spinBox_end_page = QSpinBox(self)
        layout.addWidget(self.spinBox_end_page)

        btn_split_pdf = QPushButton('Split PDF', self)
        btn_split_pdf.clicked.connect(self.split_pdf)
        layout.addWidget(btn_split_pdf)

        self.stacked_widget.addWidget(page)

    def create_join_pdf_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)

        label = QLabel("3. Join PDFs")
        layout.addWidget(label)

        btn_join_pdf = QPushButton('Join PDFs', self)
        btn_join_pdf.clicked.connect(self.join_pdf)
        layout.addWidget(btn_join_pdf)

        self.stacked_widget.addWidget(page)

    def create_convert_to_image_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)

        label = QLabel("4. Convert PDF to Images")
        layout.addWidget(label)

        btn_convert_to_image = QPushButton('Convert PDF to Images', self)
        btn_convert_to_image.clicked.connect(self.convert_to_image)
        layout.addWidget(btn_convert_to_image)

        self.stacked_widget.addWidget(page)

    def select_pdf(self):
        pdf_path, _ = QFileDialog.getOpenFileName(self, "Select PDF file", "", "PDF Files (*.pdf)")
        if pdf_path:
            self.pdf_path = pdf_path
            self.stacked_widget.setCurrentIndex(1)  # Switch to the split PDF page

    def split_pdf(self):
        if self.pdf_path:
            start_page = int(self.spinBox_start_page.value())
            end_page = int(self.spinBox_end_page.value())

            if start_page > end_page:
                self.show_message("Start Page should be less than or equal to End Page.")
                return

            output_path, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "PDF Files (*.pdf)")

            if output_path:
                with open(self.pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    writer = PyPDF2.PdfWriter()

                    for page_num in range(start_page - 1, end_page):
                        writer.add_page(reader.pages[page_num])

                    with open(output_path, 'wb') as output_file:
                        writer.write(output_file)

                self.show_message("PDF split successfully!")

    def join_pdf(self):
        pdf_files, _ = QFileDialog.getOpenFileNames(self, "Select PDF files", "", "PDF Files (*.pdf)")

        if len(pdf_files) < 2:
            self.show_message("Select at least 2 PDF files to join.")
            return

        output_path, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "PDF Files (*.pdf)")

        if output_path:
            writer = PyPDF2.PdfWriter()

            for pdf_file in pdf_files:
                with open(pdf_file, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)

                    for page_num in range(len(reader.pages)):
                        writer.add_page(reader.pages[page_num])

            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

            self.show_message("PDFs joined successfully!")

    def convert_to_image(self):
        if self.pdf_path:
            output_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")

            if output_path:
                images = convert_from_path(self.pdf_path)

                for i, image in enumerate(images):
                    image.save(f'{output_path}/page_{i + 1}.png', 'PNG')

                self.show_message("PDF converted to images successfully!")

    def show_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setText(message)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFTool()
    window.show()
    sys.exit(app.exec())
