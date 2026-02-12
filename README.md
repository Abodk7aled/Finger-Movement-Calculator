# 🖐️ Finger Movement Calculator

A gesture-controlled calculator application that uses computer vision and hand tracking to perform mathematical calculations through intuitive finger movements.

## Overview

The Finger Movement Calculator is an innovative application that demonstrates the power of computer vision in creating interactive user interfaces. By tracking hand gestures in real-time, users can perform calculations without touching any physical interface, making it ideal for touchless computing scenarios.

## 📸 Demo

![Finger Movement Calculator Demo](/assets/example-usage.png)

*The calculator in action - performing calculations using hand gestures*

## Features

- Real-time hand tracking and gesture recognition
- Touchless calculator interface controlled by finger movements
- Support for basic arithmetic operations (addition, subtraction, multiplication, division)
- Visual feedback for button presses
- Error handling for invalid calculations
- Clean and intuitive user interface

## Technology Stack

- **Python 3.x** - Core programming language
- **OpenCV** - Computer vision and image processing
- **CVZone** - Simplified hand tracking module built on MediaPipe
- **MediaPipe** - Hand landmark detection

## Installation

### Prerequisites

- Python 3.7 or higher
- Webcam (built-in or external)
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Finger-Movement-Calculator.git
cd Finger-Movement-Calculator
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
./start.sh
```

Or manually:
```bash
python src/main.py
```

## Usage

### Basic Controls

1. **Starting the Application**
   - Launch the application using the start script or directly via Python
   - Ensure your webcam is properly connected and accessible

2. **🖐️ Hand Gestures**
   - Hold your hand in front of the camera
   - 🤏 Pinch (bring index and middle finger tips together) to "click" buttons
   - 👆 Move your hand to position the cursor over different buttons

3. **🔢 Calculator Operations**
   - Numbers: Click on digit buttons (0️⃣-9️⃣)
   - Operations: Click on operator buttons (➕➖✖️➗)
   - Equals: Click '**=**' to evaluate the expression
   - Clear: Click '**AC**' to clear the current calculation

4. **Exiting**
   - Press the ESC key to close the application

### 💡Tips for Best Performance

- Ensure good lighting conditions for optimal hand detection
- Position your hand approximately 1-2 feet from the camera
- Keep your hand steady when selecting buttons
- ⏱ The application uses a delay mechanism to prevent accidental double-clicks

## Configuration

You can customize various aspects of the calculator by modifying the configuration classes in [src/config.py](src/config.py):

- **Display**: Window dimensions, button sizes, colors, and fonts
- **Fingers**: Hand landmark indices and gesture detection thresholds
- **CalculationButtons**: Button layout and styling
- **ClearButton**: Clear button appearance
- **ResultDisplay**: Result area styling
- **Delay**: Click delay timing to prevent double-clicks

### Calculation Engine

- Uses Python's built-in `eval()` function for expression evaluation
- Implements proper error handling for syntax errors, name errors, and division by zero
- Supports floating-point arithmetic with results rounded to 3 decimal places
- Handles equation overflow by storing excess characters when display limit is reached

## Limitations

- Supports single-hand operation only
- Requires adequate lighting for hand detection
- Limited to basic arithmetic operations
- Display shows maximum 7 characters per calculation
- Requires webcam access

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is available for educational and personal use. Please check the LICENSE file for more details.

---

**Note**: This project is designed for educational purposes to demonstrate the integration of computer vision with interactive applications. 
