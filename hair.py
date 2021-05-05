import pygame

GRAVITY = 2
MASS = 50
K = 10
TIMESTEP = 0.20
DAMPING = 10

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
ORANGE = [219, 121, 22]
BACKGROUND_COLOR = [240, 250, 255]


SIZE = (800, 800)


class Segment:
    def __init__(self, pos):
        self.coords = pos
        self.velocity = [0, 0]
        self.damping_force = [0, 0]
        self.spring_force = [0, 0]


class Hair:
    def __init__(self, screen, num_segments, base_pos, x_displacement, y_displacement, anchor):
        self.screen = screen
        self.base = base_pos

        self.segments = []

        for i in range(num_segments + 1):
            coords = [base_pos[0] + i * x_displacement, base_pos[1] + i * y_displacement]
            segment = Segment(coords)
            self.segments.append(segment)


        # Anchors:
        self.anchor_x = anchor[0]   # center of gravity
        self.anchor_y = anchor[1]   # length of the the segment of hair

        self.draw_me()

    def draw_me(self):
        for i in range(1, len(self.segments)):
            pygame.draw.line(self.screen, ORANGE, (self.segments[i - 1]).coords, (self.segments[i]).coords, 2)


    def update(self):
        for i in range(1, len(self.segments)):
            if i == 1:
                (self.segments[i]).spring_force[0] = -K * ((self.segments[i]).coords[0] - self.anchor_x)
                (self.segments[i]).spring_force[1] = -K * ((self.segments[i]).coords[1] - self.anchor_y)
            else:
                (self.segments[i]).spring_force[0] = -K * ((self.segments[i]).coords[0] - (self.segments[i-1]).coords[0])
                (self.segments[i]).spring_force[1] = -K * ((self.segments[i]).coords[1] - (self.segments[i-1]).coords[1] - self.anchor_y)

            (self.segments[i]).damping_force[0] = DAMPING * (self.segments[i]).velocity[0]
            (self.segments[i]).damping_force[1] = DAMPING * (self.segments[i]).velocity[1]

        for i in range(1, len(self.segments)):
            if i == (len(self.segments) - 1):  # end of the hair => no forces affecting from below
                forceX = (self.segments[i]).spring_force[0] - (self.segments[i]).damping_force[0]
                forceY = (self.segments[i]).spring_force[1] + MASS * GRAVITY - (self.segments[i]).damping_force[1]
            else:
                forceX = (self.segments[i]).spring_force[0] - (self.segments[i]).damping_force[0]                   - (self.segments[i+1]).spring_force[0] + (self.segments[i+1]).damping_force[0]
                forceY = (self.segments[i]).spring_force[1] + MASS * GRAVITY - (self.segments[i]).damping_force[1]  - (self.segments[i+1]).spring_force[1] + (self.segments[i+1]).damping_force[1]


            accelerationX = forceX / MASS
            accelerationY = forceY / MASS

            (self.segments[i]).velocity[0] += accelerationX * TIMESTEP
            (self.segments[i]).velocity[1] += accelerationY * TIMESTEP

            (self.segments[i]).coords[0] += (self.segments[i]).velocity[0] * TIMESTEP
            (self.segments[i]).coords[1] += (self.segments[i]).velocity[1] * TIMESTEP


def run_game():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Hair Animation")

    clock = pygame.time.Clock()
    running = True

    num_hairs = 20
    x = 300
    y = 50
    x_displacement = 8
    y_displacement = 0
    segment_len = 2
    num_segments = 10

    hairs = []
    for i in range(num_hairs):
        # create a hair
        pos = [x + i * x_displacement, y + i * y_displacement]
        anchor = [x + i * x_displacement, segment_len]

        # Hair(screen, # of segments per hair, position for attachment, x displacement, y displacement, anchor(center of gravity, length of each segment))
        hair = Hair(screen, num_segments, pos, -50, +50, anchor)
        hairs.append(hair)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for hair in hairs:
            hair.update()

        screen.fill(BACKGROUND_COLOR)

        for hair in hairs:
            hair.draw_me()

        pygame.display.flip()
        clock.tick(60)


run_game()
pygame.quit()


