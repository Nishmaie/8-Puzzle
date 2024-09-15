# 8 puzzles using simulated annealing 

from random import choice, shuffle, random
from math import exp

def copy_list(lst):
    return lst[:]


def row(abs_pos):
    return abs_pos // 3


def col(abs_pos):
    return abs_pos % 3


def index(row, col):
    return row * 3 + col

def print_puzzle(state):
    print(state)
    for r in range(3):
        for c in range(3):
            print(state[index(r, c)], end=" ")
        print("")


def all_moves(state):
    space = state.index(0)  
    r = row(space)
    c = col(space)
    moves = []
    if r > 0:
        moves.append("N")
    if r < 2:
        moves.append("S")
    if c > 0:
        moves.append("W")
    if c < 2:
        moves.append("E")
    return moves


def do_move(state, move):
    space = state.index(0)
    r = row(space)
    c = col(space)
    
    if move == "N":
        move_index = index(r - 1, c)
    elif move == "S":
        move_index = index(r + 1, c)
    elif move == "W":
        move_index = index(r, c - 1)
    elif move == "E":
        move_index = index(r, c + 1)
    

    state[space], state[move_index] = state[move_index], state[space]

def undo_move(state, move):
    if move == "N":
        do_move(state, "S")
    elif move == "S":
        do_move(state, "N")
    elif move == "W":
        do_move(state, "E")
    elif move == "E":
        do_move(state, "W")

# The energy of a state. It is calculated as the sum of Manhattan distances
def energy(state):
    total_energy = 0
    for i in range(1, 9):  
        current_position = state.index(i)
        goal_position = i - 1
        total_energy += abs(row(current_position) - row(goal_position)) + abs(col(current_position) - col(goal_position))
    return total_energy

def solved(state):
    return state == [1, 2, 3, 4, 5, 6, 7, 8, 0]


def sim_annealing(initial_state, max_moves, p=1):
    print("Starting from:")
    print_puzzle(initial_state)
    state = initial_state
    temperature = max_moves
    oldE = energy(state)
    
    while not solved(state) and temperature > 0:
        moves = all_moves(state)
        accepted = False
        while not accepted:
            m = choice(moves)
            do_move(state, m)
            newE = energy(state)
            deltaE = newE - oldE
            print(f"Move: {m}, Energy: {newE}, DeltaE: {deltaE}, Temp: {temperature}")
            if deltaE <= 0:
                accepted = True
            else:
                boltz = exp(-float(p * deltaE) / temperature)
                r = random()
                if r <= boltz:
                    accepted = True
            if not accepted:
                undo_move(state, m)
        oldE = newE
        temperature *= 0.95  # Exponential cooling
        print("Moving", m)
        print_puzzle(state)

def any_shuffle(state):
    shuffle(state)

def proper_shuffle(state, n=20):
    for i in range(n):
        m = choice(all_moves(state))
        do_move(state, m)

if __name__ == '__main__':
    puzzle = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    print("Initial energy:", energy(puzzle))
    proper_shuffle(puzzle, 10)
    print("Shuffled puzzle:")
    print_puzzle(puzzle)
    print("Energy after shuffle:", energy(puzzle))
    sim_annealing(puzzle, 1000, 0.5)  # Increased max_moves and adjusted p value
    if solved(puzzle):
        print("I solved your puzzle :)")
    else:
        print("Sorry, I couldn't solve it :(")
