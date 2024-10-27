import chess
import chess.engine
import pygame
import os

# Initialize pygame
pygame.init()

# Set up the colors for the chessboard
LIGHT_BROWN = (222, 184, 135)  # Light brown for light squares
DARK_BROWN = (139, 69, 19)     # Dark brown for dark squares

# Set up the dimensions of the board
BOARD_SIZE = 480
SQUARE_SIZE = BOARD_SIZE // 8

# Load chess pieces images
def load_piece_images():
    pieces = {}
    # Load white pieces
    for piece in ['P', 'N', 'B', 'R', 'Q', 'K']:
        pieces[piece] = pygame.transform.scale(
            pygame.image.load(os.path.join("pieces", "white", f"{piece}.png")),
            (SQUARE_SIZE, SQUARE_SIZE)
        )
    # Load black pieces
    for piece in ['p', 'n', 'b', 'r', 'q', 'k']:
        pieces[piece] = pygame.transform.scale(
            pygame.image.load(os.path.join("pieces", "black", f"{piece}.png")),
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
            row = 7 - (square // 8)
            col = square % 8
            screen.blit(pieces[piece.symbol()], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Get the square clicked by the player
def get_square_at(mouse_pos):
    x, y = mouse_pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)

# Main loop for the GUI
def main():
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption('Chess Game')

    # Load the piece images
    pieces = load_piece_images()

    # Create a chess board
    board = chess.Board()

    # Ask the player to choose white or black
    player_color = None
    while player_color not in ['w', 'b']:
        player_input = input("Choose your color (w for white, b for black): ").lower()
        if player_input in ['w', 'b']:
            player_color = player_input

    # Set the path to the Stockfish engine executable
    engine_path = "C:/Users/Agent Ezra/OneDrive/Pict/Docs/Ezra Chess/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2.exe"

    # Start the engine
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        running = True
        selected_square = None  # To keep track of the first click (selected piece)
        player_turn = (player_color == 'w')  # White starts the game

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Player's turn (handle mouse clicks to move pieces)
                if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_square = get_square_at(event.pos)
                    piece = board.piece_at(clicked_square)

                    if selected_square is None:
                        # First click: select the piece
                        if piece and piece.color == (player_color == 'w'):
                            selected_square = clicked_square
                    else:
                        # Second click: attempt to move the piece
                        move = chess.Move(selected_square, clicked_square)
                        if move in board.legal_moves:
                            board.push(move)
                            player_turn = False  # Now it's Stockfish's turn
                        selected_square = None  # Reset the selection

            # Draw the chess board and pieces
            draw_board(screen)
            draw_pieces(screen, board, pieces)

            # Stockfish's turn
            if not player_turn and not board.is_game_over():
                result = engine.play(board, chess.engine.Limit(time=2.0))  # 2 seconds per move
                board.push(result.move)
                player_turn = True  # After Stockfish's move, it's the player's turn again

            # Update the display
            pygame.display.flip()

            pygame.time.wait(100)

        pygame.quit()

if __name__ == '__main__':
    main()
