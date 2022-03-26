from typing import Tuple


class Grid:
    def __init__(self, w, h):
        self.walls = set()
        self.width, self.height = w, h
        self.start = 0
        self.goal = w * h - 1

    def __iter__(self):
        for x in range(self.width):
            for y in range(self.height):
                yield x, y, self.is_wall(x, y), self.is_start(x, y), self.is_goal(x, y)

    def clear(self):
        self.walls.clear()

    def save(self):
        return dict(
            walls=list(self.walls),
            width=self.width,
            height=self.height,
            start=self.start,
            goal=self.goal,
        )

    def load(self, data):
        self.walls = set(data["walls"])
        self.width = data["width"]
        self.height = data["height"]
        self.start = data["start"]
        self.goal = data["goal"]

    def get_start(self) -> Tuple[int, int]:
        return self.start % self.width, self.start // self.width

    def get_goal(self) -> Tuple[int, int]:
        return self.goal % self.width, self.goal // self.width

    def set_wall(self, x, y):
        self.walls.add(x + y * self.width)

    def is_wall(self, x, y):
        return x + y * self.width in self.walls

    def set_open(self, x, y):
        index = x + y * self.width
        if index in self.walls:
            self.walls.remove(index)

    def is_open(self, x, y):
        return x + y * self.width not in self.walls

    def set_goal(self, x, y):
        self.goal = x + y * self.width

    def is_goal(self, x, y):
        return x + y * self.width == self.goal

    def set_start(self, x, y):
        self.start = x+y*self.width

    def is_start(self, x, y):
        return x + y * self.width == self.start

    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbours(self, x, y):
        neighbours = []
        for _x, _y in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if (self.is_valid(_x, _y) and self.is_open(_x, _y)) or self.is_goal(_x, _y):
                neighbours.append((_x, _y))
        return neighbours

