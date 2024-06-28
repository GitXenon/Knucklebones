import random
import time
from faker import Faker

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()


class Board:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.grid = [[None for _ in range(3)] for _ in range(3)]

    def update_column(self, column_nb, dice_roll):
        for i in range(3):
            if self.grid[int(column_nb) - 1][i] == None:
                self.grid[int(column_nb) - 1][i] = dice_roll
                return True
        return False

    def is_valid_move(self, column_nb):
        return any(cell is None for cell in self.grid[int(column_nb) - 1])

    def column_score(self):
        column_score = [0, 0, 0]
        for i in range(3):
            value_counts = {}
            for value in self.grid[i]:
                if value is not None:
                    value_counts[value] = value_counts.get(value, 0) + 1
            for value, count in value_counts.items():
                column_score[i] += int(value) * count * count
        return column_score

    def score(self):
        return sum(self.column_score())

    def print(self, reverse=False, color="white"):
        table = Table(show_header=False, box=box.ROUNDED, style=color)

        for _ in range(3):
            table.add_column()

        range_values = range(2, -1, -1) if reverse else range(3)
        for i in range_values:
            table.add_row(self.grid[0][i], self.grid[1][i], self.grid[2][i])

        if reverse:
            console.print(table)
            self.print_column_score(color=color)
        else:
            self.print_column_score(color=color)
            console.print(table)

    def print_column_score(self, color="white"):
        console.print(self.column_score(), style=color)


class Player:
    def __init__(self, color: str, name: str):
        self.color = color
        self.name = name
        self.board = Board()


class AIPlayer(Player):
    def __init__(self, color: str, difficulty: str):
        fake = Faker("de_DE")
        super().__init__(color, fake.first_name())
        self.difficulty = difficulty

    def choose_column(self, dice_roll, opponent_board):
        valid_columns = [i for i in range(3) if None in self.board.grid[i]]

        if self.difficulty == "easy":
            return str(random.choice(valid_columns) + 1)

        elif self.difficulty == "medium":
            best_score = -1
            best_column = None
            for col in valid_columns:
                score = self._calculate_score_for_move(col, dice_roll)
                if score > best_score:
                    best_score = score
                    best_column = col
            return str(best_column + 1)

        elif self.difficulty == "hard":
            best_score = -1
            best_column = None
            for col in valid_columns:
                score = self._calculate_score_for_move(col, dice_roll)
                opponent_score = self._calculate_opponent_loss(
                    col, dice_roll, opponent_board
                )
                total_score = score + opponent_score
                if total_score > best_score:
                    best_score = total_score
                    best_column = col
            return str(best_column + 1)

    def _calculate_score_for_move(self, column, dice_roll):
        temp_board = [row[:] for row in self.board.grid]
        for i in range(3):
            if temp_board[column][i] is None:
                temp_board[column][i] = dice_roll
                break
        return self._calculate_column_score(temp_board[column])

    def _calculate_column_score(self, column):
        value_counts = {}
        for value in column:
            if value is not None:
                value_counts[value] = value_counts.get(value, 0) + 1
        return sum(int(value) * count * count for value, count in value_counts.items())

    def _calculate_opponent_loss(self, column, dice_roll, opponent_board):
        temp_board = [row[:] for row in opponent_board.grid]
        original_score = self._calculate_column_score(temp_board[column])
        temp_board[column] = [val for val in temp_board[column] if val != dice_roll]
        temp_board[column] += [None] * (3 - len(temp_board[column]))
        new_score = self._calculate_column_score(temp_board[column])
        return original_score - new_score


class Knucklebone:

    def __init__(self):
        self.current_turn_index = 0
        self.players = []

    def get_current_player(self):
        return self.players[self.current_turn_index]

    def main_menu(self):
        while True:
            console.clear()
            console.print(
                Panel(
                    "[1] Play vs Human\n[2] Play vs AI\n[3] Quit", title="Knucklebone"
                )
            )

            choice = Prompt.ask("Please select an option", choices=["1", "2", "3"])

            if choice == "1":
                console.clear()
                player1_name = Prompt.ask("Enter name for Player 1")
                player2_name = Prompt.ask("Enter name for Player 2")
                self.players = [
                    Player("cyan", player1_name),
                    Player("red", player2_name),
                ]
                self.play_game()
            elif choice == "2":
                console.clear()
                player_name = Prompt.ask("Enter your name")
                console.print("\nChoose AI difficulty:")
                console.print("[1] Easy")
                console.print("[2] Medium (default)")
                console.print("[3] Hard")
                difficulty_choice = Prompt.ask(
                    "Enter your choice", default="2", choices=["1", "2", "3"]
                )

                difficulty_map = {"1": "easy", "2": "medium", "3": "hard"}
                ai_difficulty = difficulty_map[difficulty_choice]

                self.players = [
                    Player("cyan", player_name),
                    AIPlayer("red", ai_difficulty),
                ]
                console.print(f"\nYou've chosen to play against a {ai_difficulty} AI.")
                time.sleep(1.5)  # Give the player a moment to see their choice
                self.play_game()
            elif choice == "3":
                break

    def random_number(self):
        return random.choice(["1", "2", "3", "4", "5", "6"])

    def end_turn(self):
        console.clear()
        self.current_turn_index = 1 - self.current_turn_index

    def display_end_game_screen(self):
        scores = [player.board.score() for player in self.players]
        winner = self.players[0] if scores[0] > scores[1] else self.players[1]

        table = Table()
        table.add_column("Player", no_wrap=True)
        table.add_column("Score", style="bold magenta", no_wrap=True)
        for player in self.players:
            table.add_row(player.name, str(player.board.score()), style=player.color)

        trophy = Text(f"🏆 {winner.name} Wins!", justify="center", style="bold green")
        console.print(Panel(table, title="Game Results", expand=False))
        console.print(Panel(trophy, expand=False))

    def is_game_over(self):
        player = self.players[self.current_turn_index]
        for i in range(3):
            for j in range(3):
                if player.board.grid[i][j] == None:
                    return False
        return True

    def clear_opponent_column(self, column: str, dice_roll: str):
        opponent_board = self.players[1 - self.current_turn_index].board
        column_idx = int(column) - 1
        new_column = [
            value
            for value in opponent_board.grid[column_idx]
            if value != int(dice_roll)
        ]
        new_column += [None] * (3 - len(new_column))
        opponent_board.grid[column_idx] = new_column

    def show_board(self):
        for i in range(1, -1, -1):
            self.players[i].board.print(reverse=i, color=self.players[i].color)

    def reset_game(self):
        for player in self.players:
            player.board.reset()

    def play_game(self):
        while True:
            current_player = self.get_current_player()
            dice_roll = self.random_number()
            console.print(
                f"[{current_player.color}]It's {current_player.name}'s turn! Your score is {current_player.board.score()}.\n[/{current_player.color}]You rolled a [bold]{dice_roll}[/bold]."
            )

            self.show_board()

            if isinstance(current_player, AIPlayer):
                console.print(
                    f":thinking_face: [italic]{current_player.name} is thinking...[/italic]"
                )
                time.sleep(1)
                opponent_board = self.players[1 - self.current_turn_index].board
                choice = current_player.choose_column(dice_roll, opponent_board)
            else:
                while True:
                    choice = Prompt.ask(
                        "Please select an option", choices=["1", "2", "3"]
                    )
                    if current_player.board.is_valid_move(int(choice)):
                        break
                    else:
                        console.print("[red]Invalid play[/red]")

            current_player.board.update_column(int(choice), dice_roll)
            self.clear_opponent_column(choice, dice_roll)

            if self.is_game_over():
                self.display_end_game_screen()
                input("Press enter to return to the main menu...")
                self.reset_game()
                break
            self.end_turn()


if __name__ == "__main__":
    game = Knucklebone()
    game.main_menu()
