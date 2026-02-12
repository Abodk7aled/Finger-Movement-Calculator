"""Button class for the calculator interface."""

import cv2

from config import Display


class Button:
    """
    Represents a clickable button in the calculator interface.
    
    Attributes:
        position (tuple): The (x, y) position of the button's top-left corner
        width (int): The width of the button in pixels
        height (int): The height of the button in pixels
        value (str): The text/value displayed on the button
    """
    
    def __init__(self, position: tuple, width: int, height: int, value: str):
        """
        Initialize a new Button instance.
        
        Args:
            position: Tuple containing (x, y) coordinates of top-left corner
            width: Button width in pixels
            height: Button height in pixels
            value: Text or value to display on the button
        """
        self.position = position
        self.width = width
        self.height = height
        self.value = value

    def draw_button(self, img, rectangle_color: tuple, text_color: tuple, 
                   font_scale: float, thickness: int, text_x_margin: int = 0, 
                   text_y_margin: int = 0):
        """
        Draw the button on the video frame.
        
        Args:
            img: The video frame to draw on
            rectangle_color: RGB color tuple for button background
            text_color: RGB color tuple for button text
            font_scale: Font size scale factor
            thickness: Text line thickness
            text_x_margin: Horizontal text offset (default: 0)
            text_y_margin: Vertical text offset (default: 0)
        """
        text_size = cv2.getTextSize(
            text=self.value, 
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=font_scale, 
            thickness=thickness
        )
        text_x = int(self.position[0] + self.width / 2 - text_size[1] + text_x_margin)
        text_y = int(self.position[1] + self.height / 2 + text_size[1] + text_y_margin)
        
        cv2.rectangle(
            img=img, 
            pt1=self.position, 
            pt2=(self.position[0] + self.width, self.position[1] + self.height),
            color=rectangle_color, 
            thickness=cv2.FILLED
        )
        
        cv2.rectangle(
            img=img, 
            pt1=self.position, 
            pt2=(self.position[0] + self.width, self.position[1] + self.height),
            color=Display.MAIN_BORDER_COLOR, 
            thickness=Display.MAIN_THICKNESS
        )
        
        cv2.putText(
            img=img, 
            text=self.value, 
            org=(text_x, text_y), 
            fontFace=Display.MAIN_FONT,
            fontScale=font_scale, 
            color=text_color, 
            thickness=thickness
        )

    def check_click(self, x: int, y: int, img, rectangle_color: tuple, 
                   text_color: tuple, thickness: int, text_x_margin: int = 0, 
                   text_y_margin: int = 0) -> bool:
        """
        Check if the button is clicked at the given coordinates.
        
        Args:
            x: X-coordinate of the finger position
            y: Y-coordinate of the finger position
            img: The video frame to draw on
            rectangle_color: RGB color for button when clicked
            text_color: RGB color for text when clicked
            thickness: Text thickness when clicked
            text_x_margin: Horizontal text offset (default: 0)
            text_y_margin: Vertical text offset (default: 0)
            
        Returns:
            bool: True if coordinates are within button bounds, False otherwise
        """
        if (self.position[0] < x < self.position[0] + self.width and 
            self.position[1] < y < self.position[1] + self.height):
            self.draw_button(
                img=img, 
                rectangle_color=rectangle_color, 
                text_color=text_color,
                font_scale=Display.MAIN_CLICKED_FONT_SCALE, 
                thickness=thickness,
                text_x_margin=text_x_margin, 
                text_y_margin=text_y_margin
            )
            return True
        else:
            return False
