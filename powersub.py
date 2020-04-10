import requests
import sys, os
import getopt
import threading
import queue

targetDomain = ''       # Placeholder for the target domain
wordlistFile = ''       # Placeholder for the wordlist file
excludeReturn = ['404'] # HTTP Status Code to be ignored
numberOfThreads = 10    # Default number of concurrent threads
q = queue.Queue()       # The wordlist will be put on this queue

# Help function
def show_help():
    print("Help here...")
    sys.exit()

# Try to connect to HTTP port 80 and 443 in order to test for the existence of the subdomain
def testSub(subdomain):
    proto = ['http','https']
    try:
        # Loop the range of protocols (HTTP and HTTPS)
        for p in range(len(proto)):
            # Try to connect to the subdomain on each of the default ports for HTTP and HTTPS
            r = requests.get(proto[p] + '://' + subdomain + '.' + targetDomain, timeout=(1,3))
            # If the HTTP status code of the answer is not in the exclude list, we print the subdomain on the screen
            if str(r.status_code) not in excludeReturn:
                print(str(r.status_code) + " =>\t" + proto[p] + '://' + subdomain + '.' + targetDomain)
    except :
        pass

def goingForTheKill():
    global q
    threads = []

    if os.path.exists(wordlistFile):
        with open(wordlistFile,"r") as fd:
            for line in fd:                    
                line = line.replace("\r","").replace("\n","").replace(" ","")
                q.put(line)
    else:
        print("Wordlist doesn't exist.")
    while q.qsize() > 0:
        for instance in range(numberOfThreads):
            if q.qsize() >= 1:
                thread = threading.Thread(target = testSub, args = (q.get(),))
                threads.append(thread)
                thread.start()
                print(str(q.qsize()) + " attempts left.", end="\r")
        for t in threads:
            t.join()
    
def main(argv):
    global targetDomain, wordlistFile, excludeReturn

    # t = target; w = wordlist; h = help; T = Threads; x = exclude
    try:
        opts, args  = getopt.getopt(argv, "t:w:hT:x:")
    except getopt.GetoptError:
        show_help()

    # Parsing parameters
    for opt, arg in opts:
        if opt == '-h':
            show_help()
        if opt == '-t':
            targetDomain = arg
        if opt == '-w':
            wordlistFile = arg
        if opt == '-x':
            for i in arg.split(","):
                excludeReturn.append(i)

    if not targetDomain or not wordlistFile:
        show_help()

    goingForTheKill()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
    
    main(sys.argv[1:])
        
