import requests
import sys, os
import getopt
import threading, signal
import queue

targetDomain = ''       # Placeholder for the target domain
wordlistFile = ''       # Placeholder for the wordlist file
excludeReturn = ['404'] # HTTP Status Code to be ignored
numberOfThreads = 10    # Default number of concurrent threads
q = queue.Queue()       # The wordlist will be put on this queue
proto = ['http','https']

kitsun3 = '''
                &&                         &&               
              &&&&&&&                    &&&&&&             
            #&&&&&&&&                    &&&&&&&            
            &&&. .&&&&                  &&&. .&&&           
           &&&&   &&&&&               &&&&&   &&&&          
           &&&..  ,%&&&& %%%%%%%%%%% &&&&&,  ..&&&          
          &%%%..* *#%%%%*************%%%%%* *..%%%          
        %%%%%%.*******************************.%%%%%%       
        %,..**************************************..%       
         %*.***************************************%        
       %%.(#.*************,*******,*************.,(.%%      
       %..,,.*.****((****, ,*****, ,****/#****.*..,..%      
         %*...*****%&&*****************#&&*****...*%        
        %%%%%%..****(&&***************&&%****..%%%%%%       
         %*......******&*************&/*****......*%        
              %###..,********************,.###%             
                    %%.***************.(&                   
                       %.***********.%                      
                        %.*********.%                       
                          #.&&&&&.#                         
                            %%%%%                           
'''


# Help function
def show_help():
    print(kitsun3)
    print("\n\t\t\t-= Kitsun3Sec =-")
    print("\nPowerSub: Offline subdomain enumeration")
    print('\nUSAGE: python ' + sys.argv[0] + ' -t <targetdomain> -w <wordlist> [-x <status Code> -T <threads>]')
    print('\nOPTIONS')
    print('\t-t\tTarget domain to enumerate for its subdomains')
    print('\t-w\tWordlist - file with the list of names to test')
    print('\t-x\tAdd HTTP Status code to the ignore list. Default: 404')
    print('\t-T\tNumber of threads. Default: 10')
    print('\t-h\tThis help')
    sys.exit()

def domainExists():
    try:
        for p in range(len(proto)):
            r = requests.get(proto[p] + '://' + targetDomain, timeout=(1,3))
            if r.status_code == 200:
                return 1
    except:
        pass
    return 0

# Try to connect to HTTP port 80 and 443 in order to test for the existence of the subdomain
def testSub():
    global q
    while True:
        # Get one subdomain name from the queue to test 
        subdomain = q.get()
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
        q.task_done()

def goingForTheKill():
    global q

    # Test if the wordlist file exists
    if os.path.exists(wordlistFile):
        # Open the wordlist
        with open(wordlistFile,"r") as fd:
            # Read each line of the file
            for line in fd:
                # Remove spaces and newlines       
                line = line.replace("\r","").replace("\n","").replace(" ","")
                # Add the line to the queue
                q.put(line)
    # If the file doesn't exist
    else:
        # Print this message to the user
        print("Wordlist doesn't exist.")
        # And exit the tool
        sys.exit()

    try:
        # Loop until create N threads (default: 10 threads)
        for i in range(numberOfThreads):
            # Define the thread as a daemon
            t = threading.Thread(target=testSub, daemon=True)
            # Start the thread
            t.start()

        # While there is names on the queue waiting to be testes
        while not q.empty():
            # Print on the screen how many names are left to be testes
            print(str(q.qsize()) + " attempts left.", end="\r")

    # On error
    except :
        # Print this message
        print("Error when creating the threads.")
        # Exit
        sys.exit()

# If this function is called
def signal_handler(signal, frame):
    # Exit the tool
    sys.exit()

def main(argv):
    global targetDomain, wordlistFile, excludeReturn, numberOfThreads
    # If CTRL + C call signal_handler function
    signal.signal(signal.SIGINT, signal_handler)

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
        if opt == '-T':
            numberOfThreads = int(arg)
        if opt == '-w':
            wordlistFile = arg
        if opt == '-x':
            for i in arg.split(","):
                excludeReturn.append(i)

    # Target domain and Wordlist are mandatory
    if not targetDomain or not wordlistFile:
        show_help()

    if domainExists():
        goingForTheKill()
    else:
        print("I was not able to reach the domain. Does it really exist?")
        sys.exit()

if __name__ == '__main__':
    # If the tool was called without parameters
    if len(sys.argv) < 2:
        # Print the usage
        show_help()
    
    # Let's start the process
    main(sys.argv[1:])
        
