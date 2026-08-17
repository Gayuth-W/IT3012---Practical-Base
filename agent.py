# agent.py

from collections import deque
import heapq

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SearchAgent:
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