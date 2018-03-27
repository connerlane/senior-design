#!/usr/bin/python

import os, json, datetime
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
    
    #Load all tests in input directory into a single dictionary
    test_dict = importTests(path_dict["input_path"], log_file)
    
    #run each test and output results to log file
    log_file.write("---Begin Tests---\n")
    log_file.write("--------------------\n")
    for test in test_dict:
        #run the test and record the result
        runTest(test, test_dict[test]["testCondition"], test_dict[test]["expectedResult"], log_file)
    
    log_file.write("---Testing Complete---\n")
    
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

#Takes the input path and open log file
#Returns a dictionary with all tests imported from valid files
def importTests(input_path, log_file):

    #Write all files found i input folder to log
    dirs = os.listdir(input_path)
    log_file.write("Test files: " + str(dirs) + "\n")
    
    #Try to open and input all test's in the input folder to a list
    #If any fail to input (most likely because they are not properly
    # json formatted) note in log and continue
    log_file.write("---Begin Test Import---\n")
    test_dict = {}
    for file in dirs:
        path_to_input = join(input_path, file)
        input = open(path_to_input, "r")
        input_text = input.read()
        
        try:
            json_dict = json.loads(input_text)
            load_txt =  ":LOADED"
            test_dict.update(json_dict)
        except Exception as e:
            load_txt =  ":ERROR - " + str(e)
        
        log_file.write("[" + file + "]" + load_txt + "\n")
        
        input.close()
    log_file.write("---End Test Import---\n")
    
    return test_dict

#Takes an open log file, test name, condition, and expected result
#Runs the test, then outputs to the log the results
def runTest(test_name, condition, result, log_file):

    output = dummyTest(condition)
    if result == str(output):
        result_txt = "Passed"
    else:
        result_txt = "Failed"
        
    log_file.write(test_name + ":" + result_txt + "\n")
    log_file.write("Conditions:" + condition + "\n")
    log_file.write("Expected Results:" + result + "\n")
    log_file.write("Actual Results:" + str(output) + "\n")
    log_file.write("--------------------\n")
    
    return None;

def dummyTest(condition):
    return condition
    
if __name__== "__main__":
  main()
