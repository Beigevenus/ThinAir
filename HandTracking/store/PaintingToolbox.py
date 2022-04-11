from typing import Optional


class PaintingToolbox:
    # TODO: Reconsider how to define the current color
    def __init__(self, size: int = 5, colors: Optional[dict[str, list[int]]] = None,
                 current_color: str = "WHITE") -> None:
        color_palette = {'WHITE': [150, 150, 150, 255], 'BLACK': [1, 1, 1, 1], 'RED': [0, 0, 255, 255],
                         'GREEN': [0, 255, 0, 255], 'BLUE': [255, 0, 0, 255]}

        if colors:
            for name, color in colors.items():
                color_palette[name] = color

        self.line_size: int = int(size)
        self.circle_size: int = int(size/2)
        self.color_palette: dict = color_palette
        self.current_color = self.color_palette[current_color]

    def change_color(self, new_color: str) -> None:
        """
        Changes the current color of the toolbox to the specified color if it exists in its list of possible colors.

        :param new_color: A string representing the new color to replace the current with
        """
        try:
            self.current_color = self.color_palette[new_color]
        except KeyError:
            self.current_color = self.color_palette['WHITE']

    def change_color_rgba(self, new_color: list[int]) -> None:
        """
        Changes the current color of the toolbox based on an RGBA value.

        :param new_color: The RGBA value to change the current color to
        """
        self.current_color = new_color

    def change_line_size(self, size: int = 5) -> None:
        """
        Changes the current line size of the toolbox, and thereby also the circle size.

        :param size: An integer representing the new line size to set
        """
        self.line_size = int(size)
        self.circle_size = int(size / 2)
