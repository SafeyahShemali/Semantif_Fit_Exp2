import os
import json
import csv
import re



def read_data(filename: str):

    # List that hold the records
    data = []

    # Opening the CSV file
    with open(filename, mode ='r')as file:
    
        # reading the CSV file
        csvFile = csv.reader(file)
        
        # displaying the contents of the CSV file
        for lines in csvFile:
            data.append(lines)
            
    return data

def record_exist(result_file_name: str, predicate: str, argument: str, argument_type: str):
    
    # for ferretti Instrument and Location
    if 'ferretti' in result_file_name:
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate in line and argument in line:
                    return True
        return False
    
    else:
    # for Pado and Mrecrae 
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate in line and argument in line and argument_type in line:
                    return True
        return False

def open_result_file(filename: str, fields: []):
    with open(filename, 'a') as csvfile: 
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile) 

        # writing the fields  
        csvwriter.writerow(fields)

def is_file_exits(filename: str):
    return os.path.exists(filename)

def save_result(filename: str, result: []):
    with open(filename, 'a') as csvfile: 
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile) 
    
        # writing the data rows  
        csvwriter.writerow(result) 
        
def processing_json(responce: str,filename_error: str, predicate: str, argument: str, roleType: str):
    
    try:
        data = json.loads(responce)
        return data
    except json.JSONDecodeError as e:
        print("Invalid JSON syntax:", e)
        save_result(filename_error, [predicate,argument,responce])

        extract_json = json_from_s(responce)
        
        if extract_json:
            return extract_json
        
        if 'Expecting property name enclosed in double quotes' in e.msg :
            return json.loads(responce.replace("\'", "\"")) 
        
        else:
            return None
        
    
def get_back_exp_result(result_file_name: str, predicate: str, argument: str, argument_type: str):
    
    # for ferretti Instrument and Location
    if 'ferretti' in result_file_name:
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate in line and argument in line:
                    return line
        return None
    
    else:
    # for Pado and Mrecrae 
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate in line and argument in line and argument_type in line:
                    return line
        return None
    
def json_from_s(s):
    match = re.findall(r"{.+[:,].+}|\[.+[,:].+\]", s)
    return json.loads(match[0]) if match else None