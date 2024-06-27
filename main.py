import random

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

    def column_score(self):
        column_score = [0, 0, 0]
        for i in range(3):
            value_counts = {}
            for value in self.grid[i]:
                if value in value_counts:
                    value_counts[value] += 1
                else:
                    value_counts[value] = 1
            for value, count in value_counts.items():
                if value is not None:
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
    def __init__(self, color: str):
        self.color = color
        self.board = Board()

class AIPlayer(Player):
    def choose_column(self, dice_roll):
        valid_columns = [i for i in range(3) if None in self.board.grid[i]]
        return str(random.choice(valid_columns) + 1)

class Knucklebone:

    def __init__(self):
        self.current_turn_index = 0
        self.players = []

    def get_current_player(self):
        return self.players[self.current_turn_index]

    def main_menu(self):
        while True:
            console.clear()
            console.print(Panel("[1] Play vs Human\n[2] Play vs AI\n[3] Quit", title="Knucklebone"))

            choice = Prompt.ask("Please select an option", choices=["1", "2", "3"])

            if choice == "1":
                console.clear()
                self.players = [Player("cyan"), Player("red")]
                self.play_game()
            elif choice == "2":
                console.clear()
                self.players = [Player("cyan"), AIPlayer("red")]
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
            table.add_row(player.color, str(player.board.score()), style=player.color)

        trophy = Text(f"🏆 {winner.color} Wins!", justify="center", style="bold green")
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
        for i in range(3 - 1, -1, -1):
            if opponent_board.grid[column_idx][i] == dice_roll:
                opponent_board.grid[column_idx][i:] = opponent_board.grid[column_idx][
                    i + 1 :
                ]
                opponent_board.grid[column_idx].append(None)

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
                f"[{current_player.color}]It's {current_player.color} turn! Your score is {current_player.board.score()}.\n[/{current_player.color}]You rolled a [bold]{dice_roll}[/bold]."
            )

            self.show_board()

            if isinstance(current_player, AIPlayer):
                choice = current_player.choose_column(dice_roll)
                current_player.board.update_column(int(choice), dice_roll)
                console.print(f"AI chooses column {choice}")
            else:
                while True:
                    choice = Prompt.ask("Please select an option", choices=["1", "2", "3"])
                    valid_play = current_player.board.update_column(int(choice), dice_roll)
                    if valid_play:
                        break
                    else:
                        console.print("[red]Invalid play[/red]")

            self.clear_opponent_column(choice, dice_roll)
            if self.is_game_over():
                console.clear()
                self.show_board()
                self.display_end_game_screen()
                input("Press enter to return to the main menu...")
                self.reset_game()
                break
            self.end_turn()


if __name__ == "__main__":
    game = Knucklebone()
    game.main_menu()
