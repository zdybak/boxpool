#Mate Superbowl Box Pool Automaton v0.1
# take a text file list of party animals,
# create a box pool with randomized team and value placement
# evenly but randomly assign squares to each of the party animals
# display the box pool

import random
import math

def get_party_animals(filename):
    with open(filename) as file:
        party_animals = file.read().split("\n")
    return party_animals

def create_box_pool(teams):
    rows = []
    cols = []
    for i in range(10):
        rows.append(i)
        cols.append(i)
    random.shuffle(rows)
    random.shuffle(cols)
    random.shuffle(teams)

    box_pool =  { 
        "teams" : teams,
        "rows" : rows,
        "cols" : cols,
    }

    return box_pool

def assign_party_animals_to_cells_randomly(party_animals):
    #create a list of 100 cells, then put the indices in random order
    available_cells = []
    for i in range(100):
        available_cells.append(i)
    random.shuffle(available_cells)

    #calculate the number of cells per party animal
    number_animals = len(party_animals)
    cells_per_animal = math.floor(100 / number_animals)
    left_over_cells = 100 % number_animals

    #iterate through each party animal and build a dictionary of randomly allocated cells
    final_cell_assignment = {}
    for animal in party_animals:
        for i in range(cells_per_animal):
            cell_index = available_cells.pop()
            final_cell_assignment[cell_index] = animal
    
    #the uneven remainder get marked with FS for now
    while len(available_cells) > 0:
        cell_index = available_cells.pop()
        final_cell_assignment[cell_index] = "FREE SPACE"
    
    return final_cell_assignment

def print_box_pool(box_pool, cell_assignment):
    #for each row lead with a space to provide room for row team name
    
    #handle horizontal vertices via linestr
    linestr = ""
    for i in range(100):
        linestr+="-"

    #print col wise team name
    print("  ",box_pool["teams"][0].rjust(50-math.floor(len(box_pool["teams"][0])/2)))

    #print top row scores
    rowstr = "  "
    for score in box_pool["cols"]:
        rowstr = rowstr+ "|    "+str(score)+"    "
    print(rowstr)

    #calculate when row team should be spelled
    row_team_min = 10-math.floor(len(box_pool["teams"][1])/2)
    row_team_max = row_team_min + len(box_pool["teams"][1])
    #now loop through cell assignment and print out the rows
    rowline = 1
    cell_index = 0
    
    while cell_index < 100:
        if rowline >= row_team_min and rowline < row_team_max:
            rowstr = box_pool["teams"][1][rowline-row_team_min]+" "
        else:
            rowstr = "  "
        
        if rowline % 2 != 0:
            print(rowstr+linestr)
            rowline+=1
            continue
        else:
            #get the row score here
            if rowstr != "  ":
                rowstr = rowstr[0:1] +str(box_pool["rows"].pop())
            else:
                rowstr = " " +str(box_pool["rows"].pop())
            #pop off ten from the cell assignment and print the names, truncating if greater than ten
            for i in range(10):
                cell_owner = cell_assignment[cell_index]
                if len(cell_owner) > 9:
                    cell_owner = cell_owner[:9]
                cell_owner = cell_owner
                cell_index += 1
                rowstr += "|"
                rowstr += f"{cell_owner:^9}"
            print(rowstr)
            rowline+=1

#main execution
pa = get_party_animals("guestlist.txt")
teams = ["Chiefs", "Ravens"]
bp = create_box_pool(teams)
ca = assign_party_animals_to_cells_randomly(pa)
print_box_pool(bp,ca)