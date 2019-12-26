from dataclasses import dataclass
from typing import Dict, Tuple
from collections import deque
import string
from utils import neighbours

Pos = Tuple[int, int]


@dataclass
class Maze:
    maze: Dict[Pos, str]
    pos_to_pos: Dict[Pos, Pos]
    start: Pos
    goal: Pos

    @staticmethod
    def from_string(maze_str: str) -> "Maze":
        lines = maze_str.splitlines()
        pos_to_portal = {}
        maze = {}
        portal_letters = set(string.ascii_uppercase)
        height = len(lines)
        for y in range(height):
            width = len(lines[y])
            for x in range(width):
                if lines[y][x] == " ":
                    continue

                if lines[y][x] in ".#":
                    maze[y, x] = lines[y][x]
                    continue

                if lines[y][x] in portal_letters:
                    if x + 1 < width and lines[y][x + 1] in portal_letters:
                        if x - 1 >= 0 and lines[y][x - 1] == ".":
                            pos_to_portal[y, x - 1] = lines[y][x] + lines[y][x + 1]
                        elif x + 2 < width and lines[y][x + 2] == ".":
                            pos_to_portal[y, x + 2] = lines[y][x] + lines[y][x + 1]
                    elif (
                        y + 1 < height
                        and x < len(lines[y + 1])
                        and lines[y + 1][x] in portal_letters
                    ):
                        if (
                            y - 1 >= 0
                            and x < len(lines[y - 1])
                            and lines[y - 1][x] == "."
                        ):
                            pos_to_portal[y - 1, x] = lines[y][x] + lines[y + 1][x]
                        elif (
                            y + 2 < height
                            and x < len(lines[y + 2])
                            and lines[y + 2][x] == "."
                        ):
                            pos_to_portal[y + 2, x] = lines[y][x] + lines[y + 1][x]
        start = goal = None
        pos_to_pos = {}
        for pos, portal in pos_to_portal.items():
            if portal == "AA":
                start = pos
            elif portal == "ZZ":
                goal = pos
            else:
                for other_pos, other_portal in pos_to_portal.items():
                    if pos != other_pos and portal == other_portal:
                        pos_to_pos[pos] = other_pos
        assert start and goal
        return Maze(maze, pos_to_pos, start, goal)


def a(maze_str):
    maze = Maze.from_string(maze_str)
    visited = {maze.start}
    queue = deque([(0, maze.start)])
    while queue:
        steps, pos = queue.popleft()
        if pos == maze.goal:
            return steps
        for neighbour in neighbours(pos):
            if neighbour in visited or maze.maze.get(neighbour, "#") == "#":
                continue
            visited.add(neighbour)
            queue.append((steps + 1, neighbour))
        if pos in maze.pos_to_pos:
            neighbour = maze.pos_to_pos[pos]
            if neighbour in visited:
                continue
            visited.add(neighbour)
            queue.append((steps + 1, neighbour))


@dataclass
class RecursiveMaze:
    maze: Dict[Pos, str]
    pos_to_pos: Dict[Pos, Tuple[Pos, int]]
    start: Pos
    goal: Pos

    @staticmethod
    def from_string(maze_str: str) -> "Maze":
        lines = maze_str.splitlines()

        def is_inner_hor(x):
            width = max(map(len, lines))
            if 3 < x < width - 3:
                return 1
            return -1

        def is_inner_ver(y):
            height = len(lines)
            if 3 < y < height - 3:
                return 1
            return -1

        pos_to_portal = {}
        maze = {}
        portal_letters = set(string.ascii_uppercase)
        height = len(lines)
        for y in range(height):
            width = len(lines[y])
            for x in range(width):
                if lines[y][x] == " ":
                    continue

                if lines[y][x] in ".#":
                    maze[y, x] = lines[y][x]
                    continue

                if lines[y][x] in portal_letters:
                    if x + 1 < width and lines[y][x + 1] in portal_letters:
                        if x - 1 >= 0 and lines[y][x - 1] == ".":
                            pos_to_portal[y, x - 1] = (
                                lines[y][x] + lines[y][x + 1],
                                is_inner_hor(x - 1),
                            )
                        elif x + 2 < width and lines[y][x + 2] == ".":
                            pos_to_portal[y, x + 2] = (
                                lines[y][x] + lines[y][x + 1],
                                is_inner_hor(x + 2),
                            )
                    elif (
                        y + 1 < height
                        and x < len(lines[y + 1])
                        and lines[y + 1][x] in portal_letters
                    ):
                        if (
                            y - 1 >= 0
                            and x < len(lines[y - 1])
                            and lines[y - 1][x] == "."
                        ):
                            pos_to_portal[y - 1, x] = (
                                lines[y][x] + lines[y + 1][x],
                                is_inner_ver(y - 1),
                            )
                        elif (
                            y + 2 < height
                            and x < len(lines[y + 2])
                            and lines[y + 2][x] == "."
                        ):
                            pos_to_portal[y + 2, x] = (
                                lines[y][x] + lines[y + 1][x],
                                is_inner_ver(y + 2),
                            )
        start = goal = None
        pos_to_pos = {}
        for pos, (portal, level) in pos_to_portal.items():
            if portal == "AA":
                start = pos
            elif portal == "ZZ":
                goal = pos
            else:
                for other_pos, (other_portal, _) in pos_to_portal.items():
                    if pos != other_pos and portal == other_portal:
                        pos_to_pos[pos] = other_pos, level
        assert start and goal
        return RecursiveMaze(maze, pos_to_pos, start, goal)


def b(maze_str):
    maze = RecursiveMaze.from_string(maze_str)
    start = (maze.start, 0)
    visited = {start}
    queue = deque([(0, start)])
    while queue:
        steps, (pos, level) = queue.popleft()

        if pos == maze.goal and level == 0:
            return steps
        for neighbour in neighbours(pos):
            new_state = (neighbour, level)
            if new_state in visited or maze.maze.get(neighbour, "#") == "#":
                continue
            visited.add(new_state)
            queue.append((steps + 1, new_state))
        if pos in maze.pos_to_pos:
            neighbour, level_incr = maze.pos_to_pos[pos]
            if level == 0 and level_incr == -1:
                continue
            new_state = (neighbour, level + level_incr)
            if new_state in visited:
                continue
            visited.add(new_state)
            queue.append((steps + 1, new_state))


def main():
    maze_str = open("input20.txt").read()
    print(b(maze_str))


if __name__ == "__main__":
    main()
