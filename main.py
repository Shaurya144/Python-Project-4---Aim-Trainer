import math
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")
TARGET_INCREMENT = 400 # This controls how fast the next target appears onto the screen
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_COLOR = (0, 25, 40)
LIVES = 3
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

class Target:
    MAX_SIZE = 30 # the lower the max size the harder the game
    GROWTH_RATE = 0.1 # the lower the growth rate the easier the game
    COLOR = "blue"
    SECOND_COLOR = "white"

    def __init__(self, x, y): # 
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True # if hit or reaches max height it becomes false

    def update(self): # to tell us whether the circles should be growing o r shrinking
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE

        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8) # this causes the rings 
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        dis = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return dis <= self.size


def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)


def FormatTime(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}: {seconds:02d}.{milli}"


def DrawTopBar(win, ElaspedTime, TargetHit, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(
        f"Time: {FormatTime(ElaspedTime)}", 1, "black")

    speed = round(TargetHit / ElaspedTime, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {TargetHit}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))


def EndScreen(win, ElaspedTime, TargetHit, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(
        f"Time: {FormatTime(ElaspedTime)}", 1, "white")

    speed = round(TargetHit / ElaspedTime, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits: {TargetHit}", 1, "white")

    accuracy = round(TargetHit / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(time_label, (GetMiddle(time_label), 100))
    win.blit(speed_label, (GetMiddle(speed_label), 200))
    win.blit(hits_label, (GetMiddle(hits_label), 300))
    win.blit(accuracy_label, (GetMiddle(accuracy_label), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()


def GetMiddle(surface):
    return WIDTH / 2 - surface.get_width()/2


def Main(): # Gets a window to the screen and where we draw all the images
    run = True
    targets = []
    clock = pygame.time.Clock()

    TargetHit = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        ElaspedTime = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT: # create new target with new x and y cordinates
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                TargetHit +=1

        if misses >= LIVES:
            EndScreen(WIN, ElaspedTime, TargetHit, clicks)

        draw(WIN, targets)
        DrawTopBar(WIN, ElaspedTime, TargetHit, misses)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    Main()
