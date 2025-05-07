import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QLabel, QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from picamera2 import Picamera2
from picamera2.previews import QtGlPreview
import cv2
import numpy as np

class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raspberry Pi Camera App")
        self.setGeometry(100, 100, 800, 600)

        # Initialize camera
        self.picam2 = Picamera2()
        self.preview_config = self.picam2.create_preview_configuration(
            main={"size": (640, 480)}
        )
        self.picam2.configure(self.preview_config)
        self.picam2.start()

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create camera preview label
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.camera_label)

        # Create buttons
        self.capture_button = QPushButton("Capture Image")
        self.capture_button.clicked.connect(self.capture_image)
        layout.addWidget(self.capture_button)

        # Setup timer for camera preview
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30ms

        # Create save directory if it doesn't exist
        self.save_dir = "captured_images"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def update_frame(self):
        frame = self.picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
            self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.camera_label.setPixmap(scaled_pixmap)

    def capture_image(self):
        frame = self.picam2.capture_array()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}.jpg"
        filepath = os.path.join(self.save_dir, filename)
        cv2.imwrite(filepath, frame)
        print(f"Image saved: {filepath}")

def main():
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 