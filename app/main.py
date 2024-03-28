import monteCarlo.monteCarloAlgo as monteCarloAlgo
import logging
import whisperWorkload.whisperWorkload as whisperWorkload

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting program")
    
     # Number of random points to generate
    num_points = 1

    # Estimating pi
    pi_approximation = monteCarloAlgo.estimate_pi(num_points)
    print("Approximation of pi using Monte Carlo method:", pi_approximation[0])
    logObjcets = pi_approximation[1]
    for obj in logObjcets:
        logging.info(obj)

    whisper = whisperWorkload.loadModel()
    whisperResult = whisper[0]
    whisperLoad = whisper[1]
    whisperSearchResult = whisper[2]
    logging.info("Now starting Whisper workload")
    for key, value in whisperResult.items():
        print(key, ":", value)
    
    for info in whisperLoad:
        logging.info(info)

    for info in whisperSearchResult:
        logging.info(info)

if __name__ == "__main__":
    main()
    
    