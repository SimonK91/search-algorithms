import json
import random
import tkinter as tk
from tkinter import filedialog as fd

import pygame

from App import App
from Button import Button
from Grid import Grid
from SearchAlgorithms import breadth_first_search, best_first_search, a_star_search

tk.Tk().withdraw()

open_color = (255, 255, 255)
wall_color = (0, 0, 0)

start_color = (0, 0, 255)
goal_color = (255, 0, 0)

open_set_color = (255, 255, 0)
closed_set_color = (200, 200, 200)
path_color = (0, 255, 0)


def blend(c1, c2):
    return ((c1[0] + c2[0]) / 2,
            (c1[1] + c2[1]) / 2,
            (c1[2] + c2[2]) / 2)


def render(cell, screen, color, grid_size):
    pygame.draw.rect(surface=screen,
                     color=color,
                     rect=(cell[0] * grid_size, cell[1] * grid_size, grid_size - 1, grid_size - 1))


def save(grid):
    data = json.dumps(grid.save())
    result = fd.asksaveasfilename(filetypes=[("json", "*.json")])
    if result:
        with open(result, 'w') as f:
            f.write(data)


def load(grid):
    result = fd.askopenfilename(filetypes=[("json", "*.json")])
    if result:
        with open(result, 'r') as f:
            grid.load(json.load(f))


def randomize(grid):
    grid.clear()
    for x, y, _, _, _ in grid:
        if random.random() < 0.25:
            grid.set_wall(x, y)


class State:
    def __init__(self):
        self.algorithm = breadth_first_search
        self.solving = False
        self.steps_per_render = 1

    def set_solving(self, solving):
        self.solving = solving

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def add_steps(self, amount):
        self.steps_per_render = max(1, self.steps_per_render + amount)


def main():
    grid = Grid(80, 40)
    grid_size = 10
    side_menu_size = (200, 400)
    width, height = grid.width*grid_size, grid.height*grid_size
    app = App(width + side_menu_size[0], max(height, side_menu_size[1]))
    app.init()
    side_menu_offset = (width, 0)

    state = State()

    side_menu = [Button("BreadthFirst", side_menu_offset[0] + 40, side_menu_offset[1] + 20, padding=5,
                        on_click=lambda: state.set_algorithm(breadth_first_search)),
                 Button("BestFirst", side_menu_offset[0] + 40, side_menu_offset[1] + 60, padding=5,
                        on_click=lambda: state.set_algorithm(best_first_search)),
                 Button("A Star", side_menu_offset[0] + 40, side_menu_offset[1] + 100, padding=5,
                        on_click=lambda: state.set_algorithm(a_star_search)),
                 Button("Start", side_menu_offset[0] + 40, side_menu_offset[1] + 200, padding=5,
                        on_click=lambda: state.set_solving(True)),
                 Button("Stop", side_menu_offset[0] + 100, side_menu_offset[1] + 200, padding=5,
                        on_click=lambda: state.set_solving(False)),
                 Button("Save", side_menu_offset[0] + 40, side_menu_offset[1] + 250, padding=5,
                        on_click=lambda: save(grid)),
                 Button("Load", side_menu_offset[0] + 100, side_menu_offset[1] + 250, padding=5,
                        on_click=lambda: load(grid)),
                 Button("-5", side_menu_offset[0] + 40, side_menu_offset[1] + 350, padding=5,
                        on_click=lambda: state.add_steps(-5)),
                 Button("-1", side_menu_offset[0] + 65, side_menu_offset[1] + 350, padding=5,
                        on_click=lambda: state.add_steps(-1)),
                 Button("+1", side_menu_offset[0] + 90, side_menu_offset[1] + 350, padding=5,
                        on_click=lambda: state.add_steps(1)),
                 Button("+5", side_menu_offset[0] + 115, side_menu_offset[1] + 350, padding=5,
                        on_click=lambda: state.add_steps(5)),
                 Button("Clear", side_menu_offset[0] + 40, side_menu_offset[1] + 300, padding=5,
                        on_click=grid.clear),
                 Button("Randomize", side_menu_offset[0] + 100, side_menu_offset[1] + 300, padding=5,
                        on_click=lambda: randomize(grid)),
                 ]

    mouse_down = False
    setter_function = None
    algorithm = None
    start = None
    goal = None

    while app.is_running:
        for x, y, is_wall, is_start, is_goal in grid:
            color = wall_color if is_wall else open_color
            render((x, y), app.screen, color, grid_size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.quit()
            if event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    x, y = event.pos[0] // grid_size, event.pos[1] // grid_size
                    if grid.is_valid(x, y):
                        setter_function(x, y)
                else:
                    for item in side_menu:
                        over = item.mouse_over(event.pos)
                        if not over:
                            item.state = Button.IDLE
                        else:
                            if item.state == Button.IDLE:
                                item.state = Button.HOVER
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                for item in side_menu:
                    if item.state == Button.PRESSED:
                        item.on_click()
                        item.state = Button.HOVER
            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in side_menu:
                    if item.state == Button.HOVER:
                        item.state = Button.PRESSED
                x, y = event.pos[0] // grid_size, event.pos[1] // grid_size
                if grid.is_valid(x, y):
                    mouse_down = True
                    if grid.is_start(x, y):
                        setter_function = grid.set_start
                    elif grid.is_goal(x, y):
                        setter_function = grid.set_goal
                    elif grid.is_wall(x, y):
                        setter_function = grid.set_open
                    else:
                        setter_function = grid.set_wall
                    setter_function(x, y)

        if not state.solving:
            algorithm = None
            start = None
            goal = None
        else:
            if algorithm is None:
                algorithm = state.algorithm(grid)
                start = grid.get_start()
                goal = grid.get_goal()
            try:
                open_set, closed_set, path = next(algorithm)
                for i in range(state.steps_per_render-1):
                    open_set, closed_set, path = next(algorithm)
            except StopIteration:
                algorithm = None
                continue
            for dataset, color in zip([open_set, closed_set, path], [open_set_color, closed_set_color, path_color]):
                for obj in dataset:
                    if grid.is_wall(*obj):
                        render(obj, app.screen, blend(color, wall_color), grid_size)
                    else:
                        render(obj, app.screen, color, grid_size)

        render(grid.get_start(), app.screen, start_color, grid_size)
        render(grid.get_goal(), app.screen, goal_color, grid_size)
        if start and start != grid.get_start():
            color = wall_color if grid.is_wall(*start) else open_color
            render(start, app.screen, blend(start_color, color), grid_size)
        if goal and goal != grid.get_goal():
            color = wall_color if grid.is_wall(*goal) else open_color
            render(goal, app.screen, blend(goal_color, color), grid_size)

        for item in side_menu:
            item.render(app.screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
