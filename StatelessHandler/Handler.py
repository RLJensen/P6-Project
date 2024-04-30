import os
import subprocess
def Handler():
    
    try:
        #cmd = subprocess.Popen('cmd "date"')
        #print(cmd)
        message = os.system('cmd "date"')
        print(message)
    except:
        print('could not execute command')
    

if __name__ == "__main__":
    Handler()