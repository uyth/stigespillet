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
        self.dice = 0

        self.players = []
        self.init_players(player_count)
        self.current_player = self.players[0]

        self.game_over = False

    def init_board(self):
        """
        inits and adds Cells to board = []
        inits ladders to Cells
        :return:
        """
        for index in range(self.board_size[0]*self.board_size[1]):
            self.board.append(Cell(index))

        # add ladder to cell
        for start, end in self.ladders:
            self.board[start-1].addLadder(end-1)

    def init_players(self, player_count):
        """
        inits players and adds them the players array
        :param player_count: int, amount of players in game
        :return:
        """
        for player_index in range(player_count):
            self.players.append(Player(self, player_index))

    def print_board(self):
        """
        prints the board to the CLI
        :return:
        """
        board = ""
        for cell in self.board:
            if cell.index % (self.board_size[0]) == 0:
                board += "\n"
            board += cell.to_string()

        player_state = ""
        for player in self.players:
            player_state += str(player.player_index) + ": " + str(player.board_index) + "\n"

        print(board)
        print("\n")
        print("Dice: " + str(self.dice))
        print(player_state)


    def game_run(self):
        """
        runs the game until win condition met
        :return:
        """
        if len(self.players) < 2:
            print("must have at least two players")

        self.print_board()

        while not self.is_game_over():
            self.next_turn()

        print("Hurray! Player " + str(self.current_player.get_player_index()) + " won!")


    def next_turn(self):
        """
        throw dice and checks if game is over afterwards
        :return:
        """
        print("Current player's turn: " + str(self.current_player.get_player_index()))
        input("press enter to throw a dice")
        self.throw_dice(self.current_player)
        self.print_board()
        if (self.is_game_over()):
            return
        self.next_player()

    def next_player(self):
        """
        changes current_player to current_player with index++
        if current player has the highest index, go back to first player
        :return:
        """
        player_index = self.current_player.get_player_index()
        if player_index  + 1 >= len(self.players):
            self.current_player = self.players[0]
        else:
            self.current_player = self.players[player_index + 1]

    def throw_dice(self, player):
        """
        delegates movement to player
        :param player: Player object
        :return:
        """
        self.dice = random.randint(1,6)
        player.move(self.dice)

    def is_game_over(self):
        """
        win condition: player on the last cell
        :return: bool
        """
        if self.current_player.get_board_index() == len(self.board) - 1:
            return True
        return False

class Player:

    def __init__(self, game, player_index):
        """
        inits Player object
        :param game: this game
        :param player_index: int; 0-indexed
        """
        self.board_index = 0
        self.current_cell = game.board[self.board_index]
        self.current_cell.add_player_to_cell(self)
        self.player_index = player_index
        self.game = game

    def move(self,steps):
        """
        moves the player, if exceeding the board limit, go back some steps
        :param steps: int; steps to move on the board
        :return: int; end position
        """

        self.current_cell.remove_player_from_cell(self)

        # passes last cell
        if self.board_index + steps >= len(self.game.board):
            steps = self.board_index + steps - (len(self.game.board) - 1)
            self.board_index = len(self.game.board) - 1  - steps
        # does not pass last cell
        else:
            self.board_index += steps

        # check if next cell has ladder
        next_cell = self.game.board[self.board_index]

        if next_cell.has_ladder():
            self.board_index = next_cell.go_to()

        # set current cell
        self.current_cell = self.game.board[self.board_index]
        self.current_cell.add_player_to_cell(self)

        return self.board_index

    def get_player_index(self):
        """
        :return: int; player index; 0-indexed
        """
        return self.player_index

    def get_board_index(self):
        """
        :return: int; position on board; 0-indexed
        """
        return self.board_index

class Cell:

    def __init__(self, index):
        """
        inits Cell object, Cell in board array
        can contain ladder and track players on it
        :param index: int; cell position on board
        """
        self.index = index
        self.ladder = False
        self.players = []

    def add_player_to_cell(self, player):
        """
        track players on this cell
        :param player: array; [Player, ...]
        :return:
        """
        if player not in self.players:
            self.players.append(player)

    def remove_player_from_cell(self, player):
        """
        removes players from this cell
        :param player: array; [Player, ..]
        :return:
        """
        if (player in self.players):
            self.players.remove(player)

    def addLadder(self, ladder_end):
        """
        called when ladder matches this cell
        :param ladder_end: int; board index of where the player
        goes when he/she steps on the cell
        :return:
        """
        self.ladder = True
        self.ladder_end = ladder_end

    def go_to(self):
        """
        is called when player steps on ladder
        :return:
        """
        return self.ladder_end

    def has_ladder(self):
        return self.ladder

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
    player_count = 0
    while(player_count < 2):
        try:
            player_count = int(input("Amount of players: "))
            if (player_count < 2):
                print("At least two players")
        except:
            print("Not a valid value")
    a = Game((9,10), ladders, player_count)
    a.game_run()

main()