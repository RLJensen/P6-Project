import monteCarloAlgo
import logging

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting program")
    # Number of random points to generate
    num_points = 500

    # Estimating pi
    pi_approximation = monteCarloAlgo.estimate_pi(num_points)
    print("Approximation of pi using Monte Carlo method:", pi_approximation[0])
    for i in pi_approximation[1]:
        logging.info(pi_approximation[1][i])
        
    


if __name__ == "__main__":
    main()
    
    