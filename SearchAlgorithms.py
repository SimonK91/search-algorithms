from Grid import Grid


def _h_cost(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return dx + dy


def BreadthFirst(grid: Grid):
    start = grid.get_start()
    goal = grid.get_goal()
    open_set = [start]
    route = {start: None}
    closed_set = set()
    path = []
    while open_set:
        yield open_set, closed_set, path
        cell = open_set[0]
        open_set.remove(cell)
        closed_set.add(cell)

        if cell == goal:
            path = []
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


def BestFirst(grid: Grid):
    start = grid.get_start()
    goal = grid.get_goal()

    open_set = set()
    open_set.add(start)
    route = {start: None}
    closed_set = set()
    path = []

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


def AStar(grid: Grid):
    start = grid.get_start()
    goal = grid.get_goal()

    open_set = set()
    open_set.add(start)
    route = {start: None}
    costs = {start: 0}
    closed_set = set()
    path = []

    while open_set:
        yield open_set, closed_set, path

        cell = None
        cost = None
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
