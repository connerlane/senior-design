import os, pytest, datetime
from os.path import join

def main():
    #Get current date and time
    now = datetime.datetime.now()
    
    #Make sure there are folders, if not make them
    path_dict = {"input_path":"input", "log_path":"logs"}
    for key in path_dict:
        os.makedirs(path_dict[key], exist_ok=True)
    
    #create the log file   
    log_file = initializeLog(path_dict["log_path"], now)
    
    #run pytest, outputting session to pytest_session.txt
    pytest.main([path_dict["input_path"]], plugins = ['pytest_session2file'])
    
    #import session into log file
    session_file = open("pytest_session.txt", "r")
    for line in session_file:
        log_file.write(line)
    session_file.close()
    
    #Close log file
    now = datetime.datetime.now()
    log_file.write("Log File Closed " + now.strftime("%H:%M:%S"))
    log_file.close()
    
#Takes the log path and a datetime object
#Returns an open file
def initializeLog(log_path, time):
    #Create the log file
    log_name = "LOG_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    path_to_log = join(log_path, log_name)
    log_file = open(path_to_log, "w")
    
    #Begin writing to log file
    log_file.write("Log file opened " + time.strftime("%H:%M:%S") + "\n")
    
    return log_file
    
if __name__== "__main__":
  main()