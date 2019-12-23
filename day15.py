from day11 import run_intcode
from collections import defaultdict, deque

cached_world = """
?######?##############?#######?#########?
#       G             #       #         #
# ### ### ####### ### # ##### ##### ####?
#   # #   #   #   # # # #   # #   #     #
?## # # ### ### ### # # # # # # # ##### #
#   #   #   #   #     #   # # # #   #   #
# ##?#### # # ############# # # ### # # #
#   #     # #           #   # #   # # # #
?## ##### # ########### # ### ### # # ##?
# #       #       #   # #   #     # #   #
# ########?## ##### # # ### ####### # # #
#   #     #   #     #     #   #     # # #
# ### # ### ### ### ##### ### # ####### #
# #   # #   # # #   #   # #   # #       #
# # ### # ### # ##### # ### ### # ##### #
# #   #   #   #   #   #     #   #   #   #
# ### ##### ##### # ######### ##?## # ##?
#     #         # #     #   #   #   #   #
# ############# # ##### # # ### # ######?
#   #     #     # #       #   # #       #
?## # ### # ### # # ########### # ##### #
# #   # # #   # # # #S  #     # #     # #
# ##### # ### ### # ### # ### # ##### # #
#       # #   #   # #   #   #   # #   # #
# ### ### # # # ### # ##### ##### # ### #
# # #     # # #     # #     #   #   #   #
# # ####### # ####### # ##### ### ### # #
# #         # #   #   #   #   #   #   # #
# # ######### ### # ##### ### # ### ### #
# #   #     #   # # #     #   # #   # # #
# ### # ### ### # # ### ### ### # ### # #
#   # # #     #   # #   #   #   #   #   #
?## # # # ####### # # ##### # ##### ### #
# # # # #         #   #   # # #   #   # #
# # # # ############### # # # # # ### # #
# #   # #   #   #       # # #   #   # # #
# ##### ### # # # # ##### # ####### # ##?
# #   #   #   #   #   # # #         #   #
# # # ### ########### # # ############# #
#   #                 #                 #
?###?#################?#################?
""".strip().splitlines()


def move(pos, d):
    if d == 1:
        return pos[0] - 1, pos[1]
    if d == 2:
        return pos[0] + 1, pos[1]
    if d == 3:
        return pos[0], pos[1] - 1
    if d == 4:
        return pos[0], pos[1] + 1


def a(program, return_map=False):
    initial_state = ()
    visited = {(0, 0)}
    queue = deque([initial_state])
    world = defaultdict(lambda: "?")
    world[0, 0] = "S"
    while queue:
        path = queue.popleft()
        computer = run_intcode(program[:])
        computer.send(None)
        pos = (0, 0)
        for p in path:
            status = computer.send(p)
            pos = move(pos, p)
            assert status in [0, 1, 2]
            if status == 0:
                world[pos] = "#"
                break
            elif status == 1:
                world[pos] = " "
            elif status == 2:
                pos = move(pos, p)
                world[pos] = "G"
                if not return_map:
                    return len(path), world
            r = next(computer)
            assert r is None
        else:
            for command in range(1, 5):
                maybe_new_pos = move(pos, command)
                if maybe_new_pos not in visited:
                    visited.add(maybe_new_pos)
                    queue.append(path + (command,))
    return world


def b(program):
    # world = a(program, return_map=True)
    world = cached_world
    start_pos = None
    for row in range(len(world)):
        for col in range(len(world[row])):
            if world[row][col] == "G":
                start_pos = row, col
    visited = set([start_pos])
    queue = deque([(start_pos, 0)])
    while queue:
        pos, minutes = queue.popleft()
        for neighbour in (move(pos, d) for d in range(1, 5)):
            if neighbour not in visited and world[neighbour[0]][neighbour[1]] == " ":
                visited.add(neighbour)
                queue.append((neighbour, minutes + 1))
    return minutes - 1


def main():
    program = list(map(int, open("input15.txt").read().split(",")))
    print(b(program))


if __name__ == "__main__":
    main()
