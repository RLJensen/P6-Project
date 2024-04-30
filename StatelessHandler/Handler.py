import os

class StatusInfo:
    def __init__(self, name, ready, status, restarts, age, labels):
        self.name = name
        self.ready = ready
        self.status = status
        self.restarts = restarts
        self.age = age
        self.labels = labels


def parseStatusFile(path):
    status_infos = []
    with open(path, 'r') as file:
        next(file)  # skip the header line
        for line in file:
            parts = line.split()
            name = parts[0]
            ready = parts[1]
            status = parts[2]
            restarts = int(parts[3])
            age = parts[4]
            labels = parts[5]
            status_info = StatusInfo(name, ready, status, restarts, age, labels)
            status_infos.append(status_info)
    return status_infos

def Handler():
    #path = "C:/Users/raser/Documents/GitHub/P6-Project/StatelessHandler/test.txt"
    #statusinfos = parseStatusFile(path)
    #for info in statusinfos:
    #    if info.status == "Terminated" :
    #        os.popen(f'kubectl delete Pod {info.name}')
    getPods()
    

def getPods():
    #path = "C:/Users/raser/Documents/GitHub/P6-Project/StatelessHandler/test.txt"
    #w = os.popen("kubectl get pods -n kube-system")
    #"NAME            READY   STATUS      RESTARTS    AGE     LABELS\nSomeName        1/1     Running     0           3m2s    app=somethingsomething\nSomeName1       1/1     Terminated  0           3m2s    app=somethingsomething"
    f = open("C:/Users/raser/Documents/GitHub/P6-Project/StatelessHandler/test.txt", "w")
    f.write("Woops! I have deleted the content!")
    f.close()

    print(f.read())

if __name__ == "__Handler__":
    Handler()