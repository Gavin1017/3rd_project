from random import randint, choice


class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]

    def resetMap(self, value):
        for y in range(self.height):
            for x in range(self.width):
                self.setMap(x, y, value)

    def setMap(self, x, y, value):
        if value == 0:
            self.map[y][x] = 0
        elif value == 1:
            self.map[y][x] = 1

    def isVisited(self, x, y):
        return self.map[y][x] != 1

    def showMap(self):
        for row in self.map:
            s = ''
            for entry in row:
                if entry == 0:
                    s += ' 0'
                elif entry == 1:
                    s += ' #'
                else:
                    s += ' X'
            print(s)


# find unvisited adjacent entries of four possible entris
# then add random one of them to checklist and mark it as visited
def checkAdjacentPos(map, x, y, width, height, checklist):
    directions = []
    if x > 0:
        if not map.isVisited(2 * (x - 1) + 1, 2 * y + 1):
            directions.append(0)

    if y > 0:
        if not map.isVisited(2 * x + 1, 2 * (y - 1) + 1):
            directions.append(1)

    if x < width - 1:
        if not map.isVisited(2 * (x + 1) + 1, 2 * y + 1):
            directions.append(2)

    if y < height - 1:
        if not map.isVisited(2 * x + 1, 2 * (y + 1) + 1):
            directions.append(3)

    if len(directions):
        direction = choice(directions)
        # print("(%d, %d) => %s" % (x, y, str(direction)))
        if direction == 0:
            map.setMap(2 * (x - 1) + 1, 2 * y + 1, 0)
            map.setMap(2 * x, 2 * y + 1, 0)
            checklist.append((x - 1, y))
        elif direction == 1:
            map.setMap(2 * x + 1, 2 * (y - 1) + 1, 0)
            map.setMap(2 * x + 1, 2 * y, 0)
            checklist.append((x, y - 1))
        elif direction == 2:
            map.setMap(2 * (x + 1) + 1, 2 * y + 1, 0)
            map.setMap(2 * x + 2, 2 * y + 1, 0)
            checklist.append((x + 1, y))
        elif direction == 3:
            map.setMap(2 * x + 1, 2 * (y + 1) + 1, 0)
            map.setMap(2 * x + 1, 2 * y + 2, 0)
            checklist.append((x, y + 1))
        return True
    else:
        # if not find any unvisited adjacent entry
        return False


# random prim algorithm
def randomPrim(map, width, height):
    # startX, startY = (randint(0, width - 1), randint(0, height - 1))
    startX, startY =1, 1
    # map.setMap(2 * startX + 1, 2 * startY + 1, 0)
    checklist = []
    checklist.append((startX, startY))
    print(choice(checklist))
    while bool(len(checklist)):
        # select a random entry from checklist
        entry = choice(checklist)
        if not checkAdjacentPos(map, entry[0], entry[1], width, height, checklist):
            # the entry has no unvisited adjacent entry, so remove it from checklist
            checklist.remove(entry)


def doRandomPrim(map):
    # set all entries of map to wall(the number is 1)
    map.resetMap(1)
    randomPrim(map, (map.width - 1) // 2, (map.height - 1) // 2)


def run():
    WIDTH = 11
    HEIGHT = 11
    map = Map(WIDTH, HEIGHT)
    doRandomPrim(map)
    map.showMap()


if __name__ == "__main__":
    run()
