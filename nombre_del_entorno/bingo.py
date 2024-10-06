import pygame
import random

# Dimensiones de la pantalla y colores
WIDTH, HEIGHT = 1024, 768
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
BLUE = (30, 144, 255)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (169, 169, 169)
RED = (255, 0, 0)

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bingo para dos jugadores")
clock = pygame.time.Clock()

# Fuentes
title_font = pygame.font.Font(None, 48)
number_font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 32)

# Crear los tableros de los jugadores
def crear_tablero():
    return set(random.sample(range(1, 76), 25))  # Tablero con 25 números entre 1 y 75

# Simular el sorteo de números
def sortear_numeros():
    return set(random.sample(range(1, 76), 30))  # Se sortean 30 números en total

# Dibujar los tableros de los jugadores
def dibujar_tablero(tablero, coincidencias, x, y, titulo, es_jugador_activo):
    color_titulo = RED if es_jugador_activo else BLACK
    title_surface = title_font.render(titulo, True, color_titulo)
    screen.blit(title_surface, (x + 125 - title_surface.get_width() // 2, y - 50))

    for i, num in enumerate(sorted(tablero)):
        color = GREEN if num in coincidencias else BLUE
        rect_x = x + (i % 5) * 50
        rect_y = y + (i // 5) * 50
        pygame.draw.rect(screen, color, (rect_x, rect_y, 45, 45), border_radius=5)
        num_surface = number_font.render(str(num), True, WHITE)
        screen.blit(num_surface, (rect_x + 22 - num_surface.get_width() // 2, rect_y + 12))

# Mostrar números sorteados
def mostrar_numeros_sorteados(numeros_sorteados):
    title_surface = title_font.render("Números sorteados", True, BLACK)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 450))

    for i, num in enumerate(sorted(numeros_sorteados)):
        x = 200 + (i % 10) * 60
        y = 500 + (i // 10) * 60
        pygame.draw.circle(screen, DARK_GRAY, (x, y), 25)
        num_surface = number_font.render(str(num), True, WHITE)
        screen.blit(num_surface, (x - num_surface.get_width() // 2, y - num_surface.get_height() // 2))

# Mostrar ganador
def mostrar_ganador(coincidencias1, coincidencias2):
    if len(coincidencias1) > len(coincidencias2):
        ganador_text = "¡Jugador 1 gana!"
    elif len(coincidencias2) > len(coincidencias1):
        ganador_text = "¡Jugador 2 gana!"
    else:
        ganador_text = "¡Es un empate!"

    ganador_surface = title_font.render(ganador_text, True, BLACK)
    screen.blit(ganador_surface, (WIDTH // 2 - ganador_surface.get_width() // 2, HEIGHT - 150))

# Crear botón
def crear_boton(text, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, DARK_GRAY, button_rect, border_radius=10)
    text_surface = button_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

# Menú de inicio
def menu_inicio():
    while True:
        screen.fill(LIGHT_GRAY)
        title_surface = title_font.render("Bingo para dos jugadores", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 100))

        jugador1_button = crear_boton("Jugar como Jugador 1", WIDTH // 2 - 100, 300, 200, 50)
        jugador2_button = crear_boton("Jugar como Jugador 2", WIDTH // 2 - 100, 400, 200, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if jugador1_button.collidepoint(event.pos):
                    return 1
                elif jugador2_button.collidepoint(event.pos):
                    return 2

        pygame.display.flip()
        clock.tick(30)

def main():
    jugador_elegido = menu_inicio()
    if jugador_elegido is None:
        return

    tablero_jugador1 = crear_tablero()
    tablero_jugador2 = crear_tablero()
    numeros_sorteados = None
    coincidencias_jugador1 = set()
    coincidencias_jugador2 = set()

    running = True
    mostrar_resultado = False

    while running:
        screen.fill(LIGHT_GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mostrar_resultado:
                    if reiniciar_button.collidepoint(event.pos):
                        return main()
                    elif salir_button.collidepoint(event.pos):
                        running = False
                elif not mostrar_resultado and revelar_button.collidepoint(event.pos):
                    numeros_sorteados = sortear_numeros()
                    coincidencias_jugador1 = tablero_jugador1 & numeros_sorteados
                    coincidencias_jugador2 = tablero_jugador2 & numeros_sorteados
                    mostrar_resultado = True

        dibujar_tablero(tablero_jugador1, coincidencias_jugador1, 100, 100, "Jugador 1", jugador_elegido == 1)
        dibujar_tablero(tablero_jugador2, coincidencias_jugador2, 600, 100, "Jugador 2", jugador_elegido == 2)

        if mostrar_resultado:
            mostrar_numeros_sorteados(numeros_sorteados)
            mostrar_ganador(coincidencias_jugador1, coincidencias_jugador2)
            reiniciar_button = crear_boton("Reiniciar", WIDTH // 2 - 160, HEIGHT - 80, 150, 50)
            salir_button = crear_boton("Salir", WIDTH // 2 + 10, HEIGHT - 80, 150, 50)
        else:
            revelar_button = crear_boton("Revelar resultados", WIDTH // 2 - 100, HEIGHT - 80, 200, 50)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()