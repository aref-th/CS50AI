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
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
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
        """

        # Step 1: Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Step 2: Mark the cell as safe
        self.mark_safe(cell)

        # Step 3: Get all neighboring cells
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))

        # Step 4: Remove already known safe cells from neighbors
        neighbors -= self.safes

        # Step 5: Count how many of the known neighbors are already mines
        known_mines_count = len(neighbors & self.mines)

        # Step 6: Adjust count (subtract known mines)
        count -= known_mines_count

        # Step 7: Remove known mines from the set
        neighbors -= self.mines

        # Step 8: Only add to knowledge if the sentence isn't empty
        if neighbors:
            new_sentence = Sentence(neighbors, count)
            self.knowledge.append(new_sentence)

        # Step 9: Process knowledge to infer new facts
        self.update_knowledge()


    def update_knowledge(self):
        """
        Iterates through the knowledge base and marks mines, marks safes,
        and infers new sentences from existing knowledge.
        """
        updated = True

        while updated:
            updated = False
            new_knowledge = []

            # Step 1: Mark known mines and safes
            for sentence in self.knowledge:
                known_mines = sentence.known_mines()
                known_safes = sentence.known_safes()

                if known_mines:
                    updated = True
                    for mine in known_mines:
                        self.mark_mine(mine)

                if known_safes:
                    updated = True
                    for safe in known_safes:
                        self.mark_safe(safe)

            # Step 2: Remove empty sentences
            self.knowledge = [s for s in self.knowledge if s.cells]

            # Step 3: Infer new sentences by checking subsets
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 != s2 and s1.cells.issubset(s2.cells):
                        new_sentence = Sentence(s2.cells - s1.cells, s2.count - s1.count)
                        if new_sentence not in self.knowledge and new_sentence not in new_knowledge:
                            new_knowledge.append(new_sentence)
                            updated = True

            # Step 4: Add new inferences
            self.knowledge.extend(new_knowledge)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a random move to make on the board.
        """
        all_cells = {(i, j) for i in range(self.height) for j in range(self.width)}
        possible_moves = all_cells - self.moves_made - self.mines

        if possible_moves:
            return random.choice(list(possible_moves))
        return None
