from tkinter import *
import random

class Simulation:

    def __init__(self, prob_fire, prob_tree, num_rows, num_cols):
        self.PROB_FIRE = prob_fire
        self.PROB_TREE = prob_tree
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.current_forest, self.next_forest = [], []
        for i in range(num_rows):
            temp1, temp2 = [], []
            for j in range(num_cols):
                temp1.append(2)
                temp2.append(2)
            self.current_forest.append(temp1)
            self.next_forest.append(temp2)
        
    def display_forest(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.current_forest[r][c] == 2:
                    print(2, end = " ")
                elif self.current_forest[r][c] == 1:
                    print(1, end = " ")
                elif self.current_forest[r][c] == 0:
                    print(0, end = " ")
            print()
    
    def update_tree(self, current_forest, next_forest, row, col):
        # Updates that don't rely on close trees:
            
        # 1. If the tree is burning, it will be burnt in the next frame
        if (current_forest[row][col] == 1):
            next_forest[row][col] = 0
            return
        # 2. If the tree is is burnt, it will remain 
        elif (current_forest[row][col] == 0):
            if(random.random() < self.PROB_TREE):
                next_forest[row][col] = 2
            else:
                next_forest[row][col] = 0
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
            if ((0 <= row + r < self.num_rows) and (0 <= col + c < self.num_cols) and not(r == 0 and c == 0)):
                # The cell exists
                # The cell is close to a fire
                if ((current_forest[r + row][c + col] == 1) and (current_forest[row][col] == 2)):
                    next_forest[row][col] = 1
                    return
        
        # The tree is not burning, but may catch fire
        if(current_forest[row][col] == 2):
            if(random.random() < self.PROB_FIRE):
                next_forest[row][col] = 1
            else:
                next_forest[row][col] = 2
            return

    
    def update_forest(self):
        self.next_forest = []
        for i in range(self.num_rows):
            temp = []
            for j in range(self.num_cols):
                temp.append(2)
            self.next_forest.append(temp)

        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.update_tree(self.current_forest, self.next_forest, r, c)
        
        self.current_forest = self.next_forest

def display_forest(forest_display, width, height, forest, num_rows, num_cols):
    sized_width = width / num_cols
    sized_height = height / num_rows
    forest_display.delete("all")
    for i in range(num_cols):
        for j in range(num_rows):
            if(forest[j][i] == 2):
                color = "green"
            elif(forest[j][i] == 1):
                color = "red"
            elif(forest[j][i] == 0):
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
prob_fire = 0.001
prob_tree = 0.45
simulation = Simulation(prob_fire, prob_tree, rows, cols)

root = Tk()
root.title("Forest Fire Cellular Automata")

forest_display = Canvas(root, width = w, height = h, bg = "green")

display_forest(forest_display, w, h, simulation.current_forest, rows, cols)

button = Button(root, text="Next Frame", width=25, command = lambda: update_canva(forest_display, w, h, simulation.current_forest, rows, cols))

forest_display.pack()
button.pack()

root.mainloop()



