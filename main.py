import random

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import box

console = Console()


class Board:
    def __init__(self) -> None:
        self.grid = [[" " for _ in range(3)] for _ in range(3)]

    def update_column(self, column_nb, dice_roll):
        self.grid[int(column_nb) - 1][0] = dice_roll

    def score(self):
        total_score = 0
        for row in self.grid:
            for cell in row:
                if cell.strip():  # Check if the cell is not empty
                    total_score += int(cell)
        return total_score

    def print(self, reverse=False, color="white"):
        table = Table(show_header=False, box=box.ROUNDED, style=color)

        for _ in range(3):
            table.add_column()

        if reverse:
            for i in range(2, -1, -1):
                table.add_row(self.grid[0][i], self.grid[1][i], self.grid[2][i])
        else:
            for i in range(3):
                table.add_row(self.grid[0][i], self.grid[1][i], self.grid[2][i])

        console.print(table)

class Player:
    def __init__(self, color: str):
        self.color = color
        self.board = Board()


class Knucklebone:

    def __init__(self):
        self.current_turn_index = 0
        self.players = [Player("cyan"), Player("red")]

    def get_current_player(self):
        return self.players[self.current_turn_index]

    def main_menu(self):
        while True:
            console.clear()
            console.print(Panel("[1] Play\n[2] Quit", title="Knucklebone"))

            choice = Prompt.ask("Please select an option", choices=["1", "2"])

            if choice == "1":
                console.clear()
                self.play_game()
            if choice == "2":
                break

    def random_number(self):
        return random.choice(["1", "2", "3", "4", "5", "6"])

    def end_turn(self):
        console.clear()
        self.current_turn_index = 1 - self.current_turn_index

    def play_game(self):
        while True:
            current_player = self.get_current_player()
            dice_roll = self.random_number()
            console.print(
                    f"[{current_player.color}]It's {current_player.color} turn!\nYour score is {current_player.board.score()}.\n[/{current_player.color}] You rolled a [bold]{dice_roll}[/bold]."
                )

            self.players[1].board.print(reverse=True, color=self.players[1].color)
            self.players[0].board.print(color=self.players[0].color)

            choice = Prompt.ask("Please select an option", choices=["1", "2", "3"])

            current_player.board.update_column(int(choice), dice_roll)

            self.end_turn()


if __name__ == "__main__":
    game = Knucklebone()
    game.main_menu()
