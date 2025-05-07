import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QLabel, QFileDialog, QHBoxLayout,
                            QGroupBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from picamera2 import Picamera2
from picamera2.previews import QtGlPreview
import cv2
import numpy as np

class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("라즈베리파이 카메라 앱")
        self.setGeometry(100, 100, 1000, 800)

        # 카메라 초기화
        self.picam2 = Picamera2()
        self.preview_config = self.picam2.create_preview_configuration(
            main={"size": (640, 480)}
        )
        self.picam2.configure(self.preview_config)
        self.picam2.start()

        # 중앙 위젯과 레이아웃 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 카메라 미리보기 레이블 생성
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.camera_label)

        # 컨트롤 그룹 생성
        control_group = QGroupBox("카메라 제어")
        control_layout = QHBoxLayout()

        # 자동 촛점 버튼
        self.auto_focus_button = QPushButton("자동 촛점 조절")
        self.auto_focus_button.clicked.connect(self.auto_focus)
        control_layout.addWidget(self.auto_focus_button)

        # 이미지 캡처 버튼
        self.capture_button = QPushButton("이미지 캡처")
        self.capture_button.clicked.connect(self.capture_image)
        control_layout.addWidget(self.capture_button)

        # 종료 버튼 추가
        self.exit_button = QPushButton("종료")
        self.exit_button.clicked.connect(self.close)
        control_layout.addWidget(self.exit_button)

        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)

        # 카메라 미리보기를 위한 타이머 설정
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms마다 업데이트

        # 저장 디렉토리 생성
        self.save_dir = "captured_images"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def auto_focus(self):
        # 자동 촛점 모드 설정
        self.picam2.set_controls({"AfMode": 2})  # 2는 연속 자동 촛점 모드
        # 촛점 조절 시작
        self.picam2.autofocus_cycle()
        print("자동 촛점 조절 중...")

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
        default_filename = f"이미지_{timestamp}.jpg"
        
        # 파일 저장 다이얼로그 표시
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "이미지 저장",
            os.path.join(self.save_dir, default_filename),
            "JPEG 이미지 (*.jpg);;모든 파일 (*.*)"
        )
        
        if filepath:
            cv2.imwrite(filepath, frame)
            print(f"이미지 저장됨: {filepath}")

def main():
    # 로컬 디스플레이를 위한 환경 설정
    os.environ["DISPLAY"] = ":0"  # 로컬 디스플레이 설정
    os.environ["QT_QPA_PLATFORM"] = "xcb"  # X11 디스플레이 서버 사용
    
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 