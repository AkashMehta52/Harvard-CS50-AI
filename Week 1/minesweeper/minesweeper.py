from hashlib import new
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        #if length of cells is equal to count, all cells are mines, else return an empty sety
        if(len(self.cells) == self.count):
            return self.cells
        else: return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #if there are no nearby mines, the cells are safe, otherwise they are not!
        if(self.count == 0):
            return self.cells
        else: return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #if the cell is in the set of cells, remove it and decrease the count by 1
        if(cell in self.cells):
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #if cell in set of cells, remove it but DO NOT decrease count
        if(cell in self.cells):
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #implemented step by step:
        #step 1: mark cell as move that is made:
        self.moves_made.add(cell)

        #step 2: mark the cell as safe:
        self.safes.add(cell)

        #step 3: add a new sentence to the AI's knowledge base based on the value of cells count:
        #not the most efficient, but should work :)
        newSentence = set()
        if(cell[0]-1 >= 0 and cell[1]-1 >= 0):
            newSentence.add((cell[0]-1,cell[1]-1))
        if(cell[0]-1 >= 0 and cell[1]+1 <= (self.width-1)):
            newSentence.add((cell[0]-1, cell[1]+1))
        if(cell[0]+1 <= self.height-1 and cell[1]-1 >= 0):
            newSentence.add((cell[0]+1, cell[1]-1))
        if(cell[0]+1 <= self.height-1 and cell[1]+1 < self.width):
            newSentence.add((cell[0]+1, cell[1]+1))
        if(cell[0]+1 < self.height):
            newSentence.add((cell[0]+1, cell[1]))
        if(cell[0]-1 >= 0):
            newSentence.add((cell[0]-1, cell[1]))
        if(cell[1]+1 < self.width):
            newSentence.add((cell[0], cell[1]+1))
        if(cell[1]-1 >= 0):
            newSentence.add((cell[0], cell[1]-1))
        #now we need to remove all the mines and safes that we already know
        #we cant update as we iterate so here's a seperate set 
        toRemove = set()
        countRemove = 0
        for cel in newSentence:
            if(cel in self.mines):
                toRemove.add(cel)
                #newSentence.remove(cel)
                countRemove += 1
            elif(cel in self.safes):
                toRemove.add(cel)
                #newSentence.remove(cel)
        newSentence = newSentence - toRemove
        #add sentence to AI KB
        updateSentence = Sentence(newSentence, count - countRemove)
        self.knowledge.append(updateSentence)

        #step 4: mark additional cells as safe or as mines based on KB
        #again, can't update while iterating, so here's seperate sets
        areMines = set()
        areSafes = set()
        for sentence in self.knowledge:
            for mineCell in sentence.known_mines():
                areMines.add(mineCell)
            for safeCell in sentence.known_safes():
                areSafes.add(safeCell)

        for mine in areMines:
            self.mark_mine(mine)
        for safe in areSafes:
            self.mark_safe(safe)

        #step 5: add new sentences to AI KB from inferred/existing knowledge(subset method)
        #loop over sentences in KB and compare to current sentence using subset method
        for sentence in self.knowledge:
            #avoid empty sets
            if sentence.cells and updateSentence.cells != updateSentence.cells:
                #if sentence subset of updated
                if(sentence.cells.issubset(updateSentence.cells)):
                    self.knowledge.append(Sentence(updateSentence.cells - sentence.cells, updateSentence.count - sentence.count))
                #if updated is subset of sentence
                elif(updateSentence.cells.issubset(sentence.cells)):
                    self.knowledge.append(Sentence(sentence.cells - updateSentence.cells, sentence.count - updateSentence.count))



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made:
                return move
        
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        #'random' move!
        #all possible moves:
        possibleMoves = set(itertools.product(range(self.height), range(self.width)))

        #all moves we can take
        movesReasonable = list(possibleMoves - self.mines - self.moves_made)

        #return random choice out of movesReasonable
        if(len(movesReasonable) == 0):
            return None
        else:
            return random.choice(movesReasonable)

        #raise NotImplementedError










