import pygame

def show_round_status(balance: int, spin: int, net_change: int) -> None:
    pygame.init()
    screen = pygame.display.set_mode((420, 260))
    pygame.display.set_caption("Roulette Round Status")

    font = pygame.font.SysFont(None, 32)
    clock = pygame.time.Clock()

    start_ticks = pygame.time.get_ticks()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # auto-close after 3 seconds
        if pygame.time.get_ticks() - start_ticks > 3000:
            running = False

        screen.fill((0, 80, 0))

        lines = [
            f"Balance: {balance}",
            f"Last spin: {spin}",
            f"Net change: {net_change}",
            "Window closes after 3 sec",
        ]
        y = 50
        for text in lines:
            surf = font.render(text, True, (255, 255, 255))
            screen.blit(surf, (40, y))
            y += 40

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
