# sublog
> python subprocess  logger that capture all output from shell commands started by subprocess.call function

# usage

       import subprocess
       from sublog import SubprocessLogger

       print("Subprocess starting .")
    
       with SubprocessLogger():
            subprocess.call(["java", "-version"])
         
       print("Subprocess finished, capturing stopped.")
       
# how 
> as you can see in usage example we should import two modules in to our python code  
> the sublog will dynamicaly hook subprocess.call function when used "with" statement  
> 
> 
