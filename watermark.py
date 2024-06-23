class Watermark:
    def __init__(self, text: object, font: object, color: object, fontsize: object, opacity: object, pos_x,
                 pos_y) -> object:
        self.text = text
        self.font = font
        self.color = color
        self.fontsize = fontsize
        self.opacity = opacity
        self.pos_x = pos_x
        self.pos_y = pos_y
