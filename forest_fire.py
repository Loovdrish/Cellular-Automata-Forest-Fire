from tkinter import *
import random

class Simulation:

    def __init__(self, prob_fire, prob_tree, num_rows, num_cols, delta = 100, running = True):
        self.PROB_FIRE = prob_fire
        self.PROB_TREE = prob_tree
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.current_forest, self.next_forest = [], []
        self.delta = delta
        self.running = running
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
        # 2. If the tree is is burnt, it will remain burnt
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

def auto_update():
    if(simulation.running):
        simulation.update_forest()
        display_forest(forest_display, w, h, simulation.current_forest, rows, cols)

    root.after(simulation.delta, auto_update)

def click_and_fire(event):
    col = int(event.x / (w / cols))
    row = int(event.y / (h / rows))

    if 0 <= row < rows and 0 <= col < cols:
        simulation.current_forest[row][col] = 1

    display_forest(forest_display, w, h, simulation.current_forest, rows, cols)

def update_fields(fire_field, tree_field, delta_field):
    simulation.PROB_FIRE = float(fire_field.get())
    simulation.PROB_TREE = float(tree_field.get())
    simulation.delta = int(delta_field.get())

def pause_simulation():
    simulation.running = False

def resume_simulation():
    simulation.running = True

rows = 30
cols = 30
w = 400
h = 400
prob_fire = 0.001
prob_tree = 0.1
delta = 100
simulation = Simulation(prob_fire, prob_tree, rows, cols, delta)

root = Tk()
root.title("Forest Fire Cellular Automata")
left = Frame(root)
left.grid(row = 0, column = 0)
Label(left, text = "FOREST FIRE").grid(row = 0, column = 0)

parameters = Frame(left)
parameters.grid(row = 1, column = 0)

Label(parameters, text = "Prob of fire: ").grid(row = 0, column = 0)
fire_field = Entry(parameters, width = 10)
fire_field.grid(row = 0, column = 1)
fire_field.insert(0, "0.001")

Label(parameters, text = "Prob of tree: ").grid(row = 1, column = 0)
tree_field = Entry(parameters, width = 10)
tree_field.grid(row = 1, column = 1)
tree_field.insert(0, "0.1")

Label(parameters, text = "Delta: ").grid(row = 2, column = 0)
delta_field = Entry(parameters, width = 10)
delta_field.grid(row = 2, column = 1)
delta_field.insert(0, "100")

button = Button(left, text="Update Parameters", width=25, command = lambda: update_fields(fire_field, tree_field, delta_field))
button.grid(row = 2, column = 0)

running_buttons = Frame(left)
running_buttons.grid(row = 3, column = 0)

pause_button  = Button(running_buttons, text = "Pause", width = 10, command = lambda : pause_simulation())
pause_button.grid(row = 0, column = 0)

resume_button  = Button(running_buttons, text = "Resume", width = 10, command = lambda : resume_simulation())
resume_button.grid(row = 0, column = 1)

forest_display = Canvas(root, width = w, height = h, bg = "green")
forest_display.grid(row = 0, column = 1)

display_forest(forest_display, w, h, simulation.current_forest, rows, cols)
forest_display.bind("<Button-1>", click_and_fire)
root.after(simulation.delta, auto_update)

root.mainloop()

