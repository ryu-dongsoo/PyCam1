import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QLabel, QFileDialog, QHBoxLayout,
                            QGroupBox, QSpacerItem, QSizePolicy, QDesktopWidget)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QImage, QPixmap, QFont
from picamera2 import Picamera2
from picamera2.previews import QtGlPreview
import cv2
import numpy as np

class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("라즈베리파이 카메라 앱")
        
        # 최소 크기 설정 (비율 유지)
        self.setMinimumSize(640, 480)
        
        # 크기 조절 정책 설정
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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
        main_layout.setSpacing(20)  # 위젯 간 간격 설정
        main_layout.setContentsMargins(20, 20, 20, 20)  # 여백 설정

        # 카메라 미리보기 레이블 생성
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("""
            QLabel {
                background-color: #2c3e50;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        # 카메라 레이블의 크기 정책 설정
        self.camera_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.camera_label.setMinimumSize(640, 480)  # 최소 크기 설정
        main_layout.addWidget(self.camera_label)

        # 컨트롤 그룹 생성
        control_group = QGroupBox("카메라 제어")
        control_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #34495e;
                border-radius: 8px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        control_layout = QHBoxLayout()
        control_layout.setSpacing(15)  # 버튼 간 간격 설정

        # 버튼 스타일 정의
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2472a4;
            }
        """

        # 자동 촛점 버튼
        self.auto_focus_button = QPushButton("자동 촛점 조절")
        self.auto_focus_button.setStyleSheet(button_style.replace("#3498db", "#2ecc71")
                                           .replace("#2980b9", "#27ae60")
                                           .replace("#2472a4", "#219a52"))
        self.auto_focus_button.clicked.connect(self.auto_focus)
        control_layout.addWidget(self.auto_focus_button)

        # 이미지 캡처 버튼
        self.capture_button = QPushButton("이미지 캡처")
        self.capture_button.setStyleSheet(button_style)
        self.capture_button.clicked.connect(self.capture_image)
        control_layout.addWidget(self.capture_button)

        # 종료 버튼
        self.exit_button = QPushButton("종료")
        self.exit_button.setStyleSheet(button_style.replace("#3498db", "#e74c3c")
                                     .replace("#2980b9", "#c0392b")
                                     .replace("#2472a4", "#a93226"))
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

    def resizeEvent(self, event):
        # 창 크기가 변경될 때 비율 유지
        super().resizeEvent(event)
        # 카메라 레이블의 크기를 창 크기에 맞게 조정
        self.update_frame()

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
        
        # 레이블의 크기에 맞게 이미지 크기 조정 (비율 유지)
        label_size = self.camera_label.size()
        scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
            label_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
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
    app = QApplication(sys.argv)
    window = CameraApp()
    
    # 화면 크기의 60%로 설정
    screen = QDesktopWidget().screenGeometry()
    window.setGeometry(
        screen.width() // 4,  # 화면 가로 중앙
        screen.height() // 4,  # 화면 세로 중앙
        int(screen.width() * 0.6),   # 화면 가로의 60%
        int(screen.height() * 0.6)   # 화면 세로의 60%
    )
    
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 