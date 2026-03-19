from tkinter import *
import random

class Tree:
    def __init__(self, state = "tree"):
        self.state = state
    
class Forest:

    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.forest = []
        row = []
        for i in range(num_rows):
            for j in range(num_cols):
                row.append(Tree("tree"))

            self.forest.append(row)
            row = []
        

class Simulation:

    def __init__(self, prob_fire, prob_tree, num_rows, num_cols):
        self.PROB_FIRE = prob_fire
        self.PROB_TREE = prob_tree
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.current_forest = Forest(num_rows, num_cols)
        self.next_forest = Forest(num_rows, num_cols)
    

    
    def display_forest(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.current_forest.forest[r][c].state == "tree":
                    print(2, end = " ")
                elif self.current_forest.forest[r][c].state == "burning":
                    print(1, end = " ")
                elif self.current_forest.forest[r][c].state == "burnt":
                    print(0, end = " ")
            print()
    
    def update_tree(self, current_forest, next_forest, row, col):
        # Updates that don't rely on close trees:
            
        # 1. If the tree is burning, it will be burnt in the next frame
        if (current_forest.forest[row][col].state == "burning"):
            next_forest.forest[row][col].state = "burnt"
            return
        # 2. If the tree is is burnt, it will remain 
        elif (current_forest.forest[row][col].state == "burnt"):
            if(random.random() < self.PROB_TREE):
                next_forest.forest[row][col].state = "tree"
            else:
                next_forest.forest[row][col].state = "burnt"
            return
        
        # Check if the tree is close to a fire and update accordingly
        for i in range(9):
            if(i == 0):
                r = -1
                c = -1
            elif(i == 1):
                r = -1
                c = 0
            elif(i == 2):
                r = -1
                c = 1
            elif(i == 3):
                r = 0
                c = -1
            elif(i == 4):
                r = 0
                c = 0
            elif(i == 5):
                r = 0
                c = 1
            elif(i == 6):
                r = 1
                c = -1
            elif(i == 7):
                r = 1
                c = 0
            elif(i == 8):
                r = 1
                c = 1
            if ((0 <= row + r < current_forest.num_rows) and (0 <= col + c < current_forest.num_cols) and not(r == 0 and c == 0)):
                # The cell exists
                # The cell is close to a fire
                if ((current_forest.forest[r + row][c + col].state == "burning") and (current_forest.forest[row][col].state == "tree")):
                    next_forest.forest[row][col].state = "burning"
                    return
        
        # The tree is not burning, but may catch fire
        if(current_forest.forest[row][col].state == "tree"):
            if(random.random() < self.PROB_FIRE):
                next_forest.forest[row][col].state = "burning"
            else:
                next_forest.forest[row][col].state = "tree"
            return

    
    def update_forest(self):
        self.next_forest = Forest(num_rows = self.num_rows, num_cols = self.num_cols)
        
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.update_tree(self.current_forest, self.next_forest, r, c)
        
        self.current_forest = self.next_forest

def display_forest(forest_display, width, height, forest, num_rows, num_cols):
    sized_width = width / num_cols
    sized_height = height / num_rows
    for i in range(num_cols):
        for j in range(num_rows):
            if(forest.forest[j][i].state == "tree"):
                color = "green"
            elif(forest.forest[j][i].state == "burning"):
                color = "red"
            elif(forest.forest[j][i].state == "burnt"):
                color = "black"
            
            forest_display.create_rectangle(i * sized_width, j * sized_height, (i + 1) * sized_width, (j + 1) * sized_height, fill = color)

def update_canva(forest_display, width, height, forest, num_rows, num_cols):
    print("Updating the canva")
    simulation.update_forest()
    display_forest(forest_display, width, height, forest, num_rows, num_cols)



rows = 20
cols = 20
w = 400
h = 400
prob_fire = 0.01
prob_tree = 0.99
simulation = Simulation(prob_fire, prob_tree, rows, cols)

root = Tk()
root.title("Forest Fire Cellular Automata")

forest_display = Canvas(root, width = w, height = h, bg = "green")

display_forest(forest_display, w, h, simulation.current_forest, rows, cols)

button = Button(root, text="Next Frame", width=25, command = lambda: update_canva(forest_display, w, h, simulation.current_forest, rows, cols))

forest_display.pack()
button.pack()

root.mainloop()



