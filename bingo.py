import pygame
import random

# Dimensiones de la pantalla y colores
WIDTH, HEIGHT = 800, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bingo para dos jugadores")
font = pygame.font.Font('freesansbold.ttf', 32)


# Crear los tableros de los jugadores
def crear_tablero():
    return set(random.sample(range(1, 51), 10))  # Tablero con 10 números entre 1 y 50


# Simular el sorteo de números
def sortear_numeros():
    return set(random.sample(range(1, 51), 20))  # Se sortean 20 números en total


# Dibujar los tableros de los jugadores
def dibujar_tablero(tablero, coincidencias, x, y, titulo):
    title_surface = font.render(titulo, True, BLACK)
    screen.blit(title_surface, (x, y - 40))

    for i, num in enumerate(sorted(tablero)):
        color = GREEN if num in coincidencias else BLUE
        rect_x = x + (i % 5) * 60
        rect_y = y + (i // 5) * 60
        pygame.draw.rect(screen, color, (rect_x, rect_y, 50, 50))
        num_surface = font.render(str(num), True, WHITE)
        screen.blit(num_surface, (rect_x + 15, rect_y + 10))


# Mostrar ganador
def mostrar_ganador(coincidencias1, coincidencias2):
    ganador_text = ""
    if len(coincidencias1) > len(coincidencias2):
        ganador_text = "¡Jugador 1 gana!"
    elif len(coincidencias2) > len(coincidencias1):
        ganador_text = "¡Jugador 2 gana!"
    else:
        ganador_text = "¡Es un empate!"

    ganador_surface = font.render(ganador_text, True, BLACK)
    screen.blit(ganador_surface, (WIDTH // 2 - ganador_surface.get_width() // 2, HEIGHT - 100))


def main():
    # Crear tableros para ambos jugadores
    tablero_jugador1 = crear_tablero()
    tablero_jugador2 = crear_tablero()

    # Sortear los números
    numeros_sorteados = sortear_numeros()

    # Calcular coincidencias para ambos jugadores
    coincidencias_jugador1 = tablero_jugador1 & numeros_sorteados
    coincidencias_jugador2 = tablero_jugador2 & numeros_sorteados

    # Ciclo principal del juego
    running = True
    while running:
        screen.fill(WHITE)

        # Dibujar los tableros de los jugadores
        dibujar_tablero(tablero_jugador1, coincidencias_jugador1, 100, 100, "Jugador 1")
        dibujar_tablero(tablero_jugador2, coincidencias_jugador2, 500, 100, "Jugador 2")
        dibujar_tablero(numeros_sorteados, set(), 300, 300, "Números sorteados")
        # Mostrar el ganador
        mostrar_ganador(coincidencias_jugador1, coincidencias_jugador2)

        # Actualizar la pantalla
        pygame.display.flip()

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()
