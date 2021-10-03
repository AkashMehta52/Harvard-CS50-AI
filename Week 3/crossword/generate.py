import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        #enforcing node consistency in this case boils down to ensuring the domain matches the length allowed
        #can't alter a set while iterating over it, so create an empty set to use     
        for var in self.crossword.variables:
            domainSet = list()
            for dom in self.domains[var]:
                if var.length != len(dom):
                    domainSet.append(dom)
            for dom in domainSet:
                self.domains[var].remove((dom))
        #raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        #in essense, we just want to enforce arc consistency!
        #follow formula from notes:
        revise = False
        overlap = self.crossword.overlaps[x,y]
        i = overlap[0]
        j = overlap[1]
        if overlap is not None:
            removeSet = list()
            for varX in self.domains[x]:
                #what represents a conflict? a square that two variables disagree
                overlapX = varX[i]
                yList = list()
                for varY in self.domains[y]:
                    yList.append(varY[j])
                if overlapX not in yList:
                    removeSet.append(varX)
                    revise = True

            for rem in removeSet:
                self.domains[x].remove(rem)

        return revise

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        #follow ac3 model from notes
        #create a queue 
        #arcs are variables with overlap
        queueArc = list()
        if (arcs != None):
            for element in arcs:
                queueArc.append(element)
        else:
            for valX in self.crossword.variables:
                for valY in self.crossword.variables:
                    if (valX != valY) and self.crossword.overlaps[valX, valY] is not None:
                        queueArc.append((valX, valY))
        #now implement ac3 function:
        while queueArc:
            #dequeue into tuple
            deqTuple = queueArc.pop(0)
            x = deqTuple[0]
            y = deqTuple[1]
            if self.revise(x,y):
                if(self.domains[x] == None):
                    return False
                for z in (self.crossword.neighbors(x) - {y}):
                    queueArc.append((z,x))
        return True       


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return False
        
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for key in assignment.keys():
            #ensure valid assignment
            if (assignment[key] != None):
                #make sure no value used twice
                if (len(set(assignment.values())) != len(set(assignment.keys()))):
                   
                    return False
                #ensure variable length is same as word length
                if key.length != len(assignment[key]):
                    return False
                #ensure no conflicts between neighboring variables
                #conflict = overlaps must match for neighboring vars
                for neighbor in self.crossword.neighbors(key).intersection(assignment.keys()):
                    #find overlap between neighbors
                    overlap = self.crossword.overlaps[key, neighbor]
                    i = overlap[0]
                    j = overlap[1]
                    #if the ith character of the word mapped to the key variable isn't the same
                    #as the jth character of the word mapped to the neighbor variable, 
                    #return false
                    if assignment[key][i] != assignment[neighbor][j]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #order domain values! returns a list of values in domain of var according to LCV
        #var = variable object
        #LCV = number of values ruled out for neighboring unassigned variables, if assigning
        #var to a value results in eliminating n possible choices, order results in ascending order
        #of n
        #any var in assignment already has a value shoudln't be counted 
        #if domain vals eliminate same number, any order is acceptable

        #create a dictionary of domains to hold vals for sorting later
        valDict = {}
        for dom in self.domains[var]:
            valDict[dom] = 0
        
        #loop over domain of value
        for dom in self.domains[var]:
            #loop over unassigned neighbors of node
            for neighbor in (self.crossword.neighbors(var) - assignment.keys()):
                overlap = self.crossword.overlaps[var, neighbor]
                i = overlap[0]
                j = overlap[1]
                #loop over domain of neighbor and check if conflict occurs
                for dom2 in self.domains[neighbor]:
                    #conflict situation, if conflict increment var
                    if dom[i] != dom2[j]:
                        valDict[dom] += 1
        #sort the valDict
        sortedValList = (sorted(valDict.items(), key=lambda x: x[1], reverse = False))
        returnList = list()
        for val in sortedValList:
            returnList.append(val[0])

        return returnList


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        #first, use MRV heuristic and put vars and domain lengths in a dictionary
        domLength = {}
        for var in (self.crossword.variables - assignment.keys()):
            domLength[var] = len(self.domains[var])
        
        #sort the dictionary into a list of tuples
        sortedDomLen = sorted(domLength.items(), key=lambda x: x[1], reverse=False)
        #check top values of this and return!
        if (sortedDomLen[0][1] == 1 or len(sortedDomLen) == 1):
            return sortedDomLen[0][0]
        elif(sortedDomLen[0][1] != sortedDomLen[1][1]):
            return sortedDomLen[0][0]
        #if tie, use degree heuristic:
        else:
            degLen = {}
            for var in (self.crossword.variables - assignment.keys()):
                degLen[var] = len(self.crossword.neighbors(var))
            sortedDegLen = sorted(degLen.items(), key=lambda x:x[1], reverse=False)
            #return the top regardless of tie!
            return sortedDomLen[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        #last function whoop whoop!!!
        #follow backtrack algorithm from notes
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            #create new assignment to test consistency
            checkAssignment = copy.deepcopy(assignment)
            checkAssignment[var] = val
            if self.consistent(checkAssignment):
                assignment[var] = val
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                assignment.pop(var,None)
        return None


        #raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
