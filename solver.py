
grid = [[2, 1, 1, 0, 4],
        [3, 3, 4, 0, 2],
        [3, 1, 2, 0, 4],
        [1, 2, 3, 0, 4]]

grid = [[1, 4, 7, 6, 2, 3, 6, 5, 1, 0, 0],
        [2, 5, 3, 7, 9, 5, 1, 9, 8, 0, 0],
        [3, 1, 8, 7, 9, 7, 9, 5, 6, 0, 0],
        [4, 6, 4, 2, 8, 4, 3, 8, 2, 0, 0]]

size_tube = len(grid)
nb_tubes  = len(grid[0])

moves = []
impossible_moves = []
positions_reached = []

def compute_start_tubes():
    """A start tube is a column of start grid
    """
    global tubes
    tubes = []
    
    for i, line in enumerate(grid[::-1]):
        for j, elem in enumerate(line):
            if i == 0:
                # Add tube in tubes
                tubes.append([])
            
            # Add elem in tube (0 is empty elem)
            if elem != 0:
                tubes[j].append(elem)
                
    print_game()

def print_game():
    for h in range(size_tube, 0, -1):
        line = ""
        for tube in tubes:
            if len(tube) >= h:
                line += str(tube[h-1]) + " "
            else:
                line += "- "
        print(line)
    print()
    
def tubes_to_position():
    pos = ""
    for tube in tubes:
        for elem in tube:
            pos += str(elem)

        # Add 0 for empty elem
        for _ in range(len(tube), size_tube):
            pos += "0"
            
    return pos
    
def position_to_tubes(pos):
    tubes = []
    i = 0
    for _ in range(nb_tubes):
        tubes.append([])
        for _ in range(size_tube):
            if pos[i] != "0":
                tubes[-1].append(pos[i])
            i += 1

def possible(src, dst):
    """Check if move is possible and execute it if it is.
    tube_src must be different from tube_dst
    tube_src must not be empty
    tube_src must contain at least 2 different elements to be poured in an empty tube_dst
    tube_dst must not be full
    tube_dst must be empty or his last color must be the same as tube_src's
    move must not create a list of moves that is known impossible
    move must not create a position reached before
    """
    tube_src = tubes[src]
    tube_dst = tubes[dst]
    
    if src == dst:
        return False
    if not tube_src:
        return False
    if all(x==tube_src[0] for x in tube_src) and not tube_dst:
        return False
    if not len(tube_dst) < size_tube:
        return False
    if not (not tube_dst or tube_src[-1] == tube_dst[-1]):
        return False
        
    moves.append((src, dst))    
    if moves in impossible_moves:
        print("Move ("+str(src)+", "+str(dst)+") is impossible")
        moves.pop()
        return False
    
    position_before_move = tubes_to_position()
    pour(tube_src, tube_dst)
    position_after_move = tubes_to_position()
    
    if position_after_move in positions_reached:
        print("Position reached already, move impossible")
        moves.pop()
        position_to_tubes(position_before_move)
        return False
    else:
        positions_reached.append(position_after_move)
    
    return True
        
def pour(tube_src, tube_dst):
    """Pouring has to be done all the way
    """
    while tube_src and (not tube_dst or tube_src[-1] == tube_dst[-1]) and len(tube_dst) < size_tube:
        tube_dst.append(tube_src.pop())
        
    print(moves)
    print_game()
    
def redo_moves_from_start():
    print("redo_moves_from_start")
    
    compute_start_tubes()
    for move in moves:
        pour(tubes[move[0]], tubes[move[1]])

def check_tube_finished(tube):
    """ Return True if tube is empty or full of the same element
    """
    # Check if tube is empty
    if not tube:
        return True
    
    # Check if tube is full of the same element
    if len(tube) == size_tube and all(x==tube[0] for x in tube):
        return True
    
    return False

def brute_force():
    """Recursive search with backtracking
    """
    # Find move
    for i in range(len(tubes)):
        for j in range(len(tubes)):
            if possible(i, j):
                brute_force()
                    
            # Check win
            is_solved = True
            for tube in tubes:
                if not check_tube_finished(tube):
                    is_solved = False
                    
            if is_solved:
                input("Solved.")
                return
    
    # Algorithm goes here if no more move is possible
    impossible_moves.append(moves.copy())
    print("Impossible moves:")
    for i in impossible_moves:
        print(i)
    print()
    
    # Because we don't know how much every move poured, we can't reverse moves
    # Instead of storing how much was poured for every move, we start over and play all moves but last one
    moves.pop()
    redo_moves_from_start()

# Solving script
if __name__ == "__main__":
    compute_start_tubes()
    
    brute_force()
    