import chess
import chess.engine
import pygame
import os

# Initialize pygame
pygame.init()

# Constants
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 69, 19)
BOARD_SIZE = 480
SQUARE_SIZE = BOARD_SIZE // 8
ENGINE_PATH = "YOUR_STOCKFISH_PATH_HERE"  # STOCKFISH PATH, READ THE README.md

# Load chess pieces images
def load_piece_images():
    pieces = {}
    colors = ['white', 'black']
    symbols = ['P', 'N', 'B', 'R', 'Q', 'K']
    for color in colors:
        for symbol in symbols:
            piece = symbol if color == 'white' else symbol.lower()
            pieces[piece] = pygame.transform.scale(
                pygame.image.load(os.path.join("pieces", color, f"{piece}.png")),
                (SQUARE_SIZE, SQUARE_SIZE)
            )
    return pieces

# Draw the chess board
def draw_board(screen):
    colors = [LIGHT_BROWN, DARK_BROWN]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw the pieces on the board
def draw_pieces(screen, board, pieces):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row, col = 7 - square // 8, square % 8
            screen.blit(pieces[piece.symbol()], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Get the square clicked by the player
def get_square_at(mouse_pos):
    x, y = mouse_pos
    return chess.square(x // SQUARE_SIZE, 7 - (y // SQUARE_SIZE))

# Main game loop
def main():
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption('Chess Game')
    pieces = load_piece_images()
    board = chess.Board()

    player_color = input("Choose your color (w for white, b for black): ").lower()
    while player_color not in ['w', 'b']:
        player_color = input("Choose your color (w for white, b for black): ").lower()

    with chess.engine.SimpleEngine.popen_uci(ENGINE_PATH) as engine:
        running, player_turn, selected_square = True, player_color == 'w', None
        update_display = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_square = get_square_at(event.pos)
                    piece = board.piece_at(clicked_square)
                    if selected_square is None and piece and piece.color == (player_color == 'w'):
                        selected_square = clicked_square
                    elif selected_square is not None:
                        move = chess.Move(selected_square, clicked_square)
                        if move in board.legal_moves:
                            board.push(move)
                            player_turn, selected_square, update_display = False, None, True

            if update_display:
                draw_board(screen)
                draw_pieces(screen, board, pieces)
                pygame.display.flip()
                update_display = False

            if not player_turn and not board.is_game_over():
                result = engine.play(board, chess.engine.Limit(time=2.0))
                board.push(result.move)
                player_turn, update_display = True, True

            pygame.time.wait(100)

        pygame.quit()

if __name__ == '__main__':
    main()
