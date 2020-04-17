# We import the libraries that we are going to use afterwards
from numpy import array, zeros, empty, sum 
from matplotlib import colors
import matplotlib.pyplot as plt

# We create the array with the pattern of the sudoku that we are aiming to solve
initial_pattern = array([
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
])

# We create a copy as we will need the original if we want to do a plot 
pattern = initial_pattern.copy()


# We start defining the funtions that we will need to calculate the solution of the puzzle
def In(value, arrays):

    # Studies if a value is inside of an array
    return value in arrays


def Matrix(pattern, posx, posy):

    # Create the submatrix 3x3 of a given position
    i = (posx // 3) 
    j = (posy // 3) 
    return pattern[3*i:3*(i+1), 3*j:3*(j+1)]


def Lines(pattern, posx, posy):

    # Creates the vertical and horizontal line of that contains a given value position
    return pattern[posx, :], pattern[:, posy]


def Possibles(pattern, posx, posy):

    # Studies the possible numbers that we can introduce in a gap, 
    # Removes those numbers who are alredy in the submatrix or the lines of the value position
    global In, Lines, Matrix

    matrix = Matrix(pattern, posx, posy) # Submatrix
    lines = Lines(pattern, posx, posy)   # Lines
    horizontal = lines[0]                # Horizontal line
    vertical = lines[1]                  # Vertical line

    possibles = [] # Empty list of the possible numbers that we can introduce
    # We will study each number between 1 and 10 
    # If it is not in any of the mentionated object we will introduce it on the list
    for value in range(1,10):
        if In(value, horizontal) + In(value, vertical) + In(value, matrix) == 0:
            possibles.append(value) 
 
    return possibles


def ZeroPostions(pattern, posx, posy):

    # Counts the number zeros in the submatrix and gives the position of each
    zeros_pos = []
 
    # As the value of the gap that we are studying it is zero we must remove that one from the list
    for pos1 in range(len(pattern)):
        sub_pattern = pattern[pos1] # One row of the matrix
        for pos2 in range(len(sub_pattern)):
            if sub_pattern[pos2] == 0: # In case the value of a number in the row is zero
                posXzeros = pos1 + 3*(posx//3) # X position of the zero we are studying
                posYzeros = pos2 + 3*(posy//3) # Y position of the zero we are studying

                # In case any of the (x,y) of the zero is diferent with the (x,y) of the gap
                if posXzeros != posx or posYzeros != posy: 
                    zeros_pos.append([posXzeros, posYzeros]) # We introduce this zeros in the list

    return zeros_pos # List with the positions of all the zeros in a submatrix



def Study(value, zeros_position):
    global Lines, In

    # Study if the horizontal or the vertical line in the zero positions contains a number with a certain value
    counter = 0

    # It will study each zero of the list
    for pos in zeros_position:
        lines = Lines(pattern, pos[0], pos[1])
        horizontal = lines[0] # Horizontal line of one zero
        vertical = lines[1]   # Vertical line of one zero

        # Just in case that the value is in both lines it will add nothing to the counter
        counter += abs(In(value, horizontal) * In(value, vertical) - 1)

    return counter


# The study will be finished when there is no zeros in the pattern
zeros = sum(pattern == 0)

while zeros > 0:
    # We will study each position of the pattern
    for i in range(len(pattern)):
        for j in range(len(pattern)):
            # In case the value of the number in the position is zero we will study that gap
            if pattern[i,j] == 0: 
                possibles = Possibles(pattern, i, j) # Posible values 
                zeros_position = ZeroPostions(Matrix(pattern, i, j), i, j) # Position of the zeros

                # Finally we study each possible value with the zeros in the submatrix
                for value in possibles: 
                    # If the counter of the study is zero, it means that the value can be introduce in the gap
                    if Study(value, zeros_position) == 0:
                        pattern[i,j] = value

    # Finally we recalculate how many zeros do we still have in the pattern
    zeros = sum(pattern == 0)
    # If it is not zero it will the same calculation again


# To show the solution in a visual way we will generate an image with the solution of the sudoku
# We will use the tool imshow from matplotlib
cmap = colors.ListedColormap([(1,1,1)]) # We define that the only colormap is white to have a white background
bounds=[0,10] # It will be white for any value
norm = colors.BoundaryNorm(bounds, cmap.N) # We create the colormap

# We create the figure where we will print the imshow
fig, ax = plt.subplots(figsize=(6,6))
ax.imshow(pattern.transpose(),cmap=cmap, norm=norm)
ax.tick_params(axis=u'both', which=u'both',length=0)
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

# We want to have the solution in a diffent color to make it more visual
for i_plot in range(len(pattern)):
    for j_plot in range(len(pattern)):
        # In case that the inicial value where zero we will add that number in red
        if initial_pattern.transpose()[i_plot, j_plot] == 0:
            color_plot = "#FF0000"
        else:
            color_plot = "#000000"

        # Finally we add the number in each position with its color
        ax.text(i_plot+0.02, j_plot+0.05, pattern.transpose()[i_plot, j_plot]
              , ha="center", va="center", fontsize=20, color = color_plot, fontweight="roman")

# To end we draw the lineas that defines the limits in each submatrix
for i in range(10):
    ax.axvline(i-0.5,c = "black",linewidth = 0.8)
    ax.axhline(i-0.5,c = "black",linewidth = 0.8)

for i in range(2):
    ax.axvline((9*i)-0.5,c = "black",linewidth = 4)
    ax.axhline((9*i)-0.5,c = "black",linewidth = 4)

for i in range(2):
    ax.axvline((3*i)+2.5,c = "black",linewidth = 2)
    ax.axhline((3*i)+2.5,c = "black",linewidth = 2)

plt.show()