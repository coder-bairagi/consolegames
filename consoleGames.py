import shutil
import os
import json

class Board:
    def __init__(self, width=80, height=80, vCenter=False, hCenter=False, topMargin=0, leftMargin=0, bottomMargin=0, debug=True):
        self.width = width
        self.height = height
        self.topbarWidth = 0
        self.sidebarWidth = int(0.19 * self.width) # Setting to 19% of total width
        self.initializeBoard()
        self.terminalWidth, self.terminalHeight = shutil.get_terminal_size(fallback=(80, 24))
        self.leftMargin = (self.terminalWidth - self.width) // 2 if hCenter == True else leftMargin
        self.yMargin = (self.terminalHeight - self.height) // 2
        self.topMargin = self.yMargin if vCenter == True else topMargin
        self.bottomMargin = self.yMargin if vCenter == True else bottomMargin
        self.debug = debug

    def initializeBoard(self):
        """Create an empty board with the given dimensions."""
        self.board = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def placeContent(self, content: str, topLeftRow: int, topLeftCol: int):
        """Place content in the board starting from (topLeftRow, topLeftCol)."""
        contentLines = content.split('\n')
        for i, line in enumerate(contentLines):
            for j, char in enumerate(line):
                if 0 <= topLeftRow + i < len(self.board) and 0 <= topLeftCol + j < len(self.board[0]):
                    self.board[topLeftRow + i][topLeftCol + j] = char
                    

    def placeChar(self, char: str, row: int, column: int):
        """Place character in the board exactly at row, column."""
        try:
            self.board[row][column] = char
        except IndexError as ie:
            message = 'Something is Getting Out of the Board'
            self.showError(errorname='Index Error', message=message, error=ie, lineNumber=38, code="selfboard  [row][column] = char")

    def printBoard(self, clearScreen=True):
        """Print the board to the console."""
        if clearScreen:
            os.system('cls')
        for _ in range(self.topMargin):
            print()
        for row in self.board:
            print(f'{' '*self.leftMargin}{''.join(row)}')
        for _ in range(self.bottomMargin):
            print()
    
    def drawBorders(self, left='|', right='|', top='-', bottom='-'):
        # Top border
        self.placeContent(f'{top*self.width}', 0, 0)
        # Bottom border
        self.placeContent(f'{bottom*self.width}', self.height - 1, 0)
        # Side borders
        end = self.width - 1
        for i in range(1, self.height - 1):
            self.placeChar(left, i, 0)
            self.placeChar(right, i, end)

    def drawTopbar(self, rowPosition=2, colPosition=1, symbol='-'):
        self.topbarWidth = self.width - colPosition
        for i in range(colPosition, self.width - 1):
            self.placeChar(symbol, rowPosition, i)

    def setTopbarContent(self, content=[], rowPosition=1, justifyContent='spaceAround'):
        if len(content) > 0: 
            contentWidth = 0
            for element in content:
                contentWidth += len(element)
            if justifyContent == 'spaceAround':
                space = int((self.topbarWidth - contentWidth) / (len(content) - 0.5))
                edgeSpace = int(space / 4)
                data = ' ' * edgeSpace
                flag = True
                i = 0
                for element in range(2 * len(content) - 1):
                    if flag == True:
                        data += content[i]
                        i += 1
                        flag = False
                    else:
                        data += ' ' * space
                        flag = True
                data += ' ' * edgeSpace
            for j, char in enumerate(data):
                self.placeChar(char, rowPosition, j + self.sidebarWidth + 1)

    def drawSidebar(self, colPosition: int = None, symbol: str ='|'):
        colPosition = self.sidebarWidth if colPosition == None else colPosition
        for i in range(1, self.height - 1):
            self.placeChar(symbol, i, colPosition)

    def setSidebarContent(self, content=['Sidebar'], rowPosition=1, colPosition=1, justifyContent='none', betweenPad=0):
        if justifyContent == 'maxFit':
            try:
                colPosition = int((self.sidebarWidth - 2 - len(max(content, key=len))) / 2) + 2
            except ValueError as ve:
                message = 'Sidebar content cannot be empty'
                self.showError(errorname='Value Error', message=message, error=ve, lineNumber=102, code="colPosition = int((self.sidebarWidth - 2 - len(max(content, key=len))) / 2) + 2")

        for i, word in enumerate(content):
            if justifyContent == 'center':
                colPosition = int((self.sidebarWidth - 2 - len(word)) / 2) + 2
            for j, char in enumerate(word):
                self.placeChar(char, i + rowPosition, j + colPosition)
            if betweenPad > 0:
                rowPosition += betweenPad

    def clearArea(self, fromRow: int, toRow: int, fromCol: int, toCol: int):
        for i in range(fromRow, toRow + 1):
            for j in range(fromCol, toCol + 1):
                self.placeChar(' ', i, j)

    def showError(self, errorname: str, message: str, error: str, lineNumber: int, code: str):
        print()
        if self.debug == True:
            self.printDebugWarning()
            print(f'{errorname}: {message}')
            print(f'{errorname}: {error}')
            print(f'Line Number: {lineNumber}')
            print(f'```\n{code}\n```')
        else:
            print('***Something went wrong. Please contact developer.***')
        input()

    def printDebugWarning(self):
        print('\n***YOU ARE SEEING THIS MESSAGE BECAUSE "DEBUG" IS TRUE. TURN IT TO FALSE IN PRODUCTION.\n')

class TextBasedGame(Board):
    def __init__(self, width=80, height=80, vCenter=False, hCenter=False, topMargin=0, leftMargin=0, bottomMargin=0, debug=True, playerName='ABC', story=None, scenes=None, inventory={}):
        # Calling constructor and methods of Board Class
        super().__init__(width, height, vCenter, hCenter, topMargin, leftMargin, bottomMargin, debug)
        # Initialize attributes of this class
        self.playerName = playerName
        self.health = 100
        self.defense = 0
        self.story = self.loadStory() if story is None else story
        self.scenes = self.loadScenes() if scenes is None else scenes
        self.inventory = inventory
        self.ACTIONS = {
            'INCREMENT': 'increment',
            'DECREMENT': 'decrement',
            'NONE': 'none'
        }

    def loadScenes(self):
        path = 'scenes.json'
        with open(path, 'r') as file:
            scenes = json.load(file)
        return scenes
    
    def loadStory(self):
        path = 'story.json'
        with open(path, 'r') as file:
            story = json.load(file)
        return story

    def splitMaxLength(self, string: str, maxLength: int):
        splitedString = []
        fromIndex = 0
        toIndex = maxLength

        while fromIndex < len(string):
            # If the current segment ends in the middle of a word, backtrack to the last space
            if toIndex < len(string) and string[toIndex - 1] != ' ':
                while string[toIndex - 1] != ' ':
                    toIndex -= 1

            splitedString.append(string[fromIndex:toIndex].strip())
            fromIndex = toIndex
            toIndex = min(fromIndex + maxLength, len(string))

        return splitedString

    def setTopbar(self):
        content = [
            f'Name: {self.playerName}',
            f'Health: {self.health}',
            f'Defense: {self.defense}',
        ]
        self.drawTopbar(rowPosition=4, colPosition=self.sidebarWidth + 1)
        self.setTopbarContent(content=content, rowPosition=2)

    def setSidebar(self, message = 'Collect Inventory as You Go. Save Your Sister Young Man'):
        self.drawSidebar()
        content = [
            'Inventory',
        ]
        self.setSidebarContent(content=['-'*(self.sidebarWidth - 1)], rowPosition=4)
        self.setSidebarContent(content=content, rowPosition=2, justifyContent='center')
        content = []
        if self.inventory:
            for key, value in list(self.inventory.items()):
                if value == 0:
                    del self.inventory[key]
        if self.inventory:
            if len(self.inventory) == 1:
                content = self.splitMaxLength(message, self.sidebarWidth - 2 + 1)
                content = []
            for i, (item, count) in enumerate(self.inventory.items()):
                content.append(f'{item.capitalize()}: {count}')
        else:
            content = self.splitMaxLength(message, self.sidebarWidth - 2 + 1)
        self.clearArea(5, self.height - 2, 1, self.sidebarWidth - 1)
        self.setSidebarContent(content=content, rowPosition=6, justifyContent='maxFit', betweenPad=1)

    def updateInventory(self, item, action):
        if item not in self.inventory and action == self.ACTIONS['INCREMENT']:
            self.inventory[item] = 1
        elif action == self.ACTIONS['INCREMENT']:
            self.inventory[item] = self.inventory[item] + 1
        elif action == self.ACTIONS['DECREMENT']:
            self.inventory[item] = self.inventory[item] - 1
        else:
            return False
        return True
    
    def updateHealth(self, value, action):
        if action == self.ACTIONS['INCREMENT'] and self.health < 100:
            self.health = min(self.health + value, 100)
        elif action == self.ACTIONS['DECREMENT']:
            self.health = max(self.health - value, 0)
        else:
            return False
        return True

    def showStory(self):
        message = 'Press Enter to Move Forward'
        message = self.splitMaxLength(message, self.width - 2)
        for line in self.story:
            line = self.splitMaxLength(line, self.width - 2)
            rowPosition = int((self.height - len(line)) / 2)
            mRow = rowPosition
            for i, string in enumerate(line):
                self.placeContent(string, i + rowPosition, int((self.width - len(string)) / 2))
                mRow += i
            for i, line in enumerate(message):
                self.placeContent(line, i + mRow + 2, int((self.width - len(line)) / 2))
            self.printBoard()
            input()
            self.clearArea(1, self.height - 2, 1, self.width - 2)

    def showMessagePlayArea(self, playAreaWidth: int, message: str):
        self.clearArea(5, self.height - 2, self.sidebarWidth + 1, self.width - 2)
        message = self.splitMaxLength(message, self.width - 2 - self.sidebarWidth + 1)
        rowPosition = int((self.height - 1 - len(message)) / 2) + 3
        for i, string in enumerate(message):
            messageLeftPad = int((playAreaWidth - len(string)) / 2)
            string = (' ' * messageLeftPad) + string
            for j, char in enumerate(string):
                self.placeChar(char, i + rowPosition, j + self.sidebarWidth + 1)
        # Printing updated board
        self.printBoard()
        input("\nPress Enter to Move Forward: ")

    def start(self):
        # Drawing board borders
        self.drawBorders()

        # Show the story
        self.showStory()

        # Start the game
        # Setting topbar and it's content
        self.setTopbar()

        # Setting sidebar and it's content
        self.setSidebar()

        # Setting Play Area
        for obj in self.scenes:
            while True:
                self.clearArea(5, self.height - 2, self.sidebarWidth + 1, self.width - 2)
                playWidth = self.width - 2 - (self.sidebarWidth + 1) + 1

                # Setting scene, question, and options
                scene = self.splitMaxLength(obj['scene'], self.width - 2 - self.sidebarWidth + 1)
                question = self.splitMaxLength(obj['question'], self.width - 2 - self.sidebarWidth + 1)
                options = [f'{key}. {value}' for key, value in obj['options'].items()]
                playAreaContent = [scene, question, options]
                rowPosition = int((self.height - 1 - (len(scene) + len(question) + len(options) + 2)) / 2) + 3
                for content in playAreaContent:
                    for i, string in enumerate(content):
                        contentLeftPad = int((playWidth - len(string)) / 2)
                        string = (' ' * contentLeftPad) + string
                        for j, char in enumerate(string):
                            self.placeChar(char, i + rowPosition, j + self.sidebarWidth + 1)
                    rowPosition += len(content) + 1

                # Printing the updated board
                self.printBoard()

                inputNum = input('Please Enter the Number of Your Desired Action: ')
                # Show message if check key is present in scene obj along with it's corresponding item not present in inventory and inputed number is in options list
                if 'check' in obj and obj['check']['item'] not in self.inventory and inputNum in obj['check']['options']:
                    self.showMessagePlayArea(playWidth, obj['check']['message'])
                    continue
                if inputNum in obj['results']:
                    result = obj['results'][inputNum]
                    match obj['attribute']:
                        case 'inventory':
                            self.updateInventory(obj['item'], result['action'])
                            # Set sidebar with updated inventory
                            self.setSidebar()
                        case 'health':
                            self.updateHealth(obj['value'], result['action'])
                            item = obj['item'] if 'item' in obj else obj['check']['item']
                            self.updateInventory(item, result['action'])
                            # Set topbar and sidebar with updated health and inventory
                            self.setTopbar()
                            self.setSidebar()
                        case 'defense':
                            pass
                        case _ :
                            message = f'Attribute mismatch or not found in scene.json file at results {inputNum} of scene {obj['scene']}'
                            code = f'result = obj["results"][inputNum]\nmatch result:\n{' '*4}case "inventory":\n{' '*(4*2)}code\n{' '*4}case "health":\n{' '*(4*2)}code\n{' '*4}case "defense":\n{' '*(4*2)}code'
                            self.showError(errorname='Value Error', message=message, error=message, lineNumber=253, code=code)
                    # Clearing the play area and showing message
                    self.showMessagePlayArea(playWidth, result['message'])
                    break
                else:
                    print('Invalid action. Please try again.')
    