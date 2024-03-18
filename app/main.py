import monteCarloAlgo
import logger
import logging

def main():
    logger.monteCarloLogger
    logging.info("Starting program")
    # Number of random points to generate
    num_points = 500

    # Estimating pi
    pi_approximation = monteCarloAlgo.estimate_pi(num_points)
    print("Approximation of pi using Monte Carlo method:", pi_approximation)
    


if __name__ == "__main__":
    main()
    
    