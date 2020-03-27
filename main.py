import pygame

START = (10, 10)
END = (380, 380)
DIRECTIONS = [[10, 0], [10, 10], [0, 10], [-10, 10], [-10, 0], [-10, -10], [0, -10], [10, -10]]
BLOCKED_CELLS = [(10,20),(20, 20),(30,20),(40,20),(50,20),(60,20),
                 (100,100),(110,100),(120,100),(130,100),(140,100),(150,100),(160,100),
                 (250,100),(250,100),(250,110),(250,120),(250,130),(250,140),(250,150),
                 (250,160),(250,170),(250,180),(250,190),(250,200),(250,210),(250,220),(250,230),
                 (240,230),(230,230),(220,230),(210,230),]


def draw_maze(screen):
    # pygame.draw.lines(screen, (255, 255, 255), False, [(35, 39), (234, 39)], 10)
    # pygame.draw.lines(screen, (255, 255, 255), False, [(55, 249), (334, 249)], 10)
    for b in BLOCKED_CELLS:
        pygame.draw.rect(screen, (255, 255, 255), [b[0], b[1], 10, 10])


def start_node(screen):
    pygame.draw.rect(screen, (255, 255, 0), [START[0], START[1], 10, 10])


def goal_node(screen):
    pygame.draw.rect(screen, (0, 255, 0), [END[0], END[1], 10, 10])


class Node:

    def __init__(self, current_pos, previous_pos, g, h):
        self.current_pos = current_pos
        self.previous_pos = previous_pos
        self.h = h
        self.g = g

    def f(self):
        return self.h + self.g


def heuristic_cost(node_pos):
    cost = abs(node_pos[0] - END[0]) + abs(node_pos[1] - END[1])
    return (cost / 10)


def get_best_node(open_set):
    firstEnter = True

    for node in open_set.values():
        if firstEnter or node.f() < bestF:
            firstEnter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode


def get_adjacent_node(node):
    list_of_node = []

    for dir in DIRECTIONS:
        new_pos = (node.current_pos[0] + dir[0], node.current_pos[1] + dir[1])
        if 0 <= new_pos[0] <= 390 and 0 <= new_pos[1] <= 390:
            list_of_node.append(Node(new_pos, node.current_pos, node.g + 1, heuristic_cost(new_pos)))

    return list_of_node


def min_path(closed_set):
    path = []
    node = closed_set[str(END)]
    while node.current_pos != START:
        if node.current_pos != END:
            path.insert(0, node.current_pos)
        node = closed_set[str(node.previous_pos)]
    return path


def is_blocked(node):
    blocked = False
    if node.current_pos in BLOCKED_CELLS:
        blocked = True
    return blocked


def main(start_pos):
    open_set = {str(start_pos): Node(start_pos, start_pos, 0, heuristic_cost(start_pos))}
    closed_set = {}

    while True:
        test_node = get_best_node(open_set)
        closed_set[str(test_node.current_pos)] = test_node

        if test_node.current_pos == END:
            return min_path(closed_set)

        adj_node = get_adjacent_node(test_node)

        for node in adj_node:
            if is_blocked(node) or str(node.current_pos) in closed_set.keys() or str(
                    node.current_pos) in open_set.keys() and open_set[
                str(node.current_pos)].f() < node.f():
                continue
            open_set[str(node.current_pos)] = node
        del open_set[str(test_node.current_pos)]


path = main(START)

# game variable
fps = 10
velocity_x = 10
velocity_y = 10

# initiate pygame module--- required
pygame.init()

# screen
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Short path search')
running = True

# clock
clock = pygame.time.Clock()

# main loop
while running:
    key_press = False

    # key event
    for event in pygame.event.get():
        # closing events
        if event.type == pygame.QUIT:
            running = False

    # draw maze
    draw_maze(screen)
    start_node(screen)
    goal_node(screen)

    for p in path:
        pygame.draw.rect(screen, (255, 0, 255), [p[0], p[1], 10, 10])

    # update display--- required
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
