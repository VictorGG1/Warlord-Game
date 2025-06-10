import pygame

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
Y_POSITION = HEIGHT // 2  # Fixed y-level

# Lists to track which guys need to be removed after combat
good_guys_to_remove = []
bad_guys_to_remove = []

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Classes
class Unit:
    def __init__(self):
        self.x = 50
        self.y = Y_POSITION
        self.speed = 3
        self.health = 10
        self.damage = 1
        self.range = 20
        self.last_attack = 0

    def move(self):
        self.x += self.speed

    def attack(self, bad_guy):
        if self.last_attack + 1000 < pygame.time.get_ticks():  # Attack every second
            if abs(self.x - bad_guy.x) < self.range:
                bad_guy.health -= self.damage
                self.last_attack = pygame.time.get_ticks()


class Swordsman(Unit):
    def __init__(self):
        super().__init__()
        self.speed = 3
        self.health = 10
        self.damage = 8
        self.range = 20
        
    def draw(self):
        # Draw swordsman (good guy) as a blue rectangle with a sword, taller than goblin, with legs
        # Body (taller)
        pygame.draw.rect(screen, BLUE, (g.x - 10, g.y - 25, 20, 50))
        # Head
        pygame.draw.circle(screen, (220, 220, 255), (g.x, g.y - 30), 10)
        # Sword
        pygame.draw.line(screen, (160, 160, 160), (g.x + 12, g.y - 5), (g.x + 32, g.y - 5), 5)
        # Arms
        pygame.draw.line(screen, BLUE, (g.x - 10, g.y - 10), (g.x - 25, g.y + 5), 4)
        pygame.draw.line(screen, BLUE, (g.x + 10, g.y - 10), (g.x + 25, g.y + 5), 4)
        # Legs (longer)
        pygame.draw.line(screen, (60, 60, 200), (g.x - 5, g.y + 25), (g.x - 10, g.y + 45), 5)
        pygame.draw.line(screen, (60, 60, 200), (g.x + 5, g.y + 25), (g.x + 10, g.y + 45), 5)

class Archer(Unit):
    def __init__(self):
        super().__init__()
        self.speed = 2
        self.health = 4
        self.damage = 7
        self.range = 200  # Archer can attack from 200px away

    def draw(self):
        # Draw archer (good guy) as a green rectangle with a bow, slimmer and with a quiver
            # Body (slimmer)
            pygame.draw.rect(screen, (34, 139, 34), (g.x - 7, g.y - 25, 14, 45))
            # Head
            pygame.draw.circle(screen, (220, 255, 220), (g.x, g.y - 30), 9)
            # Bow (arc)
            pygame.draw.arc(screen, (139, 69, 19), (g.x + 10, g.y - 20, 20, 40), 3.14/2, 3*3.14/2, 3)
            # Arrow (line)
            pygame.draw.line(screen, (160, 160, 100), (g.x + 20, g.y), (g.x + 32, g.y), 2)
            # Arms
            pygame.draw.line(screen, (34, 139, 34), (g.x - 7, g.y - 10), (g.x - 20, g.y + 5), 3)
            pygame.draw.line(screen, (34, 139, 34), (g.x + 7, g.y - 10), (g.x + 22, g.y + 5), 3)
            # Legs
            pygame.draw.line(screen, (0, 100, 0), (g.x - 3, g.y + 20), (g.x - 8, g.y + 40), 4)
            pygame.draw.line(screen, (0, 100, 0), (g.x + 3, g.y + 20), (g.x + 8, g.y + 40), 4)
            # Quiver (small brown rectangle on back)
            pygame.draw.rect(screen, (139, 69, 19), (g.x - 12, g.y - 18, 5, 18))

class Knight(Unit):
    def __init__(self):
        super().__init__()
        self.speed = 4
        self.health = 20
        self.damage = 10
        self.range = 25

    def draw(self):
        # Draw knight (good guy) as a blue armored figure with a helmet and shield
        # Body (tall, armored)
        pygame.draw.rect(screen, (30, 60, 180), (self.x - 12, self.y - 28, 24, 56))
        # Head (helmet)
        pygame.draw.circle(screen, (180, 180, 220), (self.x, self.y - 36), 13)
        pygame.draw.rect(screen, (100, 100, 160), (self.x - 13, self.y - 36, 26, 13))
        # Visor
        pygame.draw.rect(screen, (60, 60, 120), (self.x - 8, self.y - 36, 16, 7))
        # Shield (left arm)
        pygame.draw.ellipse(screen, (200, 200, 220), (self.x - 28, self.y - 10, 18, 32))
        pygame.draw.ellipse(screen, (120, 120, 180), (self.x - 26, self.y - 6, 14, 24))
        # Sword (right arm)
        pygame.draw.line(screen, (180, 180, 180), (self.x + 12, self.y - 10), (self.x + 38, self.y - 30), 6)
        pygame.draw.line(screen, (220, 220, 220), (self.x + 38, self.y - 30), (self.x + 48, self.y - 40), 4)
        # Arms
        pygame.draw.line(screen, (30, 60, 180), (self.x - 12, self.y - 10), (self.x - 28, self.y + 10), 6)
        pygame.draw.line(screen, (30, 60, 180), (self.x + 12, self.y - 10), (self.x + 28, self.y + 10), 6)
        # Legs (armored)
        pygame.draw.line(screen, (60, 60, 120), (self.x - 5, self.y + 28), (self.x - 10, self.y + 52), 7)
        pygame.draw.line(screen, (60, 60, 120), (self.x + 5, self.y + 28), (self.x + 10, self.y + 52), 7)

class Mage(Unit):
    def __init__(self):
        super().__init__()
        self.speed = 2
        self.health = 6
        self.damage = 15
        self.range = 400 # Mage attacks from a distance

    def draw(self):
        # Draw mage (good guy) as a purple-robed figure with a staff and glowing orb
        # Robe (body)
        pygame.draw.rect(screen, (128, 0, 128), (self.x - 9, self.y - 25, 18, 48))
        # Head
        pygame.draw.circle(screen, (230, 210, 255), (self.x, self.y - 32), 10)
        # Hat (wizard hat)
        pygame.draw.polygon(screen, (90, 0, 120), [(self.x, self.y - 48), (self.x - 12, self.y - 28), (self.x + 12, self.y - 28)])
        # Staff
        pygame.draw.line(screen, (100, 60, 20), (self.x + 10, self.y - 10), (self.x + 10, self.y + 30), 4)
        pygame.draw.circle(screen, (0, 255, 255), (self.x + 10, self.y - 15), 7)
        # Arms
        pygame.draw.line(screen, (128, 0, 128), (self.x - 9, self.y - 10), (self.x - 22, self.y + 8), 3)
        pygame.draw.line(screen, (128, 0, 128), (self.x + 9, self.y - 10), (self.x + 22, self.y + 8), 3)
        # Legs
        pygame.draw.line(screen, (80, 0, 80), (self.x - 4, self.y + 23), (self.x - 8, self.y + 43), 4)
        pygame.draw.line(screen, (80, 0, 80), (self.x + 4, self.y + 23), (self.x + 8, self.y + 43), 4)

class Goblin(Unit):
    def __init__(self):
        super().__init__()
        self.x = WIDTH - 50
        self.speed = -3
        self.health = 8
        self.range = 15
        self.damage = 3

    def draw(self):
        # Draw goblin (bad guy)
        # Head
        pygame.draw.circle(screen, RED, (b.x, b.y), 15)
        # Ears
        pygame.draw.polygon(screen, (80, 0, 0), [(b.x - 18, b.y - 8), (b.x - 28, b.y - 18), (b.x - 10, b.y - 15)])
        pygame.draw.polygon(screen, (80, 0, 0), [(b.x + 18, b.y - 8), (b.x + 28, b.y - 18), (b.x + 10, b.y - 15)])
        # Eyes
        pygame.draw.circle(screen, (0, 0, 0), (b.x - 5, b.y - 3), 3)
        pygame.draw.circle(screen, (0, 0, 0), (b.x + 5, b.y - 3), 3)
        # Mouth
        pygame.draw.arc(screen, (0, 0, 0), (b.x - 7, b.y + 2, 14, 8), 3.5, 6.0, 2)
        # Body
        pygame.draw.rect(screen, (120, 30, 30), (b.x - 10, b.y + 15, 20, 25))
        # Arms
        pygame.draw.line(screen, (120, 30, 30), (b.x - 10, b.y + 20), (b.x - 25, b.y + 30), 4)
        pygame.draw.line(screen, (120, 30, 30), (b.x + 10, b.y + 20), (b.x + 25, b.y + 30), 4)
        # Legs
        pygame.draw.line(screen, (80, 0, 0), (b.x - 5, b.y + 40), (b.x - 10, b.y + 55), 4)
        pygame.draw.line(screen, (80, 0, 0), (b.x + 5, b.y + 40), (b.x + 10, b.y + 55), 4)

class Ogre(Unit):
    def __init__(self):
        super().__init__()
        self.x = WIDTH - 50
        self.speed = -2
        self.health = 30
        self.range = 30
        self.damage = 6

    def draw(self):    # Draw ogre (bad guy) - bigger, more menacing, with club and tusks
        # Body
        pygame.draw.ellipse(screen, (100, 60, 20), (self.x - 28, self.y - 32, 56, 64))
        # Head
        pygame.draw.circle(screen, (180, 140, 90), (self.x, self.y - 48), 26)
        # Eyes
        pygame.draw.circle(screen, (0, 0, 0), (self.x - 8, self.y - 52), 4)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 8, self.y - 52), 4)
        # Eyebrows
        pygame.draw.line(screen, (60, 40, 10), (self.x - 14, self.y - 58), (self.x - 2, self.y - 56), 3)
        pygame.draw.line(screen, (60, 40, 10), (self.x + 2, self.y - 56), (self.x + 14, self.y - 58), 3)
        # Mouth (snarl)
        pygame.draw.arc(screen, (0, 0, 0), (self.x - 12, self.y - 38, 24, 16), 3.5, 6.0, 3)
        # Tusks
        pygame.draw.polygon(screen, (255, 255, 255), [(self.x - 7, self.y - 28), (self.x - 11, self.y - 18), (self.x - 3, self.y - 22)])
        pygame.draw.polygon(screen, (255, 255, 255), [(self.x + 7, self.y - 28), (self.x + 11, self.y - 18), (self.x + 3, self.y - 22)])
        # Arms (thick)
        pygame.draw.line(screen, (100, 60, 20), (self.x - 28, self.y - 10), (self.x - 48, self.y + 36), 12)
        pygame.draw.line(screen, (100, 60, 20), (self.x + 28, self.y - 10), (self.x + 54, self.y + 36), 12)
        # Club (in right hand)
        pygame.draw.line(screen, (120, 80, 40), (self.x + 54, self.y + 36), (self.x + 74, self.y + 66), 16)
        pygame.draw.circle(screen, (90, 60, 30), (self.x + 74, self.y + 66), 12)
        # Legs (short, thick)
        pygame.draw.line(screen, (80, 40, 10), (self.x - 12, self.y + 32), (self.x - 18, self.y + 72), 10)
        pygame.draw.line(screen, (80, 40, 10), (self.x + 12, self.y + 32), (self.x + 18, self.y + 72), 10)

# Game loop
good_guys = []
bad_guys = []
win_condition = 0
running = True

while running:
    # Draw background (simple grass and sky)
    screen.fill((135, 206, 235))  # Sky blue
    pygame.draw.rect(screen, (34, 139, 34), (0, Y_POSITION + 40, WIDTH, HEIGHT - (Y_POSITION + 40)))  # Grass
    pygame.draw.rect(screen, (139, 69, 19), (0, Y_POSITION + 35, WIDTH, 10))  # Dirt path

    # Draw sun
    pygame.draw.circle(screen, (255, 255, 0), (100, 100), 60)
    for i in range(12):
        angle = i * 30
        x1 = 100 + int(80 * pygame.math.Vector2(1, 0).rotate(angle).x)
        y1 = 100 + int(80 * pygame.math.Vector2(1, 0).rotate(angle).y)
        x2 = 100 + int(110 * pygame.math.Vector2(1, 0).rotate(angle).x)
        y2 = 100 + int(110 * pygame.math.Vector2(1, 0).rotate(angle).y)
        pygame.draw.line(screen, (255, 255, 0), (x1, y1), (x2, y2), 6)

    # Draw clouds
    pygame.draw.ellipse(screen, (255, 255, 255), (200, 80, 120, 50))
    pygame.draw.ellipse(screen, (255, 255, 255), (260, 60, 100, 40))
    pygame.draw.ellipse(screen, (255, 255, 255), (600, 120, 140, 60))
    pygame.draw.ellipse(screen, (255, 255, 255), (650, 100, 90, 40))

    # Draw distant mountains
    pygame.draw.polygon(screen, (120, 120, 160), [(0, Y_POSITION + 40), (120, 200), (240, Y_POSITION + 40)])
    pygame.draw.polygon(screen, (100, 100, 140), [(180, Y_POSITION + 40), (350, 160), (520, Y_POSITION + 40)])
    pygame.draw.polygon(screen, (90, 90, 120), [(500, Y_POSITION + 40), (650, 180), (800, Y_POSITION + 40)])

    # Draw trees
    for tx in range(60, WIDTH, 180):
        pygame.draw.rect(screen, (101, 67, 33), (tx, Y_POSITION + 10, 18, 40))
        pygame.draw.circle(screen, (34, 139, 34), (tx + 9, Y_POSITION + 5), 28)
        pygame.draw.circle(screen, (0, 100, 0), (tx + 9, Y_POSITION - 10), 20)

    # Draw flowers
    for fx in range(30, WIDTH, 80):
        pygame.draw.circle(screen, (255, 192, 203), (fx, Y_POSITION + 70), 5)
        pygame.draw.circle(screen, (255, 255, 0), (fx, Y_POSITION + 70), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn new characters at intervals
    keys = pygame.key.get_pressed()
    GOOD_GUY_SPAWN_INTERVAL = 54
    if not hasattr(pygame, 'last_good_guy_spawn'):
        pygame.last_good_guy_spawn = pygame.time.get_ticks()
    now = pygame.time.get_ticks()
    if (now - pygame.last_good_guy_spawn) > GOOD_GUY_SPAWN_INTERVAL:
        if keys[pygame.K_1]:
            good_guys.append(Swordsman())
            pygame.last_good_guy_spawn = now
        elif keys[pygame.K_2]:
            good_guys.append(Archer())
            pygame.last_good_guy_spawn = now
        elif keys[pygame.K_3]:
            good_guys.append(Knight())
            pygame.last_good_guy_spawn = now
        elif keys[pygame.K_4]:
            good_guys.append(Mage())
            pygame.last_good_guy_spawn = now
    
    # Spawn bad guys at fixed intervals, max 3 at a time
    OGRE_SPAWN_INTERVAL = 2000  # seconds
    if not hasattr(pygame, 'last_ogre_spawn'):
        pygame.last_ogre_spawn = pygame.time.get_ticks()
    now = pygame.time.get_ticks()

    # Always spawn Ogre every 2 seconds, max 3 bad guys at a time
    if (now - pygame.last_ogre_spawn) > OGRE_SPAWN_INTERVAL:
        bad_guys.append(Ogre())
        pygame.last_ogre_spawn = now

    # Spawn a goblin every 1.5 seconds, max 3 bad guys at a time
    GOBLIN_SPAWN_INTERVAL = 1500
    if not hasattr(pygame, 'last_goblin_spawn'):
        pygame.last_goblin_spawn = pygame.time.get_ticks()
    if (now - pygame.last_goblin_spawn) > GOBLIN_SPAWN_INTERVAL:
        bad_guys.append(Goblin())
        pygame.last_goblin_spawn = now
    
    for g in good_guys:
        g.draw()

    for b in bad_guys:
        b.draw()
    
    # Combat logic
    good_guys_to_remove.clear()
    bad_guys_to_remove.clear()

    for g in good_guys:
        g.has_attacked = False
    
    for b in bad_guys:
        b.has_attacked = False

    for g in good_guys:
        for b in bad_guys:
            g.attack(b)
            if isinstance(g, Mage) and abs(g.x - b.x) < g.range and g.last_attack + 1000 >= pygame.time.get_ticks():
                # Draw explosion effect on enemy
                pygame.draw.circle(screen, (255, 140, 0), (b.x, b.y), 32)
                pygame.draw.circle(screen, (255, 255, 0), (b.x, b.y), 18)
                pygame.draw.circle(screen, (255, 255, 255), (b.x, b.y), 8)
            b.attack(g)
    

    for g in good_guys:
        if g.health <= 0:
            good_guys.remove(g)

    for b in bad_guys:
        if b.health <= 0:
            bad_guys.remove(b)

    for g in good_guys:
        if g.last_attack + 1000 < pygame.time.get_ticks():
            g.move()
        
    for b in bad_guys:
        if b.last_attack + 1000 < pygame.time.get_ticks():
            b.move()

    # Winning condition
    if sum(g.x > WIDTH - 10 for g in good_guys) >= 1:
        font = pygame.font.SysFont(None, 72)
        text = font.render("Victory!", True, (255, 255, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Small delay before exit
        running = False

    # Losing condition
    if sum(b.x < 10 for b in bad_guys) >= 1:
        font = pygame.font.SysFont(None, 72)
        text = font.render("You lose!", True, (128, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Small delay before exit
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()