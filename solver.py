
# Depth first search or breadth first search
DEPTH_FIRST_SEARCH = False

grid = [[2, 1, 1, 0, 4],
        [3, 3, 4, 0, 2],
        [3, 1, 2, 0, 4],
        [1, 2, 3, 0, 4]]

grid = [[1, 4, 7, 6, 2, 3, 6, 5, 1, 0, 0],
        [2, 5, 3, 7, 9, 5, 1, 9, 8, 0, 0],
        [3, 1, 8, 7, 9, 7, 9, 5, 6, 0, 0],
        [4, 6, 4, 2, 8, 4, 3, 8, 2, 0, 0]]

grid = [[2, 4, 7, 6, 0, 3, 6, 0, 1, 0, 0],
        [2, 5, 3, 7, 9, 5, 1, 9, 8, 0, 0],
        [3, 1, 8, 7, 9, 7, 9, 5, 6, 0, 0],
        [4, 6, 4, 2, 8, 4, 3, 8, 2, 1, 5]]

"""
######## 0  1  2  3  4  5  6  7  8  9  A
grid = [[0, 6, 0, 2, 4, 3, 0, 0, 7, 1, 5],
        [0, 6, 0, 2, 8, 9, 3, 9, 7, 1, 5],
        [4, 6, 0, 2, 8, 8, 3, 9, 7, 1, 5],
        [4, 6, 0, 2, 8, 4, 3, 9, 7, 1, 5]]
"""
size_tube = len(grid)
nb_tubes  = len(grid[0])

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
    """Return string encoding tubes contents
    """
    pos = ""
    for tube in tubes:
        for elem in tube:
            pos += str(elem)

        # Add 0 for empty elem
        for _ in range(len(tube), size_tube):
            pos += "0"
            
    return pos
    
def position_to_tubes(pos):
    """Fill tubes by decoding a string
    """
    global tubes
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
    Rules for a move to be possible:
    tube_src must not be tube_dst
    tube_src must not be empty
    tube_dst must not be full
    if tube_dst is empty, tube_src must contain at least 2 different elements
    if tube_dst isn't empty, tube_src and tube_dst must have the same last color
    move must not create a position reached before
    """
    tube_src = tubes[src]
    tube_dst = tubes[dst]
    
    # Tube checking
    if src == dst:
        return False
    if not tube_src:
        return False
    if len(tube_dst) >= size_tube:
        return False
    
    if not tube_dst:
        if all(x==tube_src[0] for x in tube_src):
            return False
    else:
        if tube_src[-1] != tube_dst[-1]:
            return False
        
    # Try move
    moves.append((src, dst))
    
    # Save position in case of rollback needed, then pour
    position_before_move = tubes_to_position()    
    pour(tube_src, tube_dst)
    position_after_move = tubes_to_position()
    
    # Check if position was already reached
    if position_after_move in positions_reached:
        # Check if we found a faster way to reach this position
        if positions_reached[position_after_move] > len(moves):
            # Faster way, remember the new number of moves and don't rollback
            positions_reached[position_after_move] = len(moves)
            
        else:
            #print("Position reached already")
            moves.pop()
            position_to_tubes(position_before_move)
            return False            
    else:
        # Remember we reached this position and how many moves it needed
        positions_reached[position_after_move] = len(moves)
        
    return True
    
def pour(tube_src, tube_dst):
    """Pouring has to be done all the way
    """
    while tube_src and (not tube_dst or tube_src[-1] == tube_dst[-1]) and len(tube_dst) < size_tube:
        tube_dst.append(tube_src.pop())
        
    #print(moves)
    #print_game()
    
def redo_moves_from_start():
    compute_start_tubes()
    for move in moves:
        pour(tubes[move[0]], tubes[move[1]])
        
def rollback_last_move():
    if moves:
        moves.pop()
        
    # Because we don't know how much every move poured, we can't reverse moves
    # Instead of storing how much was poured for every move, we start over and play all moves but last one
    redo_moves_from_start()
    
def check_tube_finished(tube):
    """Return True if tube is empty or full of the same element
    """
    # Check if tube is empty
    if not tube:
        return True
    
    # Check if tube is full of the same element
    if len(tube) == size_tube and all(x==tube[0] for x in tube):
        return True
    
    return False
    
def brute_force_dfs():
    """Recursive search DFS with backtracking
    """
    global shortest_nb_winning_moves
    global solvable
    
    # Find move
    for i in range(len(tubes)):
        for j in range(len(tubes)):
            if len(moves) < shortest_nb_winning_moves and possible(i, j):
                brute_force_dfs()
                    
            # Check solved when no more move is possible
            is_solved = True
            for tube in tubes:
                if not check_tube_finished(tube):
                    is_solved = False
                    
            if is_solved:
                solvable = True
                if shortest_nb_winning_moves > len(moves):
                    shortest_nb_winning_moves = len(moves)
                    print("Solved in " + str(shortest_nb_winning_moves) + " moves:")
                    
                print(moves)
                
                # If solved, rollback last move to try something else
                rollback_last_move()
    
    # If no more move is possible, rollback last move to try something else
    rollback_last_move()
    
def brute_force_bfs():
    """Recursive search BFS
    """
    global solvable
    
    # Find move
    for i in range(len(tubes)):
        for j in range(len(tubes)):
            if len(moves) < shortest_nb_winning_moves and possible(i, j):
                brute_force_bfs()
                    
                # Check solved
                is_solved = True
                for tube in tubes:
                    if not check_tube_finished(tube):
                        is_solved = False
                        
                if is_solved:
                    solvable = True
                    print(moves)
                
                # Reached max number of moves, can't go further in recursion
                rollback_last_move()
                
# Solving script
if __name__ == "__main__":

    # Depth first search
    if DEPTH_FIRST_SEARCH:
        print("Start solving with DFS, fastest to find a solution.")
        
        solvable = False
        shortest_nb_winning_moves = 100
        
        moves = []
        positions_reached = {}
        
        compute_start_tubes()
        brute_force_dfs()
        
        if solvable:
            print("All shortest solutions found.")
            print("shortest_nb_winning_moves=" + str(shortest_nb_winning_moves))
        else:
            print("Not solvable.")
    
    # Breadth first search
    else:
        print("Start solving with BFS, fastest to find the shortest solution.")
        
        solvable = False
        shortest_nb_winning_moves = 0
        nb_previous_positions_reached = 0
        
        while not solvable:
            print("Not solvable in " + str(shortest_nb_winning_moves) + " moves.")
            
            shortest_nb_winning_moves += 1
        
            moves = []
            positions_reached = {}
                
            compute_start_tubes()
            brute_force_bfs()
            
            if nb_previous_positions_reached < len(positions_reached):
                nb_previous_positions_reached = len(positions_reached)
            else:
                print("Not solvable.")
                break
        
        print("All shortest solutions found.")
        print("shortest_nb_winning_moves=" + str(shortest_nb_winning_moves))
