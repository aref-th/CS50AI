import sys
from crossword import *
from collections import deque

class CrosswordCreator():
    def __init__(self, crossword):
        self.crossword = crossword
        self.domains = {var: self.crossword.words.copy() for var in self.crossword.variables}

    def letter_grid(self, assignment):
        letters = [[None for _ in range(self.crossword.width)] for _ in range(self.crossword.height)]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)
        img = Image.new("RGBA", (self.crossword.width * cell_size, self.crossword.height * cell_size), "black")
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [(j * cell_size + cell_border, i * cell_size + cell_border), ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text((rect[0][0] + ((interior_size - w) / 2), rect[0][1] + ((interior_size - h) / 2) - 10), letters[i][j], fill="black", font=font)
        img.save(filename)

    def enforce_node_consistency(self):
        for var in self.domains:
            self.domains[var] = {word for word in self.domains[var] if len(word) == var.length}

    def revise(self, x, y):
        revised = False
        overlap = self.crossword.overlaps.get((x, y))
        if overlap is None:
            return False
        i, j = overlap
        to_remove = set()
        for word_x in self.domains[x]:
            if all(word_x[i] != word_y[j] for word_y in self.domains[y]):
                to_remove.add(word_x)
        if to_remove:
            self.domains[x] -= to_remove
            revised = True
        return revised

    def ac3(self, arcs=None):
        queue = deque(arcs if arcs is not None else [(x, y) for x in self.domains for y in self.crossword.neighbors(x)])
        while queue:
            x, y = queue.popleft()
            if self.revise(x, y):
                if not self.domains[x]:  # If a domain becomes empty, no solution is possible
                    return False
                for neighbor in self.crossword.neighbors(x) - {y}:
                    queue.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        return set(assignment.keys()) == self.crossword.variables

    def consistent(self, assignment):
        words = set()
        for var, word in assignment.items():
            if len(word) != var.length or word in words:
                return False
            words.add(word)
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    if assignment[var][i] != assignment[neighbor][j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        def count_conflicts(word):
            return sum(1 for neighbor in self.crossword.neighbors(var) if neighbor not in assignment for neighbor_word in self.domains[neighbor] if any(word[i] != neighbor_word[j] for i, j in [self.crossword.overlaps[var, neighbor]] if self.crossword.overlaps[var, neighbor]))
        return sorted(self.domains[var], key=count_conflicts)

    def select_unassigned_variable(self, assignment):
        unassigned = [v for v in self.crossword.variables if v not in assignment]
        return min(unassigned, key=lambda v: (len(self.domains[v]), -len(self.crossword.neighbors(v))))

    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result:
                    return result
        return None

    def solve(self):
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack({})

if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")
    structure, words, output = sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else None
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)
