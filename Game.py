import random


"""
a laddergame that tracks players, current players, and win condition
when stepping on a ladder you will be transferred to the position of the ladder


"""
class Game:

    def __init__(self, board_size, ladders, player_count):
        """
        :param board_size: (int row, int col)
        :param ladders: array with (int start, int end)
        :param player_count: int
        """

        self.ladders = ladders
        self.board_size = board_size
        self.board = []
        self.init_board()

        self.players = []
        self.initPlayers(player_count)
        self.current_player = self.players[0]


        self.game_over = False


    # init board
    # make cell -> if cell on ladder, add something else too
    def init_board(self):

        for index in range(self.board_size[0]*self.board_size[1]):
            self.board.append(Cell(index))

        # add ladder to cell
        for start, end in self.ladders:
            print("ladder", start-1, end-1)
            self.board[start-1].addLadder(end-1)

    def initPlayers(self, player_count):
        for player_index in range(player_count):
            self.players.append(Player(self, player_index))

    def next_turn(self):
        self.print_board()
        print("Current player's turn: " + str(self.current_player.get_player_index()))
        self.throw_dice(self.current_player)
        if (self.is_game_over()):
            return
        self.next_player()

    def throw_dice(self, player):

        # adds +++index on player...
        d6 = random.randint(1,6)
        d6 = 1
        print(d6)
        input("press enter to throw")
        player.move(d6)

    def print_board(self):

        board = ""
        row = ""
        for cell in self.board:
            if (cell.index % (self.board_size[0]) == 0):
                board += "\n"
            board += cell.to_string()

        player_state = ""
        for player in self.players:
            player_state += str(player.player_index) + ": " + str(player.board_index) + "\n"

        print(board)
        print(player_state)


    def is_game_over(self):
        if self.current_player.get_board_index() == len(self.board) - 1:
            return True
        return False

    def game_run(self):
        if len(self.players) < 2:
            print("must have at least two players")

        while not self.is_game_over():
            self.next_turn()

        print("Hurray! Player " + str(self.current_player.get_player_index()) + " won!")


    def next_player(self):
        player_index = self.current_player.get_player_index()
        if player_index  + 1 >= len(self.players):
            self.current_player = self.players[0]
        else:
            self.current_player = self.players[player_index + 1]

class Player:

    def __init__(self, game, player_index):

        self.board_index = 0
        self.current_cell = game.board[self.board_index]
        self.current_cell.add_player_to_cell(self)
        self.player_index = player_index
        self.game = game

    def move(self,steps):

        self.current_cell.remove_player_from_cell(self)

        # passes finish or on finish
        if self.board_index + steps >= len(self.game.board):
            steps = self.board_index + steps - (len(self.game.board) - 1)
            self.board_index = len(self.game.board) - 1  - steps
        # does not pass finish
        else:
            self.board_index += steps

        self.current_cell = self.game.board[self.board_index]
        self.current_cell.add_player_to_cell(self)

        return self.board_index

    def get_player_index(self):
        return self.player_index

    def get_board_index(self):
        return self.board_index

class Cell:

    def __init__(self, index):
        """

        :param index: int; cell position on board
        """

        self.index = index
        self.ladder = False
        self.players = []

    def add_player_to_cell(self, player):
        if player not in self.players:
            self.players.append(player)

    def remove_player_from_cell(self, player):
        if (player in self.players):
            self.players.remove(player)

    def addLadder(self, ladder_end):
        self.ladder = True
        self.ladder_end = ladder_end

    def get_ladder(self):
        return self.ladder

    def go_to(self):
        return self.ladder_end

    def to_string(self):
        to_string = "(" + str(self.index)
        to_string.ljust(4)
        if self.ladder == True:
            to_string += " " + str(self.ladder_end)
        to_string = to_string.ljust(6)
        to_string += ")"

        if not self.players == []:
            for player in self.players:
                to_string += " " + str(player.get_player_index())
        return to_string.ljust(15)

def main():

    ladders = [(3,17), (8,10), (15,44), (22,5), (39,56), (49,75), (62,45), (64,19), (65,73), (80,12), (87,79)]

    a = Game((9,10), ladders, 2)
    a.game_run()

main()