import numpy as np

from HandTracking.Canvas import Canvas
import pytest

from HandTracking.store.Layer import Layer

x_fail = pytest.mark.xfail


class TestCanvas:
    # TODO: Reconsider test cases!
    @pytest.mark.parametrize("width, height", [(-1920, 1080), (1920, -1080)])
    def test_resize_negative_raises_value_error(self, width, height):
        # Arrange
        canvas: Canvas = Canvas.__new__(Canvas)

        # Act & Assert
        with pytest.raises(ValueError):
            canvas.resize(width, height)

    @pytest.mark.parametrize("width, height", [(0, 1080), (1920, 0)])
    def test_resize_zero_raises_value_error(self, width, height):
        # Arrange
        canvas: Canvas = Canvas.__new__(Canvas)

        # Act & Assert
        with pytest.raises(ValueError):
            canvas.resize(width, height)

    @pytest.mark.parametrize("width, height, expected_width, expected_height", [(1280, 720, 1280, 720),
                                                                                (1920, 1080, 1920, 1080),
                                                                                (3840, 2160, 3840, 2160)])
    def test_resize_positive_successful(self, width, height, expected_width, expected_height):
        # Arrange
        canvas: Canvas = Canvas.__new__(Canvas)
        canvas.image = np.zeros(shape=[height, width, 4], dtype=np.uint8)
        canvas.layers = []

        # Act
        canvas.resize(width, height)

        # Assert
        assert canvas.width == expected_width
        assert canvas.height == expected_height

    @pytest.mark.parametrize("name, position, expected_position", [("TEST1", 0, 0),
                                                                   ("TEST2", 1, 1),
                                                                   ("TEST3", -1, -1),
                                                                   ("TEST4", 35, 3),
                                                                   ("TEST5", 2, 2)])
    def test_create_layer(self, name, position, expected_position):
        # Arrange
        canvas: Canvas = Canvas.__new__(Canvas)
        canvas.layers = [(), (), ()]
        canvas.width = 100
        canvas.height = 100

        # Act
        canvas.create_layer(name, position=position)

        # Assert
        assert canvas.layers[expected_position][0] == name

    def test_delete_layer(self):
        # Arrange
        canvas: Canvas = Canvas.__new__(Canvas)
        layer: Layer = Layer.__new__(Layer)
        canvas.layers = [("OTHER1", layer), ("DELETE_ME", layer), ("OTHER2", layer)]

        # Act
        canvas.delete_layer("DELETE_ME")

        # Assert
        assert ("DELETE_ME", layer) not in canvas.layers
        assert ("OTHER1", layer) in canvas.layers
        assert ("OTHER2", layer) in canvas.layers

    def test_get_layer(self):
        # Arrange
        canvas: Canvas = Canvas.__new__(Canvas)
        layer1 = Layer.__new__(Layer)
        layer2 = Layer.__new__(Layer)
        layer3 = Layer.__new__(Layer)
        canvas.layers = [("LAYER1", layer1), ("LAYER2", layer2), ("LAYER3", layer3)]

        # Act
        actual1 = canvas.get_layer("LAYER1")
        actual2 = canvas.get_layer("LAYER2")
        actual3 = canvas.get_layer("LAYER3")
        actual4 = canvas.get_layer("LAYER4")

        # Assert
        assert actual1 == layer1
        assert actual2 == layer2
        assert actual3 == layer3
        assert actual4 is None
