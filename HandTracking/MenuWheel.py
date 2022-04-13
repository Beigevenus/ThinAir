from HandTracking.Button import Button
from HandTracking.Canvas import Canvas
from HandTracking.Point import Point


class MenuWheel:
    def __init__(self, layer: Canvas):
        self.is_open: bool = False
        self.tool_buttons: list[Button] = []
        self.color_buttons: list[Button] = []
        self.layer = layer
        self.center_point = Point(0, 0)
        self.prev_drawing_color: str = "WHITE"
        self.drawing_color: str = "WHITE"
        self.current_tool: str = "DRAW"

        self.color_palette = {'WHITE': [150, 150, 150, 255], 'BLACK': [1, 1, 1, 1], 'RED': [0, 0, 255, 255],
                              'GREEN': [0, 255, 0, 255], 'BLUE': [255, 0, 0, 255]}

        self.initialize_buttons()

    def initialize_buttons(self):
        # TODO: Write docstring for method
        self.add_tool_button(self.__select_eraser, "ERASE", img="eraser.png")
        self.add_tool_button(self.__select_drawer, "DRAW", img="brush.png")
        self.add_tool_button(self.__select_wipe, "WIPE", img="wipe.png")

        for name, color in self.color_palette.items():
            self.add_color_button(self.__change_color, color)

    def open(self):
        pass

    def add_tool_button(self, callback, tool, img=None):
        # TODO: Write docstring for method
        if self.current_tool == tool:
            self.tool_buttons.append(Button(callback, active=True, icon=img))
        else:
            self.tool_buttons.append(Button(callback, icon=img))

    def add_color_button(self, callback, color):
        if self.drawing_color == color:
            self.color_buttons.append(Button(callback, color=color, active=True))
        else:
            self.color_buttons.append(Button(callback, color=color))

    def draw_buttons(self):
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

    def __select_eraser(self, button):
        if self.current_tool != "ERASE":
            self.__clear_active_tool_button()

            button.active = True
            self.prev_drawing_color = self.drawing_color
            # self.drawing_color = "ERASER"
            self.current_tool = "ERASE"

    def __select_drawer(self, button):
        if self.current_tool != "DRAW":
            self.__clear_active_tool_button()

            button.active = True
            self.drawing_color = self.prev_drawing_color
            self.current_tool = "DRAW"

    def __select_wipe(self, button):
        self.layer.hard_wipe()

    def __clear_active_tool_button(self):
        for button in self.tool_buttons:
            button.active = False

    def __change_color(self, button: Button):
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

    def check_button_click(self, point: Point):
        for button in self.color_buttons:
            if button.is_point_in_circle(point):
                button.callback(button)
        for button in self.tool_buttons:
            if button.is_point_in_circle(point):
                button.callback(button)

    def open_menu(self):
        self.is_open = True
        self.draw_buttons()
        pass

    def close_menu(self):
        self.is_open = False
        self.layer.wipe()
        pass

