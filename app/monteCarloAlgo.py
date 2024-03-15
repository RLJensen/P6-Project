import random

def estimate_pi(num_points):
    points_inside_circle = 0
    total_points = num_points

    for _ in range(num_points):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        distance = x**2 + y**2

        if distance <= 1:
            points_inside_circle += 1

    # Pi is approximated by 4 * (number of points inside circle) / (total number of points)
    pi_estimate = 4 * points_inside_circle / total_points
    return pi_estimate

    
    