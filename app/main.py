import monteCarloAlgo
import logging
import EncryptionWorkload

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting program")
    
    # # Number of random points to generate
    # num_points = 1

    # # Estimating pi
    # pi_approximation = monteCarloAlgo.estimate_pi(num_points)
    # print("Approximation of pi using Monte Carlo method:", pi_approximation[0])
    # logObjcets = pi_approximation[1]
    # for obj in logObjcets:
    #     logging.info(obj)

    EncryptionWorkload.primefiller()
    EncryptionWorkload.setkeys()
    print("Public key: ", EncryptionWorkload.public_key)
    print("Private key: ", EncryptionWorkload.private_key)
    message = "Hello World!"
	# Uncomment below for manual input
	# message = input("Enter the message\n")
	# Calling the encoding function
    coded = EncryptionWorkload.encoder(message)

    print("Initial message:")
    print(message)
    print("\n\nThe encoded message(encrypted by public key)\n")
    print(''.join(str(p) for p in coded))
    print("\n\nThe decoded message(decrypted by public key)\n")
    print(''.join(str(p) for p in EncryptionWorkload.decoder(coded)))



if __name__ == "__main__":
    main()
    
    