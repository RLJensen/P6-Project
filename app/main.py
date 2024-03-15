import monteCarloAlgo
def main():
    # Number of random points to generate
    num_points = 50000000

    # Estimating pi
    pi_approximation = monteCarloAlgo.estimate_pi(num_points)
    print("Approximation of pi using Monte Carlo method:", pi_approximation)
    


if __name__ == "__main__":
    main()
    
    