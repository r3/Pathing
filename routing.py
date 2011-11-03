class Connection():
    def __init__(self, start, end, price=None, time=None):
        self.start = start
        self.end = end
        self.price = price
        self.time = time

    def __str__(self):
        return "To {end} in {time} minutes. (${price})".format(**self.__dict__)

def dump_connections(log):
    for airport, connections in log.items():
        print("{}:\n \t{}".format(airport, '\n\t'.join(map(str, connections))))
    print()

def construct_connections(txt='data.txt'):
    def feed_lines(txt):
        with open(txt) as data:
            for line in data:
                yield line
    def show_results(func_return, key):
        if func_return is None:
            pass
        else:
            path, cost = func_return
            print("{}: {}".format(key, cost))
            print("Path:\n\t{}".format(', '.join(path)))
            print()

    connections = dict()

    for num, line in enumerate(feed_lines(txt)):
        if line.startswith('='):
            nodeA, nodeB, price, time = line.split()[1:]
            connections.setdefault(nodeA, []).append(
                               Connection(nodeA, nodeB, int(price), int(time)))
            connections.setdefault(nodeB, []).append(
                               Connection(nodeB, nodeA, int(price), int(time)))
        elif line.startswith('-'):
            nodeA, nodeB, price, time = line.split()[1:]
            connections.setdefault(nodeA, []).append(
                               Connection(nodeA, nodeB, int(price), int(time)))
        elif line.startswith('/*'):
            pass
        elif line.startswith('@'):
            nodeA, nodeB = line.split()[1:]
            show_results(dijkstra(nodeA, nodeB, connections, 'time'), 'Time')
        elif line.startswith('$'):
            nodeA, nodeB = line.split()[1:]
            show_results(dijkstra(nodeA, nodeB, connections, 'price'), 'Price')
        elif line.startswith('?'):
            pass  # WTF?
        elif line.startswith('*'):
            dump_connections(connections)
        else:
            raise Exception("Improperly formatted input: line {}.".format(
                            num+1))

def dijkstra(start, destination, connections, key):
    def get_cheapest(cost, visited):
        for node in sorted(cost, key=cost.get):
            if not node in visited:
                return node

    cost = {start:0}
    path = {start:[start]}
    visited = list()
    current = start

    while current != destination:
        visited.append(current)
        try:
            for adjacent in connections[current]:
                traversal_cost = cost[current] + getattr(adjacent, key)
                if cost.get(adjacent.end, float("inf")) > traversal_cost:
                    cost[adjacent.end] = traversal_cost
                    path[adjacent.end] = path[current] + [adjacent.end]
            current = get_cheapest(cost, visited)
        except KeyError:
            print("Error: No path from {} to {}\n".format(start, destination))
            return None
    return path[current], cost[current]

if __name__ == '__main__':
    construct_connections()
