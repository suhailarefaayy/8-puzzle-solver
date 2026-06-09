import tkinter as tk
from tkinter import messagebox


class Node:
    state = None
    parentstate = None
    action = None
    edgeCost = None
    #g(n) : cost mn start lehad current 
    gOfN = None
    #h(n) : estimated cost mn current lehad goal 
    #for A* and greedy
    hOfN = None
    heuristicFn = None

    def __init__(self, value):
        self.value = value
        self.state = value
        self.parentstate = None
        self.action = None
        self.edgeCost = 1
        self.gOfN = 0
        self.hOfN = 0
        self.heuristicFn = None


class SearchAlgorithms:
    Path = []
    fullPath = []
    totalCost = -1

    def __init__(self, start, end):
        self.start = start
        self.end = end
        #This creates an empty path for this specific search object.
        #It will later store the moves needed to solve the puzzle.
        self.Path = []
        self.fullPath = []
        self.totalCost = -1

    #bnshuf makan el faragh fen
    def get_blank_index(self, state):
        for i in range(len(state)):
            if state[i] == 0:
                return i
        return -1

    #bnshuf el faragh ye2dar yetharak fen 
    def get_children(self, node):
        children = []
        #shakl el puzzle now
        state = node.state
        blank_index = self.get_blank_index(state)

        moves = []
        #ashan awel row 0 1 2
        if blank_index >= 3:
            moves.append(("UP", blank_index - 3))
        #ashan akher row 6 7 8
        if blank_index <= 5:
            moves.append(("DOWN", blank_index + 3))
        #ashan awel col 0 3 6
        if blank_index % 3 != 0:
            moves.append(("LEFT", blank_index - 1))
        #ashan akher col 2 5 8
        if blank_index % 3 != 2:
            moves.append(("RIGHT", blank_index + 1))

        #loop 3ala possible moves
        for action, new_index in moves:
            #3ashan manghyrsh fel parent bel ghalat
            child_state = state.copy()
            temp = child_state[blank_index]
            child_state[blank_index] = child_state[new_index]
            child_state[new_index] = temp

            #el shakl el gedeed ba3d el move
            child = Node(child_state)
            #bnrbot el child bel parent bta3o ashan neb2a ne3raf el tare2 el meshenah 
            child.parentstate = node
            child.action = action
            child.edgeCost = 1
            #cost mn start lehad current node + cost one move (1 f kol el ahwal)
            child.gOfN = node.gOfN + child.edgeCost
            children.append(child)

        return children

    #h1 = kam tile msh fi makanha 
    def misplaced(self, state):
        count = 0
        for i in range(len(state)):
            if state[i] != 0 and state[i] != self.end[i]:
                count += 1
        return count

    #h2 = kol tile be3eda ad eh 3an el goal bta3ha
    def manhattan(self, state):
        total = 0
        for i in range(len(state)):
            tile = state[i]
            if tile != 0:
                #bndwar ala makanha fel goal
                goal_i = self.end.index(tile)
                #i//3 = row , i%3 = column
                total += abs((i // 3) - (goal_i // 3)) + abs((i % 3) - (goal_i % 3))
        return total

    #manhattan distance bas bnzwd cost law two tile blocking ba3d
    def linear_conflict(self, state):
        total = self.manhattan(state)
        for row in range(3):
            row_tiles = []
            for col in range(3):
                #hangeb indices el fel list(1*3+2 = index 5)
                index = row * 3 + col
                tile = state[index]
                #nshuf row el tile f nafs row el goal?
                if tile != 0 and self.end.index(tile) // 3 == row:
                    row_tiles.append(tile)

            for i in range(len(row_tiles)):
                for j in range(i + 1, len(row_tiles)):
                    if self.end.index(row_tiles[i]) > self.end.index(row_tiles[j]):
                        #fi wahda mn tiles hattl3 bara row temp fa this costs at least 2 moves
                        total += 2

        for col in range(3):
            col_tiles = []
            for row in range(3):
                index = row * 3 + col
                tile = state[index]
                if tile != 0 and self.end.index(tile) % 3 == col:
                    col_tiles.append(tile)

            for i in range(len(col_tiles)):
                for j in range(i + 1, len(col_tiles)):
                    if self.end.index(col_tiles[i]) > self.end.index(col_tiles[j]):
                        total += 2

        return total

    def set_heuristics(self, node):
        h1 = self.misplaced(node.state)
        h2 = self.manhattan(node.state)
        h3 = self.linear_conflict(node.state)

        node.heuristicFn = [h1, h2, h3]
        node.hOfN = h3

    def save_result(self, node):
        path = []
        full_path = []
        current = node
        while current is not None:
            #0 ashan ehna bnhot el goal fel awel fa n reverse it
            full_path.insert(0, current.state)
            if current.action is not None:
                path.insert(0, current.action)
            current = current.parentstate

        self.Path = path
        self.fullPath = full_path
        self.totalCost = node.gOfN

        SearchAlgorithms.Path = self.Path
        SearchAlgorithms.fullPath = self.fullPath
        SearchAlgorithms.totalCost = self.totalCost

        return self.Path, self.fullPath, self.totalCost

    #a2al path cost g(n)
    def UCS(self):
        start_node = Node(self.start)
        frontier = [start_node]
        #{state : best cost}
        explored = {} #changed

        #tol ma fi nodes to be explored lesa
        while len(frontier) != 0:
            #bnkhaly a2al cost mn start lel current teb2a el awel
            frontier.sort(key=lambda node: node.gOfN)
            #bnakhud ba a2al cost
            current = frontier.pop(0)
            current_key = tuple(current.state) #changed

            if current_key in explored and explored[current_key] <= current.gOfN: #changed
                continue
                        
            #ahsan cost leha till now
            explored[current_key] = current.gOfN #changed

            if current.state == self.end:
                return self.save_result(current)


            #bnshuf kol el possible next states mn el current
            children = self.get_children(current)

            for child in children:
                child_key = tuple(child.state) #changed
                if child_key in explored and explored[child_key] <= child.gOfN: #changed
                    continue

                old_node = None #changed
                for node in frontier:
                    if node.state == child.state:
                        old_node = node #changed
                        break

                if old_node is None: #changed
                    #hn explore them later ba w n sort
                    frontier.append(child)
                elif child.gOfN < old_node.gOfN: #changed
                    frontier.remove(old_node) #changed
                    frontier.append(child)

        return self.Path, self.fullPath, self.totalCost

    def BFS(self):
        start_node = Node(self.start)
        frontier = [start_node]
        explored = []

        while len(frontier) != 0:
            #FIFO
            current = frontier.pop(0)

            if current.state == self.end:
                return self.save_result(current)

            if current.state in explored:
                continue

            explored.append(current.state)
            children = self.get_children(current)

            for child in children:
                if child.state not in explored:
                    #bn add at the back w bn remove from front
                    frontier.append(child)

        return self.Path, self.fullPath, self.totalCost

    def DFS(self):
        start_node = Node(self.start)
        frontier = [start_node]
        explored = []

        while len(frontier) != 0:
            #LIFO
            current = frontier.pop(0)

            if current.state == self.end:
                return self.save_result(current)

            if current.state in explored:
                continue

            explored.append(current.state)
            children = self.get_children(current)
            #3ashan bn-insert childern at front
            children.reverse()

            for child in children:
                if child.state not in explored:
                    #3ashan n-explore newest child el awel fa n go deeper
                    frontier.insert(0, child)

        return self.Path, self.fullPath, self.totalCost

    #bnkhtar smallest f(n) = g(n) + h(n)
    def Astar(self):
        start_node = Node(self.start)
        self.set_heuristics(start_node)
        frontier = [start_node]
        explored = {} #changed

        while len(frontier) != 0:
            #n-sort hasab a2al f(n) = g(n) + h(n)
            frontier.sort(key=lambda node: node.gOfN + node.hOfN)
            current = frontier.pop(0)
            current_key = tuple(current.state) #changed


            if current_key in explored and explored[current_key] <= current.gOfN: #changed
                continue

            explored[current_key] = current.gOfN #changed

            if current.state == self.end:
                return self.save_result(current)
            
            children = self.get_children(current)

            for child in children:
                #3ashan ne3raf h(n)
                self.set_heuristics(child)
                child_key = tuple(child.state) #changed

                if child_key in explored and explored[child_key] <= child.gOfN: #changed
                    continue

                old_node = None #changed
                for node in frontier:
                    if node.state == child.state:
                        old_node = node #changed
                        break

                if old_node is None: #changed
                    frontier.append(child)
                elif child.gOfN < old_node.gOfN: #changed
                    frontier.remove(old_node) #changed
                    frontier.append(child)

        return self.Path, self.fullPath, self.totalCost

    #asghar h(n)
    def Greedy(self):
        start_node = Node(self.start)
        self.set_heuristics(start_node)
        frontier = [start_node]
        explored = []

        while len(frontier) != 0:
            #n-sort b asghar h(n)
            frontier.sort(key=lambda node: node.hOfN)
            current = frontier.pop(0)

            if current.state == self.end:
                return self.save_result(current)

            if current.state in explored:
                continue

            explored.append(current.state)
            children = self.get_children(current)

            for child in children:
                if child.state not in explored:
                    self.set_heuristics(child)
                    frontier.append(child)

        return self.Path, self.fullPath, self.totalCost


def main():
    s3 = SearchAlgorithms([1, 2, 3, 4, 0, 6, 7, 5, 8], [1,2,3,4,5,6,7,8,0])
    path, fullPath, cost = s3.UCS()
    print('UCS Path: ' + str(path), end='\nFull Path is: ')
    print(fullPath)
    print(" + total Cost = " + str(cost))

    s4 = SearchAlgorithms([1, 2, 3, 4, 0, 6, 7, 5, 8], [1,2,3,4,5,6,7,8,0])
    path, fullPath, cost = s4.Astar()
    print('AstarHeuristic Path: ' + str(path), end='\nFull Path is: ')
    print(fullPath)
    print(" + total Cost = " + str(cost))

    s4 = SearchAlgorithms([1, 2, 3, 4, 0, 6, 7, 5, 8], [1,2,3,4,5,6,7,8,0])
    path, fullPath, cost = s4.Greedy()
    print('GreedyHeuristic Path: ' + str(path), end='\nFull Path is: ')
    print(fullPath)
    print(" + total Cost = " + str(cost))


class PuzzleGUI:
    def __init__(self):
        self.goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.start = [1, 2, 3, 4, 0, 6, 7, 5, 8]
        self.state = self.start.copy()
        self.solution_states = []
        self.solution_step = 0

        self.window = tk.Tk()
        self.window.title("8-Puzzle Solver")
        self.window.resizable(False, False)

        self.title_label = tk.Label(
            self.window,
            text="8-Puzzle Solver",
            font=("Arial", 20, "bold"),
            fg="#0b4f71"
        )
        self.title_label.grid(row=0, column=0, columnspan=5, padx=12, pady=(12, 4))

        self.buttons = []
        self.board_frame = tk.Frame(self.window)
        self.board_frame.grid(row=1, column=0, columnspan=3, padx=12, pady=12)

        for i in range(9):
            button = tk.Button(
                self.board_frame,
                text="",
                font=("Arial", 22, "bold"),
                width=4,
                height=2,
                command=lambda index=i: self.tile_clicked(index)
            )
            button.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self.buttons.append(button)

        self.info_frame = tk.Frame(self.window)
        self.info_frame.grid(row=1, column=3, columnspan=2, padx=12, pady=12, sticky="n")

        self.h1_label = tk.Label(self.info_frame, text="", font=("Arial", 11), anchor="w", width=30)
        self.h1_label.pack(anchor="w", pady=3)

        self.h2_label = tk.Label(self.info_frame, text="", font=("Arial", 11), anchor="w", width=30)
        self.h2_label.pack(anchor="w", pady=3)

        self.h3_label = tk.Label(self.info_frame, text="", font=("Arial", 11), anchor="w", width=30)
        self.h3_label.pack(anchor="w", pady=3)

        self.dom_label = tk.Label(self.info_frame, text="", font=("Arial", 10, "bold"), anchor="w", width=30)
        self.dom_label.pack(anchor="w", pady=(8, 3))

        self.result_label = tk.Label(
            self.window,
            text="Click an adjacent tile or choose an algorithm.",
            font=("Arial", 11),
            wraplength=520
        )
        self.result_label.grid(row=2, column=0, columnspan=5, padx=12, pady=6)

        self.algorithm_frame = tk.Frame(self.window)
        self.algorithm_frame.grid(row=3, column=0, columnspan=5, padx=12, pady=8)

        algorithms = ["A*", "UCS", "Greedy", "BFS", "DFS"]
        for i in range(len(algorithms)):
            button = tk.Button(
                self.algorithm_frame,
                text=algorithms[i],
                width=9,
                command=lambda name=algorithms[i]: self.solve(name)
            )
            button.grid(row=0, column=i, padx=3)

        self.next_button = tk.Button(self.window, text="Next Step", width=12, command=self.next_step)
        self.next_button.grid(row=4, column=0, padx=5, pady=(0, 12))

        self.reset_button = tk.Button(self.window, text="Reset", width=12, command=self.reset)
        self.reset_button.grid(row=4, column=1, padx=5, pady=(0, 12))

        self.goal_button = tk.Button(self.window, text="Goal", width=12, command=self.show_goal)
        self.goal_button.grid(row=4, column=2, padx=5, pady=(0, 12))

        self.update_screen()

    def update_screen(self):
        for i in range(9):
            value = self.state[i]
            if value == 0:
                self.buttons[i].config(text="", bg="#f7f7f7", relief="sunken")
            elif value == self.goal[i]:
                self.buttons[i].config(text=str(value), bg="#d9f5ec", relief="raised")
            else:
                self.buttons[i].config(text=str(value), bg="#ffe9c7", relief="raised")

        search = SearchAlgorithms(self.state, self.goal)
        h1 = search.misplaced(self.state)
        h2 = search.manhattan(self.state)
        h3 = search.linear_conflict(self.state)

        self.h1_label.config(text="h1 - Misplaced tiles: " + str(h1))
        self.h2_label.config(text="h2 - Manhattan distance: " + str(h2))
        self.h3_label.config(text="h3 - Linear conflict: " + str(h3))

        if h3 >= h2 and h2 >= h1 and h1 >= 0:
            self.dom_label.config(text="h3 >= h2 >= h1 >= 0 holds", fg="#0b6b46")
        else:
            self.dom_label.config(text="Check heuristic values", fg="#9b1c1c")

    def tile_clicked(self, index):
        blank = self.state.index(0)
        valid_moves = []

        if blank >= 3:
            valid_moves.append(blank - 3)
        if blank <= 5:
            valid_moves.append(blank + 3)
        if blank % 3 != 0:
            valid_moves.append(blank - 1)
        if blank % 3 != 2:
            valid_moves.append(blank + 1)

        if index in valid_moves:
            temp = self.state[blank]
            self.state[blank] = self.state[index]
            self.state[index] = temp
            self.solution_states = []
            self.solution_step = 0
            self.result_label.config(text="Moved tile " + str(self.state[blank]) + ".")
            self.update_screen()

    def solve(self, name):
        if not self.is_solvable(self.state):
            messagebox.showerror("Unsolvable", "This puzzle state cannot reach the goal.")
            return

        search = SearchAlgorithms(self.state.copy(), self.goal)

        if name == "A*":
            path, full_path, cost = search.Astar()
        elif name == "UCS":
            path, full_path, cost = search.UCS()
        elif name == "Greedy":
            path, full_path, cost = search.Greedy()
        elif name == "BFS":
            path, full_path, cost = search.BFS()
        else:
            path, full_path, cost = search.DFS()

        self.solution_states = full_path
        self.solution_step = 0

        self.result_label.config(
            text=(
                name + " path: " + str(path)
                + "\nfull path: " + str(full_path)
                + "\n total cost = " + str(cost)
            )
        )

        if len(full_path) > 0:
            self.state = full_path[0].copy()
            self.update_screen()

    def next_step(self):
        if len(self.solution_states) == 0:
            self.result_label.config(text="Choose an algorithm first.")
            return

        if self.solution_step < len(self.solution_states) - 1:
            self.solution_step += 1
            self.state = self.solution_states[self.solution_step].copy()
            self.result_label.config(
                text="Showing step " + str(self.solution_step) + " of " + str(len(self.solution_states) - 1)
            )
            self.update_screen()
        else:
            self.result_label.config(text="Goal reached.")

    def reset(self):
        self.state = self.start.copy()
        self.solution_states = []
        self.solution_step = 0
        self.result_label.config(text="Click an adjacent tile or choose an algorithm.")
        self.update_screen()

    def show_goal(self):
        self.state = self.goal.copy()
        self.solution_states = []
        self.solution_step = 0
        self.result_label.config(text="Goal state.")
        self.update_screen()

    def is_solvable(self, state):
        numbers = []
        for value in state:
            if value != 0:
                numbers.append(value)

        inversions = 0
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[i] > numbers[j]:
                    inversions += 1

        return inversions % 2 == 0

    def run(self):
        self.window.mainloop()


main()
gui = PuzzleGUI()
gui.run()
