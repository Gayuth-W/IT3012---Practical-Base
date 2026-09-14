import random

def local_beam_search(initial_states, k, max_iters, objective_fn):
    """
    initial_states: list of k randomly generated starting positions
    k: the beam width (number of states to keep)
    objective_fn: the function we are trying to maximize
    """
    current_states = initial_states

    for iteration in range(max_iters):
        all_successors = []
        for state in current_states:
            for _ in range(5):
                neighbor = state + random.uniform(-10, 10)
                fit = objective_fn(neighbor)
                all_successors.append((neighbor, fit))

        all_successors.sort(key=lambda x: x[1], reverse=True)
        current_states = [item[0] for item in all_successors[:k]]

    return max(current_states, key=objective_fn)


if __name__ == "__main__":
    random.seed(42)
    objective_fn = lambda x: -(x - 10) ** 2 + 100

    k = 3
    max_iters = 20
    initial_states = [random.uniform(-50, 50) for _ in range(k)]

    best_state = local_beam_search(
        initial_states,
        k,
        max_iters,
        objective_fn
    )

    print("Best state found:", best_state)

    if abs(best_state - 10) < 5:
        print("Success! Local Beam Search is working correctly.")
    else:
        print("Try again. Search did not converge near the optimum.")