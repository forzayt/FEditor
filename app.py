import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QLineEdit, QComboBox, QHBoxLayout
)

class FFmpegGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FFmpeg Clip Tool")
        self.file_path = None
        self.audio_streams = []

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # File selection
        self.file_label = QLabel("No file selected")
        btn_file = QPushButton("Select Video")
        btn_file.clicked.connect(self.select_file)

        layout.addWidget(self.file_label)
        layout.addWidget(btn_file)

        # Time inputs
        time_layout = QHBoxLayout()
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("Start (00:27:00)")
        self.end_input = QLineEdit()
        self.end_input.setPlaceholderText("End (00:31:00)")

        time_layout.addWidget(self.start_input)
        time_layout.addWidget(self.end_input)
        layout.addLayout(time_layout)

        # Audio dropdown
        self.audio_dropdown = QComboBox()
        layout.addWidget(self.audio_dropdown)

        # Run button
        btn_run = QPushButton("Cut Clip")
        btn_run.clicked.connect(self.run_ffmpeg)
        layout.addWidget(btn_run)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video")
        if file_path:
            self.file_path = file_path
            self.file_label.setText(file_path)
            self.load_streams()

    def load_streams(self):
        cmd = [
            "ffmpeg", "-i", self.file_path
        ]
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

        self.audio_dropdown.clear()
        self.audio_streams.clear()

        for line in result.stderr.split("\n"):
            if "Audio:" in line:
                index = line.split("Stream #0:")[1].split("(")[0]
                self.audio_streams.append(index)
                self.audio_dropdown.addItem(f"Stream {index} | {line}")

    def run_ffmpeg(self):
        if not self.file_path:
            return

        start = self.start_input.text()
        end = self.end_input.text()

        selected_index = self.audio_dropdown.currentIndex()
        audio_stream = self.audio_streams[selected_index]

        # Ask user where to save
        output, _ = QFileDialog.getSaveFileName(self, "Save Output", "output.mp4", "MP4 Files (*.mp4)")
        if not output:
            return

        cmd = [
            "ffmpeg",
            "-ss", start,
            "-to", end,
            "-i", self.file_path,
            "-map", "0:v",
            "-map", f"0:{audio_stream}",
            "-c", "copy",
            output
        ]

        subprocess.run(cmd)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FFmpegGUI()
    window.showMaximized()  # opens in fullscreen-like maximized mode
    sys.exit(app.exec_())
