from typing import Tuple, Optional, List, Dict, Set

from Grid import Grid


def _h_cost(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return dx + dy


def breadth_first_search(grid: Grid):
    start = grid.get_start()
    goal = grid.get_goal()

    open_set: List[Tuple[int, int]] = []
    route: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
    closed_set: Set[Tuple[int, int]] = set()
    path: List[Tuple[int, int]] = []
    open_set.append(start)

    while open_set:
        yield open_set, closed_set, path
        cell = open_set[0]
        open_set.remove(cell)
        closed_set.add(cell)

        if cell == goal:
            while cell:
                path.append(cell)
                cell = route[cell]
            path = list(reversed(path))
            break
        else:
            for nbr in grid.get_neighbours(*cell):
                if nbr not in closed_set and nbr not in open_set:
                    route[nbr] = cell
                    open_set.append(nbr)

    for i in range(len(path)):
        yield open_set, closed_set, path[:i]
    for i in range(100):
        yield open_set, closed_set, path


def best_first_search(grid: Grid):
    start = grid.get_start()
    goal = grid.get_goal()

    open_set: Set[Tuple[int, int]] = set()
    route: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
    closed_set: Set[Tuple[int, int]] = set()
    path: List[Tuple[int, int]] = []
    open_set.add(start)

    while open_set:
        yield open_set, closed_set, path
        cell = None
        cost = None
        for obj in open_set:
            cand_cost = _h_cost(obj, goal)
            if cost is None or cand_cost < cost:
                cell = obj
                cost = cand_cost
        open_set.remove(cell)
        closed_set.add(cell)

        if cell == goal:
            while cell:
                path.append(cell)
                cell = route[cell]
            path = list(reversed(path))
            break
        else:
            for nbr in grid.get_neighbours(*cell):
                if nbr not in closed_set and nbr not in open_set:
                    open_set.add(nbr)
                    route[nbr] = cell

    for i in range(len(path)):
        yield open_set, closed_set, path[:i]
    for i in range(100):
        yield open_set, closed_set, path


def a_star_search(grid: Grid):
    start = grid.get_start()
    goal = grid.get_goal()

    open_set: Set[Tuple[int, int]] = set()
    route: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
    costs: Dict[Tuple[int, int], int] = {start: 0}
    closed_set: Set[Tuple[int, int]] = set()
    path: List[Tuple[int, int]] = []
    open_set.add(start)

    while open_set:
        yield open_set, closed_set, path

        cell: Optional[Tuple[int, int]] = None
        cost: Optional[int] = None
        for obj in open_set:
            cand_cost = _h_cost(obj, goal) + costs[obj]
            if cost is None or cand_cost < cost:  # or (cand_cost == cost and costs[obj] > costs[cell]):
                cell = obj
                cost = cand_cost
        open_set.remove(cell)
        closed_set.add(cell)

        if cell == goal:
            while cell:
                path.append(cell)
                cell = route[cell]
            path = list(reversed(path))
            break
        else:
            for nbr in grid.get_neighbours(*cell):
                if nbr not in closed_set:
                    if nbr not in open_set:
                        open_set.add(nbr)
                        route[nbr] = cell
                        costs[nbr] = costs[cell]+1
                    elif costs[cell] + 1 < costs[nbr]:
                        route[nbr] = cell
                        costs[nbr] = costs[cell] + 1

    for i in range(len(path)):
        yield open_set, closed_set, path[:i]
    for i in range(100):
        yield open_set, closed_set, path
