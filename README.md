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
# Powersub
A tool to enumerate subdomains offline (do not make use of google, bing or any other online resource). This tool depends basically on a word list. Also, it implements threads to speedy the tasks. The tools tries HTTP and HTTPS connection for each subdomain.

## Basic Usage
python.exe .\powersub.py -t targetdomain.com -w D:\wordlists\subdomains-top1million-110000.txt -x 403,500

## OPTIONS
        -t      Target domain to enumerate for its subdomains
        -w      Wordlist - file with the list of names to test
        -x      Add HTTP Status code to the ignore list. Default: 404
        -T      Number of threads. Default: 10
        -h      This help

