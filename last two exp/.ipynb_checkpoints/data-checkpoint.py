import os
import json
import csv
import re
import pandas as pd
import prompt_bank

def read_data(filename: str):
    data = []
    with open(filename, mode ='r')as file:
        csvFile = csv.reader(file)  
        for lines in csvFile:
            data.append(lines)
    return data

def read_data_pado(filename: str):
    data = []
    with open(filename, mode ='r')as file:
        txtFile = file.readlines()
        txtFile = remove_items(txtFile,'\t\n')
        for i in txtFile:
            line = i.split("\t")
            data.append(line)
            
        return data

def read_data_mcrae(filename: str):
    data = []
    with open(filename, mode ='r')as file:
        txtFile = file.readlines()
        txtFile = remove_items(txtFile, '\n')
        for i in txtFile:
            line = i.split(" ")
            data.append(line)
            
        return data

def is_file_exits(filename: str):
    return os.path.exists(filename)

def open_result_file(filename: str, fields: []):
    with open(filename, 'a') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields)

def record_exist(result_file_name: str, predicate: str, argument: str, roleType: str):
    
    # for ferretti Instrument and Location
    if 'ferretti' in result_file_name:
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate == line[0] and argument == line[1]:
                        return True
        return False
    
    else:
        # for Pado and Mcrae 
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate == line[0] and argument == line[1] and roleType == line[2]:
                    return True
        return False
    
def record_exist_other(result_file_name: str, predicate: str, argument: str, roleType: str):
    
    # Get the Result
    result = read_data(result_file_name)
    result.pop(0)

    for i in range(len(result)):
        p = result[i][0]
        a = result[i][1]
        t = result[i][2]
        
        if p == predicate and a == argument and t == roleType:
            return True
        
    return False

def save_result(filename: str, result: []):
    with open(filename, 'a') as csvfile: 
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile) 
    
        # writing the data rows  
        csvwriter.writerow(result) 

# def save_reasons(filename: str, result: []):
#     df = pd.DataFrame(result)
#     df.to_csv("list_of_dict_to_csv.csv")

def processing_json(responce: str, json_key: str ,filename_error: str, predicate: str, argument: str, roleType: str):
    
    try:
        data = json.loads(responce)
        return data[json_key]
    
    except json.JSONDecodeError as e:
        print("Invalid JSON syntax:", e.msg)
        save_result(filename_error, [predicate,argument,responce])

        if 'Expecting property name enclosed in double quotes' in e.msg : 
            dic = eval(responce)
            dic_value = dic[json_key]
            return dic_value
        
        if 'Expecting value' in e.msg:
            print('just responcse: ', responce)
            fixed = responce.split(',\n]\n}')[0]
            fixed = fixed + '\n]\n}'
            print('ggggg',fixed)
            data = json.loads(fixed)
            return data[json_key]
        else:
            exit()
        
    
def get_back_exp_result(result_file_name: str, predicate: str, argument: str, argument_type: str):
    
    if not is_file_exits(result_file_name):
        print('not exist file ', result_file_name)
        return
    
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

def remove_items(test_list, item): 
    # remove the item for all its occurrences 
    c = test_list.count(item) 
    for i in range(c): 
        test_list.remove(item) 
    return test_list 

def retrive_reasons(result_file_name: str,predicate: str, argument: str, roleType: str):
     
    reasons_conversation = []
    json_key = 'Response'
    reasons_prompts = prompt_bank.get_prompt('reasoning_lemma_tuple', predicate, argument, roleType, json_key)
    
    if not is_file_exits(result_file_name):
        print('not exist file')
        return None
    
    # for ferretti Instrument and Location
    if 'ferretti' in result_file_name:
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate in line and argument in line:
                    for i in range(3):
                        reasons_conversation.append({"role": "user", "content": f"{reasons_prompts[i]}"})
                        reasons_conversation.append({"role": "assistant", "content": f"{line[3+i]}"})

            return reasons_conversation
        return None
    
    else:
    # for Pado and Mrecrae 
        with open(result_file_name, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if predicate in line and argument in line and roleType in line:
                     for i in range(3):
                        reasons_conversation.append({"role": "user", "content": f"{reasons_prompts[i]}"})
                        reasons_conversation.append({"role": "assistant", "content": f"{line[3+i]}"})

            print(reasons_conversation)                
            return reasons_conversation
        
        return None
    
# def check_result(result_file_name: str, predicate: str, argument: str, roleType: str):
      
#     # for ferretti Instrument and Location
#     if 'ferretti' in result_file_name:
#         with open(result_file_name, mode ='r')as file:
#             csvFile = csv.reader(file)
#             for line in csvFile:
#                 if not (predicate in line[0] and argument in line[1]):
#                         return False
#         return True
    
#     else:
#     # for Pado and Mcrae 
#         with open(result_file_name, mode ='r')as file:
#             csvFile = csv.reader(file)
#             for line in csvFile:
#                 if not (predicate in line[0] and argument in line[1] and roleType in line[2]):
#                     return False
#         return True
    
def result_checking (dataset_file_name, result_file_name):
    
    if 'ferretti' in dataset_file_name:
        # Get the data
        dataset = read_data(dataset_file_name)
       
        for i in range (len(dataset)):
            '''Data Extraction'''
            predicate = dataset[i][0]
            argument = dataset[i][1]

            isExit = record_exist(result_file_name, predicate, argument, '')
            
            if not isExit:
                print(f"{predicate} , {argument} does not exist at {i}")
        
        result = read_data(result_file_name)

        if len(dataset)+1 != len(result):
            return False
            
    else:
        if 'pado' in dataset_file_name:
            # Get the data
            dataset = read_data_pado(dataset_file_name)
            print(len(dataset))

        if 'mcrae' in dataset_file_name:
            # Get the data
            dataset = read_data_mcrae(dataset_file_name)
            print(len(dataset))
            
        for i in range (len(dataset)):
            '''Data Extraction'''
            predicate = dataset[i][0]
            argument = dataset[i][1]
            roleType = dataset[i][2]

            isExit = record_exist(result_file_name, predicate, argument, roleType)
            print(predicate,argument,roleType,isExit)
            if not isExit:
                print(f"{predicate} , {argument} , {roleType} does not exist at {i}")

        result = read_data(result_file_name)

        if len(dataset)+1 != len(result):
            return False

def fix_json(jsonStr):
    
    # Remove all empty spaces to make things easier bellow
    jsonStr = jsonStr.replace('" :','":').replace(': "',':"').replace('"\n','"').replace('" ,','",').replace(', "',',"')
    
    # First remove the " from where it is supposed to be.
    jsonStr = re.sub(r'\\"', '"', jsonStr)
    jsonStr = re.sub(r'{"', '{`', jsonStr)
    jsonStr = re.sub(r'"}', '`}', jsonStr)
    jsonStr = re.sub(r'":"', '`:`', jsonStr)
    jsonStr = re.sub(r'":\[', '`:[', jsonStr)
    jsonStr = re.sub(r'":\{', '`:{', jsonStr)
    jsonStr = re.sub(r'":([0-9]+)', '`:\\1', jsonStr)
    jsonStr = re.sub(r'":([null|true|false])', '`:\\1', jsonStr)
    jsonStr = re.sub(r'","', '`,`', jsonStr)
    jsonStr = re.sub(r'",\[', '`,[', jsonStr)
    jsonStr = re.sub(r'",\{', '`,{', jsonStr)
    jsonStr = re.sub(r',"', ',`', jsonStr)
    jsonStr = re.sub(r'\["', '[`', jsonStr)
    jsonStr = re.sub(r'"\]', '`]', jsonStr)
    
    # Backslash all double quotes (")
    jsonStr = re.sub(r'"','\\"', jsonStr)
    
    # Put back all the " where it is supposed to be.
    jsonStr = re.sub(r'\`','\"', jsonStr)
    return jsonStr


        
        
            
    
    