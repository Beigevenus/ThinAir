from menu_wheel.Button import Button
from model.Canvas import Canvas
from model.Point import Point


class MenuWheel:
    def __init__(self, layer: Canvas):
        self.tool_buttons: list[Button] = []
        self.color_buttons: list[Button] = []
        self.layer = layer
        self.prev_drawing_color: str = "WHITE"
        self.drawing_color: str = "WHITE"
        self.current_tool: str = "DRAW"

        self.color_palette = {'WHITE': [150, 150, 150, 255], 'BLACK': [1, 1, 1, 1], 'RED': [0, 0, 255, 255],
                              'GREEN': [0, 255, 0, 255], 'BLUE': [255, 0, 0, 255]}

        self.initialize_buttons()

    def initialize_buttons(self) -> None:
        """
        Creates all tool and color buttons for the menu wheel, when first instantiated.
        """
        self.add_tool_button(self.__select_eraser, "ERASE", img="eraser.png")
        self.add_tool_button(self.__select_drawer, "DRAW", img="brush.png")
        self.add_tool_button(self.__select_wipe, "WIPE", img="wipe.png")

        for name, color in self.color_palette.items():
            self.add_color_button(self.__change_color, color)

    def add_tool_button(self, callback, tool: str, img: str = None) -> None:
        """
        Adds a new tool button to the menu wheel.

        :param callback: The callback function to call when the button is "pressed"
        :param tool: The name of the tool to add
        :param img: The path of the image to display for the tool
        """
        if self.current_tool == tool:
            self.tool_buttons.append(Button(callback, active=True, icon=img, offset=(-100, 0)))
        else:
            self.tool_buttons.append(Button(callback, icon=img, offset=(-100, 0)))

    def add_color_button(self, callback, color: str) -> None:
        """
        Adds a new color button to the menu wheel.

        :param callback: The callback function to call when the button is "pressed"
        :param color: The name of the color
        """
        if self.drawing_color == color:
            self.color_buttons.append(Button(callback, color=color, active=True, offset=(0, 100)))
        else:
            self.color_buttons.append(Button(callback, color=color, offset=(0, 100)))

    def draw_buttons(self) -> None:
        """
        Draws the buttons on the canvas, in the top left corner.
        """
        top_left = Point(self.layer.width, 0)
        circle_size = round(self.layer.width * 0.03)

        for idx, button in enumerate(self.tool_buttons):
            button.size = circle_size
            button_location = Point(round(top_left.x - circle_size - (circle_size / 2)),
                                    round(top_left.y + ((circle_size * 2 + 10) * (idx + 1)) + (circle_size * 2)))
            button.set_location(button_location)
            
            if button.active:
                self.layer.draw_circle(button.location, [255, 201, 99, 255], circle_size + 4)

            self.layer.draw_circle(button.location, [150, 150, 150, 255], circle_size)

            if button.icon is not None:
                self.layer.draw_img(button.icon, button.size, button.location)
                pass

        for idx, button in enumerate(self.color_buttons):
            button.size = circle_size
            button_location = Point(round(top_left.x - ((circle_size * 2 + 10) * (idx + 1)) - (circle_size * 2)),
                                    round(top_left.y + circle_size + (circle_size / 2)))
            button.set_location(button_location)

            if button.active:
                self.layer.draw_circle(button.location, [255, 201, 99, 255], circle_size + 4)

            self.layer.draw_circle(button.location, button.color, circle_size)

    def __select_eraser(self, button: Button) -> None:
        """
        Selects the eraser tool.

        :param button: The eraser Button object
        """
        if self.current_tool != "ERASE":
            self.__clear_active_tool_button()

            button.active = True
            self.prev_drawing_color = self.drawing_color
            # self.drawing_color = "ERASER"
            self.current_tool = "ERASE"

    def __select_drawer(self, button: Button) -> None:
        """
        Selects the drawing tool.

        :param button: The drawing Button object
        """
        if self.current_tool != "DRAW":
            self.__clear_active_tool_button()

            button.active = True
            self.drawing_color = self.prev_drawing_color
            self.current_tool = "DRAW"

    def __select_wipe(self, button: Button) -> None:
        """
        Performs a wipe of the canvas.

        :param button: (Unused)
        """
        self.layer.hard_wipe()

    def __clear_active_tool_button(self) -> None:
        """
        Sets all tool button statuses to inactive.
        """
        for button in self.tool_buttons:
            button.active = False

    def __change_color(self, button: Button) -> None:
        """
        Changes the current drawing color.

        :param button: The color button that has been selected
        """
        if self.current_tool != "ERASE":
            actual_color = button.color

            for button in self.color_buttons:
                if actual_color == button.color:
                    button.active = True
                    self.layer.color = button.color
                    self.drawing_color = button.color
                else:
                    button.active = False
        else:
            actual_color = button.color

            for button in self.color_buttons:
                if actual_color == button.color:
                    button.active = True
                    self.prev_drawing_color = button.color
                else:
                    button.active = False

    def check_button_click(self, point: Point) -> None:
        """
        Determines whether a button has been "clicked" and calls the appropriate callback function.

        :param point: The position of the cursor
        """
        for button in self.color_buttons:
            if button.is_point_in_circle(point):
                button.callback(button)
        for button in self.tool_buttons:
            if button.is_point_in_circle(point):
                button.callback(button)

    def draw_menu(self) -> None:
        """
        Opens the menu wheel.
        """
        self.draw_buttons()
