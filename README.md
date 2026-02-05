# sublog
> python subprocess  logger that capture all output from shell commands started by subprocess.call function

# usage

       import subprocess
       from sublog import SubprocessLogger

       print("Subprocess starting ")
    
       with SubprocessLogger():
            subprocess.call(["java", "-version"])
         
       print("Subprocess finished, capturing stopped.")

after executing above code we can see following as output, it willbe redirected to pythons builtin logger

    Subprocess starting
        2026-02-05 21:11:47,739 - DEBUG - SubprocessLogger enabled (patched subprocess.call).
        2026-02-05 21:11:47,829 - ERROR - java version "25" 2025-09-16 LTS
        2026-02-05 21:11:47,829 - ERROR - Java(TM) SE Runtime Environment (build 25+37-LTS-3491)
        2026-02-05 21:11:47,829 - ERROR - Java HotSpot(TM) 64-Bit Server VM (build 25+37-LTS-3491, mixed mode, sharing)
        2026-02-05 21:11:47,842 - DEBUG - SubprocessLogger disabled (restored subprocess.call).
    Subprocess finished, capture stopped.

# how 
> as you can see in usage example we should import two modules in to our python code  
> the sublog will dynamicaly hook subprocess.call function when used "with" statement   
> if some errors occured inside the with statement then the redirecting functions will gracefully ends
> 
> 
