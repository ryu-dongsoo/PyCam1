# Raspberry Pi 5 CSI Camera Application

This application provides a GUI interface for real-time camera display and image capture using the Raspberry Pi 5's CSI camera module.

## Features
- Real-time camera preview
- Image capture and save functionality
- Simple and intuitive GUI interface
- Remote access support

## Requirements
- Raspberry Pi 5
- CSI Camera Module 3
- Python 3.7+
- Required Python packages (see requirements.txt)

## Installation
1. Clone this repository:
```bash
git clone [repository-url]
cd PyCam1
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Enable the camera interface:
```bash
sudo raspi-config
```
Navigate to "Interface Options" -> "Camera" and enable it.

## Usage
Run the application:
```bash
python camera_app.py
```

## Development History
- Initial project setup
- Basic GUI implementation
- Camera integration
- Image capture functionality
- File saving implementation 