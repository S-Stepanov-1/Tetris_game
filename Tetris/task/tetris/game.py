import numpy as np


class Game:
    grid = []
    position = 0  # the number of the nested list for a particular key-letter in the dictionary
    letters_pieces = {"O": [[4, 14, 15, 5]],
                      "I": [[4, 14, 24, 34], [3, 4, 5, 6]],
                      "S": [[5, 4, 14, 13], [4, 14, 15, 25]],
                      "Z": [[4, 5, 15, 16], [5, 15, 14, 24]],
                      "L": [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
                      "J": [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
                      "T": [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]
                      }

    def __init__(self, columns, rows):
        self.columns, self.rows = columns, rows
        self.figure, self.save_grid = [], set()
        self.piece = ""

    #   ===output of the first grid consisting of "-"===
    def get_start_grid(self):
        for i in range(self.columns * self.rows):
            print("-", end=" " if (i + 1) % self.columns != 0 else "\n")
        print()
        if input() == "piece":
            self.enter_piece()

    def enter_piece(self):
        self.piece = input()
        self.figure = np.asarray(self.letters_pieces[self.piece])

    def get_current_grid(self):
        self.grid = ["-" if i not in self.figure[self.position] else "0" for i in range((self.columns * self.rows))]
        return self.grid

    def print_playground(self):
        for i in range(self.columns * self.rows):
            print("-" if i not in self.figure[self.position] and i not in self.save_grid else "0",
                  end=" " if (i + 1) % self.columns != 0 else "\n")
        print()

    def check_x_incident(self):
        if "0" in self.get_current_grid()[len(self.grid) - self.columns: len(self.grid)] or\
                set(self.figure[self.position] + 10) & self.save_grid:
            self.print_playground()
            self.save_grid |= set(self.figure[self.position])
            if "0" in self.grid[:self.columns]:
                print("Game Over!")
                exit()

            next_step = input()
            if next_step == "piece":
                self.position = 0
                self.enter_piece()
            elif next_step == "exit":
                exit()
            elif next_step == "break":
                self.check_row()
            else:
                self.check_x_incident()

    def check_row(self):
        for element in range(self.rows):
            grid = [i for i in range(element * 10, (element + 1) * self.columns)]
            if set(grid).issubset(self.save_grid):
                self.save_grid -= set(grid)
                new_save = list(self.save_grid)
                for index in range(len(new_save)):
                    if new_save[index] < grid[0]:
                        new_save[index] += 10
                self.save_grid = set(new_save)
        for i in range(self.columns * self.rows):
            print("-" if i not in self.save_grid else "0",
                  end=" " if (i + 1) % self.columns != 0 else "\n")
        print()
        self.position = 0
        next_step = input()
        if next_step == "piece":

            self.enter_piece()
        elif next_step == "exit":
            exit()

    def left_move(self):
        if "0" not in self.get_current_grid()[0::10] and not set(self.figure[self.position] + 9) & self.save_grid:
            self.figure -= 1
        self.down_move()

    def right_move(self):
        if "0" not in self.get_current_grid()[9::10] and not set(self.figure[self.position] + 11) & self.save_grid:
            self.figure += 1
        self.down_move()

    def down_move(self):
        self.figure += self.columns
        self.check_x_incident()

    def rotate(self):
        self.position = (self.position + 1) % len(self.figure)
        self.down_move()

    def enter_the_command(self):
        command = input()
        if command == "exit":
            exit()
        print()
        command_list = {"left": self.left_move, "right": self.right_move,
                        "down": self.down_move, "rotate": self.rotate, "break": self.check_row}
        self.check_x_incident()
        command_list[command]()


def main():
    dimension = [int(i) for i in input().split()]
    tetris = Game(*dimension)
    tetris.get_start_grid()
    while True:
        #   ===grid output "-"===
        #   elements with indexes specified in the list (dictionary[key][position] are replaced by "0" ===
        tetris.print_playground()
        tetris.enter_the_command()


if __name__ == '__main__':
    main()
