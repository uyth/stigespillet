$(document).ready(function() {

    var buttonDice = $('#buttonDice');
    var buttonReset = $('#buttonReset');
    var playerCount = $('input[name="playerInput"]').val();

    var game = {
        board: [],
        currentPlayer: 0,
        dice: 0,
        gameOver: false,
        players: [],
        init: function e() {
          game.initBoard();
          game.initPlayers();
        },
        initBoard: function e() {
            // add all cells to board
            for (var i = 0; i < 90; i++) {
                var cell = $("#index-" + i);
                cell.css("border", "3px solid black");
                var row = cell.css("grid-row").split("/")[0];
                var col = cell.css("grid-column").split("/")[0];
                game.board.push(new Cell(i, row, col));
            }
        },
        initPlayers: function e() {
            game.players = [];
            playerCount = $('input[name="playerInput"]').val();
            for (var i = 0; i < playerCount; i++) {
                // add player with inital start at cell 0
                game.players.push(new Player(i,game.board[0]));
                console.log(i);
            }
            console.log(game.players);
        },
        updateView: function e() {
            document.getElementById("dice").innerHTML = '' + game.dice;
            document.getElementById("currentPlayer").innerHTML = '' + (game.currentPlayer + 1);
            game.updatePlayerPosition();
        },
        updatePlayerPosition: function e() {
            game.players.forEach(function(player) {
                var element = document.getElementById("player-" + player.playerIndex);
                var cell = player.currentCell;
                element.className = 'player ' + "row-" + (cell.row - 1) + " col-" + (cell.col-1);
            });
        },
        rollDice: function e() {
            // roll a dice between 1 and 6
            game.dice = Math.floor(Math.random()*(7 - 1) + 1);
            game.updateView();
            game.players[game.currentPlayer].actions.move();
            game.nextTurn();
        },
        nextTurn: function e() {
            if (game.currentPlayer + 1 >= playerCount) {
                game.currentPlayer = 0;
            } else {
                game.currentPlayer++;
            }
            game.updateView();
        },
        ladders: [(3,17), (8,10), (15,44), (22,5),
            (39,56), (49,75), (62,45), (64,19),
            (65,73), (80,12), (87,79)]
    };

    // init Cell
    var Cell = function(index, row, col) {
        this.index = index;
        this.row = row;
        this.col = col;
        this.ladder = false;
        this.players = [];
    };

    // init Player
    var Player = function(index, cell) {
        this.playerIndex = index;
        this.currentCell = cell;
        this.currentCell.players.push(this);
        this.actions = {
            move: function e(){
                var indexBoard = currentCell.index;
                currentCell.players.pop(this);

                indexBoard += game.dice;
                currentCell = game.board[indexBoard];
                currentCell.players.push(this);
            }
        }
    };

    game.init();

    buttonDice.click(function e() {
        console.log("dice");
        game.rollDice();

    });
    buttonReset.click(function e() {
        console.log("reset");
        game.init();

    });

});
