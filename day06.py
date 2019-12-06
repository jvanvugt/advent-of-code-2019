from collections import defaultdict, deque


def a(graph):
    total_orbits = 0
    parents = {}
    for node, children in graph.items():
        for child in children:
            parents[child] = node

    for node in graph:
        while node != "COM":
            node = parents[node]
            total_orbits += 1
    return total_orbits


def b(graph):
    neighbours = defaultdict(list)
    for node, children in graph.items():
        for child in children:
            neighbours[node].append(child)
            neighbours[child].append(node)
    start = "YOU"
    queue = deque([(start, 0)])
    visited = {start}
    while len(queue) > 0:
        pos, steps = queue.pop()
        if pos == "SAN":
            return steps - 2
        for neighbour in neighbours[pos]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.appendleft((neighbour, steps + 1))


def main():
    lines = open("input06.txt").read().splitlines()
    graph = defaultdict(list)
    for line in lines:
        parent, child = line.split(")")
        graph[parent].append(child)
        graph[child]
    print(b(graph))


if __name__ == "__main__":
    main()
