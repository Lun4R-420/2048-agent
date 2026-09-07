import heuristics
from benchmark import run_benchmark

GAMES_PER_EVAL = 15
DEPTH = 3
MAX_ITERATIONS = 8
STEP_SIZE = 0.5

def fitness(weights):
    heuristics.WEIGHTS = weights
    win_rate, average_max_tile, average_played_moves = run_benchmark(GAMES_PER_EVAL, DEPTH)
    return win_rate * 10000 + average_max_tile

def hill_climb():
    current_weights = list(heuristics.WEIGHTS)
    current_score = fitness(current_weights)
    print(f"Starting weights: {current_weights}, score: {current_score}")

    for iteration in range(MAX_ITERATIONS):
        improved = False
        for i in range(4):
            up_candidate = list(current_weights)
            up_candidate[i] += STEP_SIZE
            up_score = fitness(up_candidate)

            down_candidate = list(current_weights)
            down_candidate[i] -= STEP_SIZE
            down_score = fitness(down_candidate)

            if up_score > current_score or down_score > current_score:
                improved = True
                if up_score > down_score:
                    current_score = up_score
                    current_weights = [weight for weight in up_candidate]
                else:
                    current_score = down_score
                    current_weights = [weight for weight in down_candidate]

        print(f"Iteration {iteration}: {current_weights}, score: {current_score}")

    return current_weights

def validate(tuned_weights, n=25):
    heuristics.WEIGHTS = [1, 1, -1, 1]
    baseline = run_benchmark(n, DEPTH)
    heuristics.WEIGHTS = tuned_weights
    tuned = run_benchmark(n, DEPTH)
    print(f"\nBaseline [1, 1, -1, 1] -> win_rate={baseline[0]}, avg_max_tile={baseline[1]}, avg_moves={baseline[2]}")
    print(f"Tuned {tuned_weights} -> win_rate={tuned[0]}, avg_max_tile={tuned[1]}, avg_moves={tuned[2]}")

if __name__ == "__main__":
    final_weights = hill_climb()
    print(f"\nFinal weights found: {final_weights}")
    validate(final_weights)