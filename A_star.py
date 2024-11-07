class Location:
    """
    This class for coordinates for node on field
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'{self.x} {self.y}'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Field:
    """
    Our field where we are looking for stone that is empty by the default (because we know nothing about it)
    """
    def __init__(self):
        self.list = []
        for i in range(9):
            self.list.append([])
            for j in range(9):
                self.list[i].append(' ')

    def __change_position__(self, location: Location, avenger):
        self.list[location.x][location.y] = avenger


class Node:
    """
    Node - square from our field for algorithm to know
    how much cost the path if we go in this node and
    to know which node was before
    """
    def __init__(self, parent=None, location=None):
        self.parent = parent
        self.location = location

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.location == other.location


def a_star_algorithm(field, start, end):
    """
    :param field: field where we are looking for stone
    :param start: our initial point where we start
    :param end: the coordinates of our goal - stone
    :return: the shortest path to infinity stone or -1 if the path does not exist
    """

    start_node = Node(None, start)
    end_node = Node(None, end)
    open_list = []
    closed_list = []
    previous_node = Node(None, None)
    open_list.append(start_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
            elif item.f == current_node.f:
                if item.h < current_node.h:
                    current_node = item
                    current_index = index
                elif item.h == current_node.h:
                    if item.g <= current_node.g:
                        current_node = item
                        current_index = index

        open_list.pop(current_index)

        if previous_node.location is not None and current_node.parent != previous_node:
            path = []
            current = previous_node.parent
            while current != start_node:
                move(current.location, field)
                current = current.parent
            move(current.location, field)
            current = current_node.parent
            while current != start_node:
                path.append(current)
                current = current.parent
            while len(path) > 0:
                move(path.pop(len(path) - 1).location, field)

        if current_node == end_node:
            return current_node.f

        move(current_node.location, field)
        closed_list.append(current_node)
        previous_node = current_node
        children = []
        for new_position in [(1, 0), (0, 1),(0, -1), (-1, 0)]:  # Adjacent squares

            node_location = Location(current_node.location.x + new_position[0],
                                     current_node.location.y + new_position[1])

            if node_location.x > (len(field.list) - 1) or node_location.x < 0 \
                    or node_location.y > (len(field.list) - 1) or node_location.y < 0:
                continue

            if check_perception_zone(node_location, field):
                continue

            new_node = Node(current_node, node_location)

            children.append(new_node)

        for child in children:

            if child in closed_list:
                continue

            child.g = current_node.g + 1
            child.h = abs(end_node.location.x - child.location.x) + abs(end_node.location.y - child.location.y)
            child.f = child.g + child.h

            if child in open_list and open_list[open_list.index(child)].g < child.g:
                continue

            open_list.append(child)
    return -1


def check_perception_zone(location, field):
    """
    :param location: coordinates of node
    :param field: field where we are looking for stone
    :return: is this node restricted or not
    """
    if field.list[location.x][location.y] in ('M', 'P', 'H', 'T'):
        return True
    return False


def result(weight):
    """
    :param weight: shortest path
     print our path
    """
    print("e " + weight.__str__())


def move(location: Location, field):
    """
    :param location: coordinates where we are going to go
    :param field: field where we are looking for stone
     give interpreter the information where we go
    """
    print("m " + location.__str__())
    get_zone(field)


def get_zone(field):
    """
    :param field: field where we are looking for stone
    take information from interpreter to know about what happens on field around us
    """

    items = int(input())

    if items != 0:
        for i in range(items):
            x, y, avenger = input().split()
            new_location = Location(int(x), int(y))
            field.__change_position__(new_location, avenger)


def main():
    start_point = Location(0, 0)
    variant = int(input())
    x, y = map(int, input().split())
    end_point = Location(x, y)
    field = Field()
    result(a_star_algorithm(field, start_point, end_point))


if __name__ == '__main__':
    main()
