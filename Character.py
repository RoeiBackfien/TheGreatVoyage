
class Character:
    def __init__(self, x, y, name, color, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def __str__(self):
        return self.name
