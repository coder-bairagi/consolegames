from consoleGames import TextBasedGame

# Minimum dimension should be 90 X 20, Standard is 120 X 30
WIDTH = 120
HEIGHT = 30

# board = Board(WIDTH, HEIGHT, hCenter=True, topMargin=4, debug=True)
game = TextBasedGame(WIDTH, HEIGHT, hCenter=True, topMargin=4, debug=True)
game.playerName = input('\nPlease Enter Your Name: ')

# Starts the Game
game.start()
