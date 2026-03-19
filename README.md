# Cellular Automata Forest Fire
Forest Fire is a cellular automata simulation that demonstrates the propagation of a forest fires.

## How Does It Work
The simulation begins with a grid of green cells representing trees. 
![image alt](https://github.com/Loovdrish/Cellular-Automata-Forest-Fire/blob/dd95e9ccf927a47edaf0a35139c53c05fef484e3/Grid_Trees.png)

At each instant, there is a probability that a forest fire begins by burning one of the trees. Burning trees are represented by red cells. 
![image alt](https://github.com/Loovdrish/Cellular-Automata-Forest-Fire/blob/b7fa7f92d4bf6d8571831d18edaf6358c2859c1b/Forest_Fires_Appear.png)

Burning cells propagate by burning trees around them. After burning, the tree gets completely burnt (shown in black).

After a tree got burnt, a new tree can grow in that same location. This possibility constitutes another key parameter.

To move from one instant to the next, click on the button "Next Frame".
