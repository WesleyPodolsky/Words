import pygame

def main_loop(screen, frame_rate=60):
    """Main loop generator function.

    Args:
        screen (pygame.Surface): The display surface.
        frame_rate (int): The frame rate to cap the loop at.
    """
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((0, 0, 139))  # Clear screen with deep blue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        yield

        pygame.display.flip()
        clock.tick(frame_rate)