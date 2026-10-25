import random

def generate_challenge():
    """Generates a target hidden curve for the Match the Graph challenge."""
    types = ["Linear", "Quadratic", "Trigonometric"]
    chosen_type = random.choice(types)
    
    if chosen_type == "Linear":
        target_params = {"m": round(random.uniform(-3, 3), 1), "c": round(random.uniform(-4, 4), 1)}
    elif chosen_type == "Quadratic":
        target_params = {
            "a": round(random.choice([-2, -1, -0.5, 0.5, 1, 2]), 1),
            "b": round(random.uniform(-3, 3), 1),
            "c": round(random.uniform(-3, 3), 1)
        }
    else:  # Trigonometric
        target_params = {
            "a": round(random.uniform(1, 3), 1),
            "b": round(random.uniform(0.5, 2), 1),
            "c": 0.0,
            "d": round(random.uniform(-2, 2), 1)
        }
    return chosen_type, target_params

def calculate_score(user_y, target_y):
    """Calculates MSE and match accuracy percentage."""
    import numpy as np
    mse = float(np.mean((user_y - target_y) ** 2))
    accuracy = max(0.0, 100.0 - (mse * 10))
    return round(mse, 3), round(accuracy, 1)
