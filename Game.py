class Game():

    def __init__(self):
        self.snake = Snake()

class Snake():

    def __init__(self):
        self.length = 1
        self.orientation = [0, 1]
