
grid = [[2, 1, 1, 0, 4],
        [3, 3, 4, 0, 2],
        [3, 1, 2, 0, 4],
        [1, 2, 3, 0, 4]]

grid = [[1, 4, 7, 6, 2, 3, 6, 5, 1, 0, 0],
        [2, 5, 3, 7, 9, 5, 1, 9, 8, 0, 0],
        [3, 1, 8, 7, 9, 7, 9, 5, 6, 0, 0],
        [4, 6, 4, 2, 8, 4, 3, 8, 2, 0, 0]]

size_tube = len(grid)
#nb_tubes  = len(grid[0])

moves = []
impossible_moves = []

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
        
def possible(src, dst):
    """
    tube_src must be different from tube_dst
    tube_src must not be empty
    tube_dst must not be full
    tube_dst must be empty or his last color must be the same as tube_src's
    move must not create a list of moves that is known impossible
    move must not be the last move reversed
    """
    tube_src = tubes[src]
    tube_dst = tubes[dst]
    
    if src == dst:
        return False
    if not tube_src:
        return False
    if not len(tube_dst) < size_tube:
        return False
    if not (not tube_dst or tube_src[-1] == tube_dst[-1]):
        return False
        
    moves.append((src, dst))    
    if moves in impossible_moves:
        moves.pop()
        print("Move ("+str(src)+", "+str(dst)+") is impossible")
        return False
    
    if moves and moves[-1] == (dst, src):
        return False
    
    return True
        
def pour(tube_src, tube_dst):
    """Pouring has to be done all the way
    """
    while tube_src and (not tube_dst or tube_src[-1] == tube_dst[-1]) and len(tube_dst) < 4:
        tube_dst.append(tube_src.pop())
        
    print(moves)
    print_game()
    
def redo_moves_from_start():
    print("redo_moves_from_start")
    
    compute_start_tubes()
    for move in moves:
        pour(tubes[move[0]], tubes[move[1]])

def brute_force():
    """Recursive search with backtracking
    """
    # Find move
    for i in range(len(tubes)):
        for j in range(len(tubes)):
            if possible(i, j):
                pour(tubes[i], tubes[j])
                brute_force()
                    
            # Check win
            is_solved = True
            for tube in tubes:
                # Check if all elements in a tube are the same
                if not all(x==tube[0] for x in tube):
                    is_solved = False
                
                # Check if all tubes are either full or empty
                if len(tube) != 0 and len(tube) != 4:
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
    