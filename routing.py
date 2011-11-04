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
        print("{}:\n \t{}\n".format(airport, '\n\t'.join(map(str, connections))))

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
            print("Path:\n\t{}\n".format(', '.join(path)))

    connections = dict()

    for num, line in enumerate(feed_lines(txt)):
        if line.startswith('='):
            nodeA, nodeB, price, time = line.split()[1:5]
            connections.setdefault(nodeA, []).append(
                               Connection(nodeA, nodeB, int(price), int(time)))
            connections.setdefault(nodeB, []).append(
                               Connection(nodeB, nodeA, int(price), int(time)))
        elif line.startswith('-'):
            nodeA, nodeB, price, time = line.split()[1:5]
            connections.setdefault(nodeA, []).append(
                               Connection(nodeA, nodeB, int(price), int(time)))
        elif line.startswith('/*'):
            pass
        elif line.startswith('@'):
            nodeA, nodeB = line.split()[1:3]
            show_results(pathing(nodeA, nodeB, connections, 'time'), 'Time')
        elif line.startswith('$'):
            nodeA, nodeB = line.split()[1:3]
            show_results(pathing(nodeA, nodeB, connections, 'price'), 'Price')
        elif line.startswith('?'):
            pass  # WTF?
        elif line.startswith('*'):
            dump_connections(connections)
        else:
            raise Exception("Improperly formatted input: line {}.".format(
                            num+1))
    return connections

def pathing(start, destination, connections, key):
    def serve_cheapest(cost, visited):
        for node in sorted(cost, key=cost.get):
            if (not node in visited) and (node in connections):
                yield node

    cost = {start:0}
    path = {start:[start]}
    visited = list()
    current = start

    while visited != connections.keys():
        visited.append(current)
        available = connections[current]
        if available:
            for adjacent in available:
                traversal_cost = cost[current] + getattr(adjacent, key)
                if cost.get(adjacent.end, float("inf")) > traversal_cost:
                    cost[adjacent.end] = traversal_cost
                    path[adjacent.end] = path[current] + [adjacent.end]
                pool = serve_cheapest(cost, visited)
        try:
            current = next(pool)
        except StopIteration:
            if destination in path:
                return path[destination], cost[destination]
            else:
                print("Cannot reach {} from {}.\n".format(destination, start))
                return None

    return path[current], cost[current]

if __name__ == '__main__':
    construct_connections()
