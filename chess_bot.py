import chess
import chess.engine
import pygame
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 69, 19)
BOARD_SIZE = 480
SQUARE_SIZE = BOARD_SIZE // 8
FPS = 60
ENGINE_PATH = "YOUR_CHESS_ENGINE_PATH_HERE"

# Load chess pieces images
def load_piece_images():
    pieces = {}
    colors = ['white', 'black']
    symbols = ['P', 'N', 'B', 'R', 'Q', 'K']
    for color in colors:
        for symbol in symbols:
            piece = symbol if color == 'white' else symbol.lower()
            try:
                pieces[piece] = pygame.transform.scale(
                    pygame.image.load(os.path.join("pieces", color, f"{piece}.png")),
                    (SQUARE_SIZE, SQUARE_SIZE)
                )
            except FileNotFoundError:
                print(f"Image for {piece} not found.")
    return pieces

# Load sound effects
move_sound = pygame.mixer.Sound("Voice1.wav")
capture_sound = pygame.mixer.Sound("Voice2.wav")

# Draw the chess board
def draw_board(screen):
    colors = [LIGHT_BROWN, DARK_BROWN]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw legal move highlights
def draw_legal_moves(screen, legal_moves):
    for move in legal_moves:
        col, row = move.to_square % 8, 7 - move.to_square // 8
        pygame.draw.circle(screen, (0, 255, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)

# Draw the pieces on the board
def draw_pieces(screen, board, pieces):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row, col = 7 - square // 8, square % 8
            screen.blit(pieces.get(piece.symbol(), None), pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Get the square clicked by the player
def get_square_at(mouse_pos):
    x, y = mouse_pos
    return chess.square(x // SQUARE_SIZE, 7 - (y // SQUARE_SIZE))

# Main game loop
def main():
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE), pygame.RESIZABLE)
    pygame.display.set_caption('Chess Game')
    clock = pygame.time.Clock()
    pieces = load_piece_images()
    board = chess.Board()

    player_color = ""
    while player_color not in ['w', 'b']:
        player_color = input("Choose your color (w for white, b for black): ").lower()

    with chess.engine.SimpleEngine.popen_uci(ENGINE_PATH) as engine:
        running, player_turn = True, player_color == 'w'
        selected_square = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_square = get_square_at(event.pos)
                    if selected_square is None and board.piece_at(clicked_square) and board.piece_at(clicked_square).color == (player_color == 'w'):
                        selected_square = clicked_square
                    elif selected_square is not None:
                        move = chess.Move(selected_square, clicked_square)
                        if move in board.legal_moves:
                            if board.is_capture(move):
                                capture_sound.play()
                            else:
                                move_sound.play()
                            board.push(move)
                            player_turn = False
                        selected_square = None

            draw_board(screen)
            draw_pieces(screen, board, pieces)
            if selected_square:
                legal_moves = [move for move in board.legal_moves if move.from_square == selected_square]
                draw_legal_moves(screen, legal_moves)
            pygame.display.flip()

            if not player_turn and not board.is_game_over():
                result = engine.play(board, chess.engine.Limit(time=2.0))
                board.push(result.move)
                move_sound.play()
                player_turn = True

            clock.tick(FPS)

        pygame.quit()

if __name__ == '__main__':
    main()
