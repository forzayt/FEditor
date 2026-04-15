import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QComboBox, QHBoxLayout, QProgressBar
)


class FFmpegGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FFmpeg Clip Tool")
        self.file_path = None
        self.audio_streams = []
        self.duration = 0

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # File selection
        self.file_label = QLabel("No file selected")
        btn_file = QPushButton("Select Video")
        btn_file.clicked.connect(self.select_file)

        layout.addWidget(self.file_label)
        layout.addWidget(btn_file)

        # --- START TIME ---
        start_layout = QHBoxLayout()
        self.start_h = QComboBox()
        self.start_m = QComboBox()
        self.start_s = QComboBox()

        start_layout.addWidget(QLabel("Start:"))
        start_layout.addWidget(self.start_h)
        start_layout.addWidget(self.start_m)
        start_layout.addWidget(self.start_s)

        # --- END TIME ---
        end_layout = QHBoxLayout()
        self.end_h = QComboBox()
        self.end_m = QComboBox()
        self.end_s = QComboBox()

        end_layout.addWidget(QLabel("End:"))
        end_layout.addWidget(self.end_h)
        end_layout.addWidget(self.end_m)
        end_layout.addWidget(self.end_s)

        # Populate dropdowns
        for i in range(60):
            val = f"{i:02}"
            self.start_m.addItem(val)
            self.start_s.addItem(val)
            self.end_m.addItem(val)
            self.end_s.addItem(val)

        for i in range(24):
            val = f"{i:02}"
            self.start_h.addItem(val)
            self.end_h.addItem(val)

        layout.addLayout(start_layout)
        layout.addLayout(end_layout)

        # Audio dropdown
        self.audio_dropdown = QComboBox()
        layout.addWidget(self.audio_dropdown)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

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
        # Get duration
        try:
            result = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries",
                "format=duration", "-of",
                "default=noprint_wrappers=1:nokey=1", self.file_path
            ], stdout=subprocess.PIPE, text=True)
            self.duration = float(result.stdout.strip())
        except:
            self.duration = 0

        # Get audio streams
        cmd = ["ffmpeg", "-i", self.file_path]
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)

        self.audio_dropdown.clear()
        self.audio_streams.clear()

        for line in result.stderr.split("\n"):
            if "Audio:" in line:
                index = line.split("Stream #0:")[1].split(":")[0].strip()
                if "(eng)" in line.lower():
                    label = f"Stream {index} (English)"
                else:
                    label = f"Stream {index}"
                self.audio_streams.append(index)
                self.audio_dropdown.addItem(label)


    def run_ffmpeg(self):
        if not self.file_path:
            print("No file selected")
            return

        # Build time strings
        start = f"{self.start_h.currentText()}:{self.start_m.currentText()}:{self.start_s.currentText()}"
        end = f"{self.end_h.currentText()}:{self.end_m.currentText()}:{self.end_s.currentText()}"

        print("Start:", start)
        print("End:", end)

        if start >= end:
            print("Invalid time range")
            return

        selected_index = self.audio_dropdown.currentIndex()
        if selected_index < 0:
            print("No audio selected")
            return

        audio_stream = self.audio_streams[selected_index].strip()

        # Save dialog
        output, _ = QFileDialog.getSaveFileName(
            self, "Save Output", "output.mp4", "MP4 Files (*.mp4)"
        )
        if not output:
            print("Save cancelled")
            return

        print("Saving to:", output)

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

        print("Running command:", " ".join(cmd))

        self.progress.setValue(0)

        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)

        while True:
            line = process.stderr.readline()
            if not line:
                break

            print(line.strip())  # 🔥 show logs

            if "time=" in line:
                try:
                    time_str = line.split("time=")[1].split(" ")[0]
                    h, m, s = time_str.split(":")
                    current = int(h) * 3600 + int(m) * 60 + float(s)

                    if self.duration > 0:
                        percent = int((current / self.duration) * 100)
                        self.progress.setValue(percent)
                except:
                    pass

        process.wait()

        print("Return code:", process.returncode)

        if process.returncode == 0:
            print("✅ Success")
        else:
            print("❌ FFmpeg failed")

        self.progress.setValue(100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FFmpegGUI()
    window.showMaximized()
    sys.exit(app.exec_())