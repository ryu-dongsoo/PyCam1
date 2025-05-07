# 라즈베리파이 5 CSI 카메라 애플리케이션

이 애플리케이션은 라즈베리파이 5의 CSI 카메라 모듈을 사용하여 실시간 카메라 디스플레이와 이미지 캡처 기능을 제공하는 GUI 인터페이스입니다.

## 주요 기능
- 실시간 카메라 미리보기
- 이미지 캡처 및 저장 기능
- 직관적인 GUI 인터페이스
- 원격 접속 지원

## 시스템 요구사항
- 라즈베리파이 5
- CSI 카메라 모듈 3
- Python 3.7 이상
- 필요한 Python 패키지 (requirements.txt 참조)

## 설치 방법
1. 저장소 클론:
```bash
git clone [repository-url]
cd PyCam1
```

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

3. 카메라 인터페이스 활성화:
```bash
sudo raspi-config
```
"Interface Options" -> "Camera"로 이동하여 활성화합니다.

## 사용 방법
애플리케이션 실행:
```bash
python camera_app.py
```

## 개발 이력
- 초기 프로젝트 설정
- 기본 GUI 구현
- 카메라 통합
- 이미지 캡처 기능 구현
- 파일 저장 기능 구현 