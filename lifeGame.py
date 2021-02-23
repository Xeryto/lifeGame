from random import *


class Animal:
    def __init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx, foody,
                 pairx,
                 pairy):
        self.lifespan = lifespan
        self.maxLifespan = maxlifespan
        self.gender = gender
        self.x = x
        self.y = y
        self.vision = vision
        self.seeFood = seefood
        self.nearFood = nearfood
        self.foodX = foodx
        self.foodY = foody
        self.seePair = seepair
        self.nearPair = nearpair
        self.pairX = pairx
        self.pairY = pairy

    def goto(self, cordx, cordy):
        r = floyd(self.x, self.y, cordx, cordy)
        if r:
            y = r[-1] // w
            x = r[-1] - y*w
            y += span
            x += span
            sign = landscape[self.y][self.x]
            landscape[self.y][self.x] = "*"
            self.x = x
            self.y = y
            landscape[self.y][self.x] = sign

    def check(self,cordx,cordy,sign):
        if landscape[cordy][cordx] == sign:
            return True
        else:
            return False


class Fox(Animal):
    def __init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx, foody,
                 pairx,
                 pairy):
        Animal.__init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx,
                        foody, pairx,
                        pairy)

    def searchforfood(self):
        for i in range(self.vision * 2 + 1):
            for j in range(self.vision * 2 + 1):
                if landscape[self.y - self.vision + j][self.x - self.vision + i] == "r":
                    self.seeFood = 1
                    self.foodX = self.x - self.vision + i
                    self.foodY = self.y - self.vision + j
                    break
            if self.seeFood == 1:
                break

    def searchforpair(self):
        for i in range(self.vision * 2 + 1):
            for j in range(self.vision * 2 + 1):
                if landscape[self.y - self.vision + j][self.x - self.vision + i] == "f":
                    if self.gender == 0:
                        for l in range(len(foxFem)):
                            a = foxFem[l]
                            if a.x == self.x - self.vision + i and a.y == self.y - self.vision + j and (
                                    a.seePair == 0 or (a.pairX == self.x and a.pairY == self.y)):
                                self.seePair = 1
                                self.pairX = a.x
                                self.pairY = a.y
                                break
                    else:
                        for l in range(len(foxMan)):
                            a = foxMan[l]
                            if a.x == self.x - self.vision + i and a.y == self.y - self.vision + j and (
                                    a.seePair == 0 or (a.pairX == self.x and a.pairY == self.y)):
                                self.seePair = 1
                                self.pairX = a.x
                                self.pairY = a.y
                                break
            if self.seePair == 1:
                break

    def eatfood(self):
        for i in rab:
            for j in i:
                if self.foodX == j.x and self.foodY == j.y:
                    i.remove(j)
                    landscape[j.y][j.x] = "*"


class FemFox(Fox):
    def __init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx, foody,
                 pairx,
                 pairy):
        Fox.__init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx,
                     foody, pairx,
                     pairy)

    def makemove(self):
        if self.lifespan > self.maxLifespan:
            if self.seePair == 1:
                if not (self.check(self.pairX,self.pairY,"f")):
                    self.seePair = 0
                    self.searchforpair()
                if commonfloyd(self.x, self.y, self.pairX, self.pairY) != 1:
                    self.goto(self.pairX, self.pairY)
            else:
                self.seePair = 0
                self.searchforpair()
                if self.seePair != 1:
                    self.searchforfood()
                    if self.seeFood!=1:
                        counter = 0
                        data = []
                        for i in range(3):
                            for j in range(3):
                                if span <= self.x + i - 2 < w + span * 2 and span <= self.y + j - 2 < h + span * 2 and landscape[self.y + j - 2][self.x + i - 2] == "*":
                                    counter+=1
                                    data+=[[self.x+i-2,self.y+j-2]]
                        a = randint(0,counter-1)
                        self.goto(data[a][0],data[a][1])
        elif self.seeFood == 1:
            if not self.check(self.foodX,self.foodY,"r"):
                self.seeFood = 0
                self.searchforfood()
            else:
                if commonfloyd(self.x, self.y, self.foodX, self.foodY) == 1:
                    self.eatfood()
                    self.lifespan += 1
                    self.seeFood = 0
                else:
                    self.goto(self.foodX, self.foodY)
        else:
            self.searchforfood()
            if self.seeFood != 1:
                counter = 0
                data = []
                for i in range(3):
                    for j in range(3):
                        if span <= self.x + i - 2 < w + span * 2 and span <= self.y + j - 2 < h + span * 2 and \
                                landscape[self.y + j - 2][self.x + i - 2] == "*":
                            counter += 1
                            data+=[[self.x+i-2,self.y+j-2]]
                if counter != 0:
                    a = randint(0, counter - 1)
                    self.goto(data[a][0], data[a][1])


class ManFox(Fox):
    def __init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx,
                 foody, pairx, pairy,
                 chanceofpairing):
        Fox.__init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx,
                     foody, pairx,
                     pairy)
        self.chanceOfPairing = chanceofpairing
        self.foxMan = foxMan
        self.foxFem = foxFem

    def pairing(self):
        if randint(0, 100) <= self.chanceOfPairing:
            if randint(0, 100) >= 50:
                counter = 0
                data = []
                for i in range(3):
                    for j in range(3):
                        if span <= self.x + i - 2 < w + span * 2 and span <= self.y + j - 2 < h + span * 2 and \
                                landscape[self.y + j - 2][self.x + i - 2] == "*":
                            counter += 1
                            data+=[[self.x+i-2,self.y+j-2]]
                if counter != 0:
                    a = randint(0, counter - 1)
                    self.foxMan += [ManFox(self.lifespan, self.lifespan, 0, data[a][0], data[a][1], self.vision, 0, 0, 0, 0, 0, 0, 0, 0,
                                       self.chanceOfPairing)]
                    landscape[data[a][1]][data[a][0]] = "f"
            else:
                counter = 0
                data = []
                for i in range(3):
                    for j in range(3):
                        if span <= self.x + i - 2 < w + span * 2 and span <= self.y + j - 2 < h + span * 2 and \
                                landscape[self.y + j - 2][self.x + i - 2] == "*":
                            counter += 1
                            data+=[[self.x+i-2,self.y+j-2]]
                if counter != 0:
                    a = randint(0, counter - 1)
                    self.foxFem += [FemFox(self.lifespan, self.lifespan, 1, data[a][0], data[a][1], self.vision, 0, 0, 0, 0, 0, 0, 0, 0)]
                    landscape[data[a][1]][data[a][0]] = "f"
            return True
        else:
            return False

    def makemove(self):
        if self.lifespan > self.maxLifespan:
            if self.seePair == 1:
                if not (self.check(self.pairX, self.pairY, "f")):
                    self.seePair = 0
                    self.searchforpair()
                if commonfloyd(self.x, self.y, self.pairX, self.pairY) != 1:
                    self.goto(self.pairX, self.pairY)
                else:
                    self.pairing()
                    self.seePair = 0
                    self.lifespan -=1
                    for i in fox:
                        for j in i:
                            if self.pairX == j.x and self.pairY == j.y:
                                j.seePair = 0
                                j.lifespan -=1
            else:
                self.searchforpair()
                if self.seePair != 1:
                    self.searchforfood()
                    if self.seeFood!=1:
                        counter = 0
                        data = []
                        for i in range(3):
                            for j in range(3):
                                if span <= self.x + i - 2 < w + span * 2 and span <= self.y + j - 2 < h + span * 2 and \
                                        landscape[self.y + j - 2][self.x + i - 2] == "*":
                                    counter += 1
                                    data+=[[self.x+i-2,self.y+j-2]]
                        if counter != 0:
                            a = randint(0, counter - 1)
                            self.goto(data[a][0], data[a][1])
        elif self.seeFood == 1:
            if not self.check(self.foodX,self.foodY,"r"):
                self.seeFood = 0
                self.searchforfood()
            if commonfloyd(self.x, self.y, self.foodX, self.foodY) == 1:
                self.eatfood()
                self.lifespan += 1
                self.seeFood = 0
            else:
                self.goto(self.foodX, self.foodY)
        else:
            self.searchforfood()
            if self.seeFood != 1:
                counter = 0
                data = []
                for i in range(3):
                    for j in range(3):
                        if span <= self.x + i - 2 < w + span * 2 and span <= self.y + j - 2 < h + span * 2 and \
                                landscape[self.y + j - 2][self.x + i - 2] == "*":
                            counter += 1
                            data+=[[self.x+i-2,self.y+j-2]]
                if counter != 0:
                    a = randint(0, counter - 1)
                    self.goto(data[a][0], data[a][1])


class Rabbit(Animal):
    def __init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx, foody,
                 pairx,
                 pairy):
        Animal.__init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx,
                        foody, pairx,
                        pairy)

    def searchforfood(self):
        for i in range(self.vision * 2 + 1):
            for j in range(self.vision * 2 + 1):
                if landscape[self.y - self.vision + j][self.x - self.vision + i] == "c":
                    for l in range(len(carrots)):
                        a = carrots[l]
                        if a.x == self.x - self.vision + i and a.y == self.y - self.vision + j and (
                                a.eaten == 0 or a.respTime <= commonfloyd(self.x,self.y,a.x,a.y) or commonfloyd(self.x,self.y,a.x,a.y) == 1):
                            self.seeFood = 1
                            self.foodX = a.x
                            self.foodY = a.y
                            break
            if self.seeFood == 1:
                break

    def searchforpair(self):
        for i in range(self.vision * 2 + 1):
            for j in range(self.vision * 2 + 1):
                if landscape[self.y - self.vision + j][self.x - self.vision + i] == "r":
                    if self.gender == 0:
                        for l in range(len(rabFem)):
                            a = rabFem[l]
                            if a.x == self.x - self.vision + i and a.y == self.y - self.vision + j and (
                                    a.seePair == 0 or (a.pairX == self.x and a.pairY == self.y)):
                                self.seePair = 1
                                self.pairX = a.x
                                self.pairY = a.y
                                break
                    else:
                        for l in range(len(rabMan)):
                            a = rabMan[l]
                            if a.x == self.x - self.vision + i and a.y == self.y - self.vision + j and (
                                    a.seePair == 0 or (a.pairX == self.x and a.pairY == self.y)):
                                self.seePair = 1
                                self.pairX = a.x
                                self.pairY = a.y
                                break
            if self.seePair == 1:
                break

    def eatfood(self):
        for l in range(len(carrots)):
            a = carrots[l]
            if self.foodX == a.x and self.foodY == a.y:
                a.eaten = 1
                a.respAfter = a.respTime - 1


class FemRabbit(Rabbit):
    def __init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx, foody,
                 pairx,
                 pairy):
        Rabbit.__init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx,
                        foody, pairx,
                        pairy)

    def makemove(self):
        if self.lifespan > self.maxLifespan:
            if self.seePair == 1:
                if not self.check(self.pairX,self.pairY,"r"):
                    self.seePair = 0
                    self.searchforpair()
                if commonfloyd(self.x, self.y, self.pairX, self.pairY) != 1:
                    self.goto(self.pairX, self.pairY)
            else:
                self.searchforpair()
                if self.seePair != 1:
                    self.searchforfood()
                    if self.seeFood!=1:
                        counter = 0
                        data = []
                        for i in range(3):
                            for j in range(3):
                                if span <= self.x + i - 2 < w + span * 2 and span <= self.y + j - 2 < h + span * 2 and \
                                        landscape[self.y + j - 2][self.x + i - 2] == "*":
                                    counter += 1
                                    data += [[self.x + i - 2, self.y + j - 2]]
                        if counter != 0:
                            a = randint(0, counter - 1)
                            self.goto(data[a][0], data[a][1])
        elif self.seeFood == 1:
            if commonfloyd(self.x, self.y, self.foodX, self.foodY) == 1:
                self.eatfood()
                self.lifespan += 1
                self.seeFood = 0
            else:
                self.goto(self.foodX, self.foodY)
        else:
            self.searchforfood()
            if self.seeFood != 1:
                counter = 0
                data = []
                for i in range(3):
                    for j in range(3):
                        if span <= self.x + i - 2 < w + span * 2 and span <= self.y + j - 2 < h + span * 2 and \
                                landscape[self.y + j - 2][self.x + i - 2] == "*":
                            counter += 1
                            data += [[self.x + i - 2, self.y + j - 2]]
                if counter!=0:
                    a = randint(0, counter - 1)
                    self.goto(data[a][0], data[a][1])


class ManRabbit(Rabbit):
    def __init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx, foody,
                 pairx, pairy,
                 chanceofpairing):
        Rabbit.__init__(self, lifespan, maxlifespan, gender, x, y, vision, seefood, seepair, nearfood, nearpair, foodx,
                        foody, pairx,
                        pairy)
        self.chanceOfPairing = chanceofpairing
        self.rabMan = rabMan
        self.rabFem = rabFem

    def pairing(self):
        if randint(0, 100) <= self.chanceOfPairing:
            if randint(0, 100) >= 50:
                counter = 0
                data = []
                for i in range(3):
                    for j in range(3):
                        if span <= self.x + i - 2 < w + span * 2 and span <= self.y + j - 2 < h + span * 2 and \
                                landscape[self.y + j - 2][self.x + i - 2] == "*":
                            counter += 1
                            data += [[self.x + i - 2, self.y + j - 2]]
                if counter != 0:
                    a = randint(0, counter - 1)
                    self.rabMan += [ManRabbit(self.lifespan, self.lifespan, 0, data[a][0], data[a][1], self.vision, 0, 0, 0, 0, 0, 0, 0, 0,
                                          self.chanceOfPairing)]
                    landscape[data[a][1]][data[a][0]] = "r"
            else:
                counter = 0
                data = []
                for i in range(3):
                    for j in range(3):
                        if span <= self.x + i - 2 < w + span * 2 and span <= self.y + j - 2 < h + span * 2 and \
                                landscape[self.y + j - 2][self.x + i - 2] == "*":
                            counter += 1
                            data += [[self.x + i - 2, self.y + j - 2]]
                if counter != 0:
                    a = randint(0, counter - 1)
                    self.rabFem += [FemRabbit(self.lifespan, self.lifespan, 1, data[a][0], data[a][1], self.vision, 0, 0, 0, 0, 0, 0, 0, 0)]
                    landscape[data[a][1]][data[a][0]] = "r"
            return True
        else:
            return False

    def makemove(self):
        if self.lifespan > self.maxLifespan:
            if self.seePair == 1:
                if not self.check(self.pairX,self.pairY,"r"):
                    self.seePair = 0
                    self.searchforpair()
                if commonfloyd(self.x, self.y, self.pairX, self.pairY) != 1:
                    self.goto(self.pairX, self.pairY)
                else:
                    self.pairing()
                    self.lifespan-=1
                    self.seePair = 0
                    for i in rab:
                        for j in i:
                            if self.pairX == j.x and self.pairY == j.y:
                                j.lifespan-=1
                                j.seePair = 0
            else:
                self.searchforpair()
                if self.seePair != 1:
                    self.searchforfood()
                    if self.seeFood!=1:
                        counter = 0
                        data = []
                        for i in range(3):
                            for j in range(3):
                                if span <= self.x + i - 2 < w + span * 2 and span <= self.y + j - 2 < h + span * 2 and \
                                        landscape[self.y + j - 2][self.x + i - 2] == "*":
                                    counter += 1
                                    data += [[self.x + i - 2, self.y + j - 2]]
                        if counter != 0:
                            a = randint(0, counter - 1)
                            self.goto(data[a][0], data[a][1])
        elif self.seeFood == 1:
            if commonfloyd(self.x, self.y, self.foodX, self.foodY) == 1:
                self.eatfood()
                self.lifespan += 1
                self.seeFood = 0
            else:
                self.goto(self.foodX, self.foodY)
        else:
            self.searchforfood()
            if self.seeFood != 1:
                counter = 0
                data = []
                for i in range(3):
                    for j in range(3):
                        if span <= self.x + i - 2 < w + span * 2 and span <= self.y + j - 2 < h + span * 2 and \
                                landscape[self.y + j - 2][self.x + i - 2] == "*":
                            counter += 1
                            data += [[self.x + i - 2, self.y + j - 2]]
                if counter != 0:
                    a = randint(0, counter - 1)
                    self.goto(data[a][0], data[a][1])


class Carrot:
    def __init__(self, eaten, resptime, x, y, respafter):
        self.eaten = eaten
        self.respTime = resptime
        self.x = x
        self.y = y
        self.respAfter = respafter

    def makemove(self):
        if self.eaten == 1:
            self.respAfter -= 1
        elif self.respAfter == -1:
            self.eaten = 0


def creatematrix(sx=-1, sy=-1, fx=-1, fy=-1):
    inf = 10 ** 9

    matrix = [[inf for i in range(w * h)] for j in range(w * h)]
    for i in range(w * h):
        matrix[i][i] = 0
    for i in range(span, w + span):
        for j in range(span, h + span):
            if landscape[j][i] == "*" or (i == sx and j == sy) or (i == fx and j == fy):
                for l in range(3):
                    for k in range(3):
                        x = i - 1 + k
                        y = j - 1 + l
                        if (x >= span and y >= span and landscape[y][
                            x] == "*" and x < w + span and y < h + span and (
                                w + span * 2) * j + i != (
                                w + span * 2) * y + x) or (((x == sx and y == sy) or (x == fx and y == fy)) and i!=x and j!=y):
                            matrix[(w + span * 2) * j + i - ((w + 2*span)*span-span) - span * 2 * (j-span+1)][
                                (w + span * 2) * y + x - ((w + 2*span)*span-span) - span * 2 * (y-span+1)] = 1
    return matrix


def commonfloyd(sx, sy, fx, fy):
    inf = 10 ** 9

    matrix = creatematrix(sx, sy, fx, fy)
    n = len(matrix)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if i != j and matrix[i][k] + matrix[k][j] < matrix[i][j]:
                    matrix[i][j] = matrix[i][k] + matrix[k][j]
    if matrix[(w + span * 2) * sy + sx - ((w + 2*span)*span-span) - span * 2 * (sy-span+1)][
            (w + span * 2) * fy + fx - ((w + 2*span)*span-span) - span * 2 * (fy-span+1)] == inf:
        return -1
    else:
        return matrix[(w + span * 2) * sy + sx - ((w + 2*span)*span-span) - span * 2 * (sy-span+1)][
            (w + span * 2) * fy + fx - ((w + 2*span)*span-span) - span * 2 * (fy-span+1)]


def floyd(sx, sy, fx, fy):
    inf = 10 ** 9

    matrix = creatematrix(sx, sy, fx, fy)
    n = len(matrix)
    pred = [[-1 for i in range(n)] for j in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if i != j and matrix[i][k] + matrix[k][j] < matrix[i][j]:
                    matrix[i][j] = matrix[i][k] + matrix[k][j]
                    pred[i][j] = k
    if matrix[(w + span * 2) * sy + sx - ((w + 2 * span) * span - span) - span * 2 * (sy - span + 1)][
        (w + span * 2) * fy + fx - ((w + 2 * span) * span - span) - span * 2 * (fy - span + 1)] == inf:
        return False
    else:
        result = []
        a = (w + span * 2) * fy + fx - ((w + 2 * span) * span - span) - span * 2 * (fy - span + 1)
        while a != -1:
            a = pred[(w + span * 2) * sy + sx - ((w + 2 * span) * span - span) - span * 2 * (sy - span + 1)][a]
            result += [a]
        return result[:-1:]

carrots = []
foxFem = []
foxMan = []
rabFem = []
rabMan = []
fox = [foxFem, foxMan]
rab = [rabFem, rabMan]
print("Введите количество дней для симуляции")
simDays = int(input())
print("Введите размеры поля, начиная с ширины")
w, h = map(int, input().split())
print(
    "Введите количество очков жизни кролика, дальность их взгляда, шанс успешного спаривания - целое число, "
    "отражающее шанс в процентах")
rlifespan, rvision, rchance = map(int, input().split())
print("Введите количество кроликов, начиная с количества женских особей")
rf, rm = map(int, input().split())
print(
    "Введите количество очков жизни лисы, дальность их взгляда, шанс успешного спаривания - целое число, отражающее "
    "шанс в процентах")
flifespan, fvision, fchance = map(int, input().split())
print("Введите количество лис, начиная с количества женских особей")
ff, fm = map(int, input().split())
span = max(rvision, fvision)
landscape = [["*" for i in range(w + span * 2)] for j in range(h + span * 2)]
for i in range(rf):
    a = 0
    b = 0
    while True:
        a = randint(span, w + span - 1)
        b = randint(span, h + span - 1)
        if landscape[b][a] == "*":
            landscape[b][a] = "r"
            break
    rabFem += [FemRabbit(rlifespan, rlifespan, 1, a, b, rvision, 0, 0, 0, 0, 0, 0, 0, 0)]
for i in range(rm):
    a = 0
    b = 0
    while True:
        a = randint(span, w + span - 1)
        b = randint(span, h + span - 1)
        if landscape[b][a] == "*":
            landscape[b][a] = "r"
            break
    rabMan += [ManRabbit(rlifespan, rlifespan, 0, a, b, rvision, 0, 0, 0, 0, 0, 0, 0, 0, rchance)]
for i in range(ff):
    a = 0
    b = 0
    while True:
        a = randint(span, w + span - 1)
        b = randint(span, h + span - 1)
        if landscape[b][a] == "*":
            landscape[b][a] = "f"
            break
    foxFem += [FemFox(flifespan, flifespan, 1, a, b, fvision, 0, 0, 0, 0, 0, 0, 0, 0)]
for i in range(fm):
    a = 0
    b = 0
    while True:
        a = randint(span, w + span - 1)
        b = randint(span, h + span - 1)
        if landscape[b][a] == "*":
            landscape[b][a] = "f"
            break
    foxMan += [ManFox(flifespan, flifespan, 0, a, b, fvision, 0, 0, 0, 0, 0, 0, 0, 0, fchance)]
print("Введите количество часов, за которые будет выростать поле с морковкой после опустошения")
respTime = int(input())
print("Введите количество морковок")
carrAmount = int(input())
print("Введите 1, если хотите, чтобы морковь на полях была уже заранее выросшей")
flag = bool(input())
for i in range(carrAmount):
    a = 0
    b = 0
    while True:
        a = randint(span, w + span - 1)
        b = randint(span, h + span - 1)
        if landscape[b][a] == "*":
            landscape[b][a] = "c"
            break
    if flag:
        carrots += [Carrot(0, respTime, a, b, -1)]
    else:
        carrots += [Carrot(1, respTime, a, b, respTime - 1)]

for i in range(simDays):
    for j in range(24):
        for fh in fox:
            for f in fh:
                f.makemove()
        for rh in rab:
            for r in rh:
                r.makemove()
        for c in carrots:
            c.makemove()
        for k in range(h + span * 2):
            print(*landscape[k])
        print()
    foxesAmount = 0
    rabbitsAmount = 0
    for fh in fox:
        foxesAmount += len(fh)
        for f in fh:
            f.lifespan -= 1
            if f.lifespan == 0:
                landscape[f.y][f.x] = "*"
                fh.remove(f)
    for rh in rab:
        rabbitsAmount += len(rh)
        for r in rh:
            r.lifespan -= 1
            if r.lifespan == 0:
                landscape[r.y][r.x] = "*"
                rh.remove(r)
    print("foxes:", foxesAmount)
    print("rabbits:", rabbitsAmount)