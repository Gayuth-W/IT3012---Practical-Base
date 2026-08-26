# agent.py

from collections import deque
import heapq
import math
import random

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SearchAgent:

    def __init__(self):
        self.plan = []
        self.active_algo = "AStar"
        
    def manhattan_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal

        return abs(x1 - x2) + abs(y1 - y2)

    def euclidean_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal

        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)        

    def get_neighbors(self, state, grid_size, walls):
        x, y = state
        width, height = grid_size

        possible_moves = [
            ("Up", (x, y + 1)),
            ("Down", (x, y - 1)),
            ("Left", (x - 1, y)),
            ("Right", (x + 1, y)),
        ]

        neighbors = []

        for action, next_state in possible_moves:
            nx, ny = next_state

            inside_grid = (
                0 <= nx < width and
                0 <= ny < height
            )

            if inside_grid and next_state not in walls:
                neighbors.append((action, next_state))

        return neighbors

    def bfs_search(self, start, goal, grid_size, walls):
        frontier = deque([(start, [])])
        reached = {start}

        while frontier:
            state, path = frontier.popleft()

            if state == goal:
                return path

            for action, next_state in self.get_neighbors(state, grid_size, walls):
                if next_state not in reached:
                    reached.add(next_state)
                    new_path = path + [action]
                    frontier.append((next_state, new_path))

        return []

    def dfs_search(self, start, goal, grid_size, walls):
        frontier = [(start, [])]
        reached = {start}

        while frontier:
            state, path = frontier.pop()

            if state == goal:
                return path

            for action, next_state in self.get_neighbors(state, grid_size, walls):
                if next_state not in reached:
                    reached.add(next_state)
                    new_path = path + [action]
                    frontier.append((next_state, new_path))

        return []

    def ucs_search(self, start, goal, grid_size, walls):
        frontier = [(0, start, [])]
        reached = set()

        while frontier:
            cost, state, path = heapq.heappop(frontier)

            if state in reached:
                continue

            reached.add(state)

            if state == goal:
                return path

            for action, next_state in self.get_neighbors(state, grid_size, walls):
                if next_state not in reached:
                    step_cost = 1
                    new_cost = cost + step_cost
                    new_path = path + [action]

                    heapq.heappush(frontier, (new_cost, next_state, new_path))

        return []

    def sense_and_act(self, percept, agent_pos=None):
        if agent_pos is None:
            agent_pos = percept["agent_pos"]

        start = tuple(agent_pos)
        grid_size = tuple(percept["grid_size"])
        walls = set(percept["walls"])
        remaining_food = percept.get(
            "remaining_food",
            percept.get("all_food", []),
        )

        if not remaining_food:
            return "Stay"

        if not self.plan:
            closest_food = min(
                remaining_food,
                key=lambda food: (
                    abs(food[0] - start[0])
                    + abs(food[1] - start[1])
                ),
            )

            goal = tuple(closest_food)

            if self.active_algo == "BFS":
                self.plan = self.bfs_search(
                    start,
                    goal,
                    grid_size,
                    walls,
                )

            elif self.active_algo == "DFS":
                self.plan = self.dfs_search(
                    start,
                    goal,
                    grid_size,
                    walls,
                )

            elif self.active_algo == "UCS":
                self.plan = self.ucs_search(
                    start,
                    goal,
                    grid_size,
                    walls,
                )

            elif self.active_algo == "AStar":
                    self.plan = self.astar_search(
                    start,
                    goal,
                    walls,
                    grid_size,
                    heuristic_type="manhattan"
                )   
            
            else:
                raise ValueError(
                    f"Unknown algorithm: {self.active_algo}"
                )

        if self.plan:
            return self.plan.pop(0)

        return "Stay"
    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        
        """Find a path from start_pos to goal_pos using A* search."""
        if heuristic_type == "manhattan":
            heuristic = self.manhattan_distance
        elif heuristic_type == "euclidean":
            heuristic = self.euclidean_distance
        else:
            raise ValueError(
                "heuristic_type must be 'manhattan' or 'euclidean'"
            )

        priority_queue = []
        reached_states = set()

        start_g_cost = 0
        start_h_cost = heuristic(start_pos, goal_pos)
        start_f_cost = start_g_cost + start_h_cost

        heapq.heappush(
            priority_queue,
            (start_f_cost, start_g_cost, start_pos, []),
        )   
        
        while priority_queue:
            f_cost, g_cost, current_pos, path_taken = heapq.heappop(
                priority_queue
            )

            if current_pos == goal_pos:
                return path_taken

            if current_pos in reached_states:
                continue

            reached_states.add(current_pos)

            for action, neighbor in self.get_neighbors(
                current_pos,
                grid_size,
                walls,
            ):
                if neighbor not in reached_states:
                    new_g_cost = g_cost + 1
                    new_h_cost = heuristic(neighbor, goal_pos)
                    new_f_cost = new_g_cost + new_h_cost
                    new_path = path_taken + [action]

                    heapq.heappush(
                        priority_queue,
                        (new_f_cost, new_g_cost, neighbor, new_path),
                    )

        return []        
    
if __name__ == "__main__":
    agent = SearchAgent()

    start_position = (0, 0)
    goal_position = (3, 4)

    # Manhattan Distance: 7
    print(
    "Manhattan Distance:",
    agent.manhattan_distance(start_position, goal_position),
    )

    # Euclidean Distance: 5.0
    print(
    "Euclidean Distance:",
    agent.euclidean_distance(start_position, goal_position),
    )    