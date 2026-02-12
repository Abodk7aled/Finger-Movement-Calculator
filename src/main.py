"""
Finger Movement Calculator - Main Application

A gesture-controlled calculator that uses computer vision and hand tracking
to perform calculations through finger movements.
"""

import cv2
from cvzone.HandTrackingModule import HandDetector

from button import Button
from config import (
    Display, ClearButton, CalculationButtons, 
    ResultDisplay, Fingers, Delay
)


def create_calculator_buttons():
    """
    Create and return a list of calculator buttons in a 4x4 grid.
    
    Returns:
        list: List of Button objects for calculator operations
    """
    buttons = []
    for x_index in range(len(CalculationButtons.BUTTON_VALUES_LIST)):
        for y_index in range(len(CalculationButtons.BUTTON_VALUES_LIST)):
            x_position = x_index * Display.MAIN_BUTTON_SIZE + Display.MAIN_X_OFFSET
            y_position = y_index * Display.MAIN_BUTTON_SIZE + Display.MAIN_Y_OFFSET
            buttons.append(
                Button(
                    position=(x_position, y_position),
                    width=Display.MAIN_BUTTON_SIZE,
                    height=Display.MAIN_BUTTON_SIZE,
                    value=CalculationButtons.BUTTON_VALUES_LIST[y_index][x_index]
                )
            )
    return buttons


def create_clear_button():
    """
    Create and return the AC (All Clear) button.
    
    Returns:
        Button: The clear button object
    """
    return Button(
        position=(
            Display.MAIN_X_OFFSET + Display.MAIN_BUTTON_SIZE * 
            (len(CalculationButtons.BUTTON_VALUES_LIST) - 1), 
            Display.MAIN_BUTTON_SIZE
        ),
        width=Display.MAIN_BUTTON_SIZE, 
        height=Display.MAIN_BUTTON_SIZE, 
        value=ClearButton.START_VALUE
    )


def draw_result_display(img, equation):
    """
    Draw the result display area and equation text.
    
    Args:
        img: The video frame to draw on
        equation: The current equation string to display
    """
    cv2.rectangle(
        img=img,
        pt1=(Display.MAIN_X_OFFSET, Display.MAIN_BUTTON_SIZE),
        pt2=(
            Display.MAIN_X_OFFSET + Display.MAIN_BUTTON_SIZE * 
            (len(CalculationButtons.BUTTON_VALUES_LIST) - 1),
            Display.MAIN_Y_OFFSET + Display.MAIN_BUTTON_SIZE
        ),
        color=ResultDisplay.BUTTON_COLOR,
        thickness=cv2.FILLED
    )
    
    cv2.rectangle(
        img=img,
        pt1=(Display.MAIN_X_OFFSET, Display.MAIN_BUTTON_SIZE),
        pt2=(
            Display.MAIN_X_OFFSET + Display.MAIN_BUTTON_SIZE * 
            (len(CalculationButtons.BUTTON_VALUES_LIST) - 1),
            Display.MAIN_Y_OFFSET + Display.MAIN_BUTTON_SIZE
        ),
        color=ResultDisplay.MAIN_BORDER_COLOR,
        thickness=Display.MAIN_THICKNESS
    )
    
    text_size = cv2.getTextSize(
        text=equation, 
        fontFace=ResultDisplay.MAIN_FONT,
        fontScale=ResultDisplay.FONT_SCALE, 
        thickness=ResultDisplay.THICKNESS
    )
    text_y = int(Display.MAIN_Y_OFFSET - Display.MAIN_BUTTON_SIZE / 2 + text_size[1])
    
    cv2.putText(
        img=img, 
        text=equation, 
        org=(Display.MAIN_X_OFFSET + ResultDisplay.X_MARGIN, text_y),
        fontFace=ResultDisplay.MAIN_FONT, 
        fontScale=ResultDisplay.FONT_SCALE,
        color=ResultDisplay.TEXT_COLOR, 
        thickness=ResultDisplay.THICKNESS
    )


def main():
    """Main application loop for the finger movement calculator."""
    cap = cv2.VideoCapture(0)
    cap.set(3, Display.DISPLAY_DIMENSIONS[0])  # Set width
    cap.set(4, Display.DISPLAY_DIMENSIONS[1])  # Set height
    
    detector = HandDetector(detectionCon=0.5, maxHands=1)
    
    calculation_buttons = create_calculator_buttons()
    clear_button = create_clear_button()
    
    equation = ResultDisplay.START_VALUE
    delay_counter = 0
    is_new_calculation = True
    equation_overflow = ''  # Stores characters that overflow from display
    
    while True:
        success, img = cap.read()
        img = cv2.flip(src=img, flipCode=1)  # Mirror the image
        
        hands, img = detector.findHands(img=img, flipType=False)
        
        draw_result_display(img, equation)
        
        for button in calculation_buttons:
            button.draw_button(
                img=img,
                rectangle_color=CalculationButtons.BUTTON_COLOR,
                text_color=CalculationButtons.TEXT_COLOR,
                font_scale=CalculationButtons.MAIN_FONT_SCALE,
                thickness=CalculationButtons.THICKNESS
            )
        
        clear_button.draw_button(
            img=img,
            rectangle_color=ClearButton.BUTTON_COLOR,
            text_x_margin=-ClearButton.X_MARGIN,
            text_color=ClearButton.TEXT_COLOR,
            font_scale=ClearButton.MAIN_FONT_SCALE,
            thickness=ClearButton.THICKNESS
        )
        
        if hands:
            landmark_list = hands[0]['lmList']  # Get hand landmarks
            
            length, _, img = detector.findDistance(
                p1=landmark_list[Fingers.FINGER_TIP_1][0:2],
                p2=landmark_list[Fingers.FINGER_TIP_2][0:2],
                img=img
            )
            
            x, y = landmark_list[Fingers.FINGER_TIP_1][0:2]
            
            if length < Fingers.CRITICAL_FINGERS_DISTANCE:
                
                if clear_button.check_click(
                    x=x, y=y, img=img,
                    rectangle_color=ClearButton.CHECK_BUTTON_COLOR,
                    text_x_margin=-ClearButton.X_MARGIN,
                    text_color=ClearButton.CHECK_TEXT_COLOR,
                    thickness=ClearButton.CHECK_THICKNESS
                ) and delay_counter == 0:
                    equation = ResultDisplay.START_VALUE
                    is_new_calculation = True
                    equation_overflow = ''
                    delay_counter = 1
                
                for index, button in enumerate(calculation_buttons):
                    if button.check_click(
                        x=x, y=y, img=img,
                        rectangle_color=CalculationButtons.CHECK_BUTTON_COLOR,
                        text_color=CalculationButtons.CHECK_TEXT_COLOR,
                        thickness=CalculationButtons.CHECK_THICKNESS
                    ) and delay_counter == 0:
                        
                        current_value = CalculationButtons.BUTTON_VALUES_LIST[
                            int(index % len(CalculationButtons.BUTTON_VALUES_LIST))
                        ][
                            int(index / len(CalculationButtons.BUTTON_VALUES_LIST))
                        ]
                        
                        if current_value == '=':
                            try:
                                full_equation = equation_overflow + equation
                                equation_overflow = ''
                                # Replace 'x' with '*' for multiplication
                                equation = str(round(eval(full_equation.replace('x', '*')), 3))
                            except (SyntaxError, NameError, ZeroDivisionError):
                                equation = Display.EXCEPTION_MESSAGE
                                is_new_calculation = True
                        else:
                            if is_new_calculation:
                                equation = ''
                                is_new_calculation = False
                            
                            equation += current_value
                            
                            if len(equation) > Display.MAX_NUM_OF_CHARACTERS:
                                equation_overflow += equation[0]
                                equation = equation[1:]
                        
                        delay_counter = 1
        
        if delay_counter != 0:
            delay_counter += 1
            if delay_counter > Delay.MAX_DELAY:
                delay_counter = 0
        
        cv2.imshow(winname=Display.WIN_NAME, mat=img)
        
        # Exit on ESC key (wait for 1ms and check if ESC key is pressed)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
