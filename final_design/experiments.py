import data
from models import Model
import fit_scoring
import prompt_bank
import json

'''Simple Lemma Tuple'''
def exp_simple_lemma_tuple_ferretti(filename: str, role_type: str, model: Model, model_name: str):
    
    exp_name = 'lemma_tuple'
    
    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(100)       

    # Get the data
    dataset = data.read_data(filename)
    
    # Create files for the results if not exits 
    fields = ['predicate', 'argument', 'actual_fit', 'exp_fit']
    dataset_name = filename.split('.csv')[0]
    model_name_only = model_name.split('/')[1]
    result_filename1 = f'Result/{exp_name}_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_categorical_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
   
    for i in range(len(dataset)): 

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = role_type
        actual_fit = dataset[i][2]
        model.reset_conversation()

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , '')
        IsExist2 = data.record_exist(result_filename2, predicate, argument , '')

        if 'paint' in predicate and 'paint' in argument:
            print(predicate,argument ,IsExist1, IsExist2)
            
        if IsExist1:
            if IsExist2:
                continue
        else:
            print(predicate, argument)

        '''Result Preparation'''  
        result1 = [predicate, argument, actual_fit]
        result2 = [predicate, argument, actual_fit]

        '''Prompting Part For Categorical Result '''
        fit_score_categorical= fit_scoring.simple_lemma_tuple(model, predicate, argument, roleType, 'categorical')

        # Add the fit score to the result list
        result2.append(fit_score_categorical)

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        '''Prompting Part For Numerical Result '''
        fit_score_numerical= fit_scoring.simple_lemma_tuple(model, predicate, argument, roleType, 'numerical')

        # Add the fit score to the result list
        result1.append(fit_score_numerical)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)

# The difference than the previous one:
# - no need to specify the roletype as it is included in the dataset (ARG0, ARG1, ARG2)
# - reading the data is diffrernt due to the dataset formating 
# - result fields are different
def exp_simple_lemma_tuple_other(filename: str, model: Model, model_name: str):
    
    exp_name = 'lemma_tuple'
    
    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(100)       

    # Get the data
    if 'pado' in filename:
        dataset = data.read_data_pado(filename)
    elif 'mcrae' in filename:
        dataset = data.read_data_mcrae(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument', 'role_type' , 'actual_fit', 'exp_fit']
    dataset_name = filename.split('.txt')[0]
    model_name_only = model_name.split('/')[1]
    result_filename1 = f'Result/{exp_name}_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_categorical_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
   
    for i in range(len(dataset)): 

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = dataset[i][2]
        actual_fit = dataset[i][3]  
        model.reset_conversation()

        '''TRACING'''
        print('New Record : ', predicate, argument)
        print('New COnversation : ', model.conversation , '\n')


        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument, roleType)
        IsExist2 = data.record_exist(result_filename2, predicate, argument, roleType)

        if IsExist1 and IsExist2:
            if 'mcrae' in filename:
                if (predicate != 'teach' and argument != 'instructor') or (predicate != 'execute' and argument != 'martyr'):
                    continue
            else:
                continue
               

        '''Result Preparation'''  
        result1 = [predicate, argument, roleType, actual_fit]
        result2 = [predicate, argument, roleType, actual_fit]

        '''Prompting Part For Categorical Result '''
        fit_score_categorical= fit_scoring.simple_lemma_tuple(model, predicate, argument, roleType, 'categorical')

        # Add the fit score to the result list
        result2.append(fit_score_categorical)

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        '''Prompting Part For Numerical Result '''
        fit_score_numerical= fit_scoring.simple_lemma_tuple(model, predicate, argument, roleType, 'numerical')

        # Add the fit score to the result list
        result1.append(fit_score_numerical)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)

'''Reasoning Lemma Tuple'''
def exp_reasoning_lemma_tuple_ferretti(filename: str, role_type: str, model: Model, model_name: str):
    
    exp_name = 'lemma_tuple'
    
    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(600)       

    # Get the data
    dataset = data.read_data(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','actual_fit', 'exp_fit']
    dataset_name = filename.split('.csv')[0]
    model_name_only = model_name.split('/')[1]
    result_filename1 = f'Result/{exp_name}_reasoning_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}__reasoning_categorical_{dataset_name}_{model_name_only}.csv'
    reason_filename = f'Result/reasons_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
    if not data.is_file_exits(reason_filename):
        data.open_result_file(filename= reason_filename, fields= ['predicate', 'argument', 'role_type', 'reasons 1', 'reasons 2','reasons 3'])
   
    for i in range(6): #len(dataset)

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = role_type
        actual_fit = dataset[i][2]
        model.reset_conversation()

        '''TRACING'''
        print('New Record : ', predicate, argument)
        print('New COnversation : ', model.conversation , '\n')


        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , '')
        IsExist2 = data.record_exist(result_filename2, predicate, argument , '')

        if IsExist1 and IsExist2:
            continue
        
        '''Result Preparation'''  
        result1 = [predicate, argument, actual_fit]
        result2 = [predicate, argument, actual_fit]

        '''Reasoning'''
        fit_scoring.reasoning(model,predicate, argument, roleType, reason_filename)
        
        '''TRACKING'''
        print('Conversation Before the fit scoring: \n', model.conversation)
        
        '''Prompting Part For Categorical Result '''
        fit_score_categorical= fit_scoring.simple_lemma_tuple(model, predicate, argument, roleType, 'categorical')

        # Add the fit score to the result list
        result2.append(fit_score_categorical)

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        '''Prompting Part For Numerical Result '''
        fit_score_numerical= fit_scoring.simple_lemma_tuple(model, predicate, argument, roleType, 'numerical')

        # Add the fit score to the result list
        result1.append(fit_score_numerical)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)

# The difference than the previous one:
# - no need to specify the roletype as it is included in the dataset (ARG0, ARG1, ARG2)
# - reading the data is diffrernt due to the dataset formating 
# - result fields are different
def exp_reasoning_lemma_tuple_other(filename: str, model: Model, model_name: str):
    
    exp_name = 'lemma_tuple'
    
    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(600)       

    # Get the data
    if 'pado' in filename:
        dataset = data.read_data_pado(filename)
    elif 'mcrae' in filename:
        dataset = data.read_data_mcrae(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','role_type','actual_fit', 'exp_fit']
    dataset_name = filename.split('.txt')[0]
    model_name_only = model_name.split('/')[1]
    result_filename1 = f'Result/{exp_name}_reasoning_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}__reasoning_categorical_{dataset_name}_{model_name_only}.csv'
    reason_filename = f'Result/reasons_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
    if not data.is_file_exits(reason_filename):
        data.open_result_file(filename= reason_filename, fields= ['predicate', 'argument', 'role_type', 'reasons 1', 'reasons 2','reasons 3'])   
   
    for i in range(5): #len(dataset)

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = dataset[i][2]
        actual_fit = dataset[i][3]  
        model.reset_conversation()

        '''TRACING'''
        print('New Record : ', predicate, argument)
        print('New COnversation : ', model.conversation , '\n')


        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , roleType)
        IsExist2 = data.record_exist(result_filename2, predicate, argument , roleType)

        if IsExist1 and IsExist2:
            continue
        
        '''Result Preparation'''  
        result1 = [predicate, argument, roleType]
        result2 = [predicate, argument, roleType]

        '''Reasoning'''
        fit_scoring.reasoning(model,predicate, argument, roleType, reason_filename)
        
        '''TRACKING'''
        print('Conversation Before the fit scoring: \n', model.conversation)
        
        '''Prompting Part For Categorical Result '''
        fit_score_categorical= fit_scoring.simple_lemma_tuple(model, predicate, argument, roleType, 'categorical')

        # Add the fit score to the result list
        result2.append(fit_score_categorical)

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        '''Prompting Part For Numerical Result '''
        fit_score_numerical= fit_scoring.simple_lemma_tuple(model, predicate, argument, roleType, 'numerical')

        # Add the fit score to the result list
        result1.append(fit_score_numerical)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)

'''Simple Generated Sentences'''
def exp_simple_gen_sentences_ferretti(filename: str, role_type: str, model: Model, model_name: str):
    
    exp_name = 'gen_sentences'
    
    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(300)       

    # Get the data
    dataset = data.read_data(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','sentence 1','sub-fit score 1','sentence 2','sub-fit score 2','sentence 3','sub-fit score 3','sentence 4','sub-fit score 4', 'sentence 5','sub-fit score 5','actual_fit', 'exp_fit']
    dataset_name = filename.split('.csv')[0]
    model_name_only = model_name.split('/')[1]
    result_filename1 = f'Result/{exp_name}_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_categorical_{dataset_name}_{model_name_only}.csv'
    sentence_filename = f'Result/gen_sentences_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= sentence_filename, fields= ['predicate','argument','sentence 1','sentence 2','sentence 3','sentence 4','sentence 5'])
    
    for i in range(len(dataset)): #

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = role_type
        actual_fit = dataset[i][2]
        model.reset_conversation()

        '''TRACING'''
        print('New Record : ', predicate, argument)
        print('New COnversation : ', model.conversation , '\n')

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , '')
        IsExist2 = data.record_exist(result_filename2, predicate, argument , '')

        if IsExist1 and IsExist2:
            continue
        
        '''Result Preparation'''  
        result1 = [predicate, argument]
        result2 = [predicate, argument]
        result3 = [predicate, argument]
        
        '''Generating Sentences Part'''
        sentences = fit_scoring.generate_sentence(model, predicate, argument, roleType)
        
        '''TRACING'''
        print('The sentences are: ', sentences)

        avg1 = 0
        avg2 = 0
        sentence_no = 5

        for sentence in sentences:
            
            '''Storing Sentences'''
            result3.append(sentence)
            
            '''Checking Semantic Coherent'''
            is_semantic = fit_scoring.semantic_coherent(model, predicate, argument, roleType, sentence) 

            '''TRACING'''
            print('is_semantic: ', model.conversation)

            '''Sematically Fit Sentence'''
            if is_semantic:  
                result1.append(sentence)
                result2.append(sentence)

                '''Prompting Part For Categorical Result '''
                fit_score_categorical= fit_scoring.simple_gen_sentences(model, predicate, argument, roleType, 'categorical', sentence)

                '''TRACING'''
                print('categorical_with_senetence: ', fit_score_categorical)
                
                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical

                '''Prompting Part For Numerical Result '''
                fit_score_numerical= fit_scoring.simple_gen_sentences(model, predicate, argument, roleType, 'numerical', sentence)

                '''TRACING'''
                print('numerical_with_senetence: ',fit_score_numerical)

                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            else:
                '''Back off'''
                result1.append('')
                result2.append('')
                
                '''Retrieve the data from previous exp'''
                print(f'Result/lemma_tuple_categorical_{dataset_name}_{model_name_only}.csv')
                fit_score_categorical = data.get_back_exp_result( f'Result/lemma_tuple_categorical_{dataset_name}_{model_name_only}.csv', predicate, argument, '')
                
                '''TRACING'''
                print('categorical from prevL ', fit_score_categorical)
                
                fit_score_categorical = float(fit_score_categorical[-1])
                
                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical

                
                fit_score_numerical = data.get_back_exp_result(f"Result/lemma_tuple_numerical_{dataset_name}_{model_name_only}.csv", predicate, argument, '')
                
                print('Numerical from prev: ', fit_score_numerical)
                fit_score_numerical = float(fit_score_numerical[-1])
                
                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            # Pop out the assistance prompt of sematic fit 
            model.conversation.pop()

             # Pop out the user prompt of sematic fit
            model.conversation.pop()

            '''TRACING'''
            print('After Poping the semantic: \n', model.conversation)

        '''Add the results'''
        result2.append(actual_fit)
        result2.append(round(avg2/sentence_no,2))

        result1.append(actual_fit)
        result1.append(round(avg1/sentence_no,2))

        '''TRACING'''
        print('result1: ',result1)
        print('result2: ',result2)
        print('---------------------DONE----------------------')

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)
        
        # Save the sentences
        data.save_result(sentence_filename, result3)

def exp_simple_gen_sentences_other(filename: str, model: Model, model_name: str):
    
    exp_name = 'gen_sentences'
    
    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(300)       

    # Get the data
    if 'pado' in filename:
        dataset = data.read_data_pado(filename)
    elif 'mcrae' in filename:
        dataset = data.read_data_mcrae(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','role_type','sentence 1','sub-fit score 1','sentence 2','sub-fit score 2','sentence 3','sub-fit score 3','sentence 4','sub-fit score 4', 'sentence 5','sub-fit score 5','actual_fit', 'exp_fit']
    dataset_name = filename.split('.txt')[0]
    model_name_only = model_name.split('/')[1]
    result_filename1 = f'Result/{exp_name}_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_categorical_{dataset_name}_{model_name_only}.csv'
    sentence_filename = f'Result/gen_sentences_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
    if not data.is_file_exits(result_filename2):    
        data.open_result_file(filename= sentence_filename, fields= ['predicate', 'argument',['predicate','argument','sentence 1','sentence 2','sentence 3','sentence 4','sentence 5']])
    
    for i in range(5): #len(dataset)

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = dataset[i][2]
        actual_fit = dataset[i][3]  
        model.reset_conversation()

        '''TRACING'''
        print('New Record : ', predicate, argument)
        print('New COnversation : ', model.conversation , '\n')


        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , roleType)
        IsExist2 = data.record_exist(result_filename2, predicate, argument , roleType)

        if IsExist1 and IsExist2:
            continue
        
        '''Result Preparation'''  
        result1 = [predicate, argument, roleType]
        result2 = [predicate, argument, roleType]
        result3 = [predicate, argument, roleType]

        '''Generating Sentences Part'''
        sentences = fit_scoring.generate_sentence(model, predicate, argument, roleType)
        
        '''TRACING'''
        print('The sentences are: ', sentences)

        # Save the sentences
        data.save_result(sentence_filename, [predicate, argument, sentences])


        avg1 = 0
        avg2 = 0
        sentence_no = 5

        for sentence in sentences:
            
            '''Storing Sentences'''
            result3.append(sentence)

            '''Checking Semantic Coherent'''
            is_semantic = fit_scoring.semantic_coherent(model, predicate, argument, roleType, sentence) 

            '''TRACING'''
            print('is_semantic: ', model.conversation)

            '''Sematically Fit Sentence'''
            if is_semantic:  
                result1.append(sentence)
                result2.append(sentence)

                '''Prompting Part For Categorical Result '''
                fit_score_categorical= fit_scoring.simple_gen_sentences(model, predicate, argument, roleType, 'categorical', sentence)

                '''TRACING'''
                print('categorical_with_senetence: ', fit_score_categorical)
                
                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical

                '''Prompting Part For Numerical Result '''
                fit_score_numerical= fit_scoring.simple_gen_sentences(model, predicate, argument, roleType, 'numerical', sentence)

                '''TRACING'''
                print('numerical_with_senetence: ',fit_score_numerical)

                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            else:
                '''Back off'''
                result1.append('')
                result2.append('')
                
                '''Retrieve the data from previous exp'''
                fit_score_categorical = data.get_back_exp_result( f'Result/lemma_tuple_categorical_{dataset_name}_{model_name_only}.csv', predicate, argument, '')
                
                '''TRACING'''
                print('categorical from prevL ', fit_score_categorical)
                
                fit_score_categorical = float(fit_score_categorical[-1])
                
                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical

                
                fit_score_numerical = data.get_back_exp_result(f"Result/lemma_tuple_numerical_{dataset_name}_{model_name_only}.csv", predicate, argument, '')
                
                print('Numerical from prev: ', fit_score_numerical)
                fit_score_numerical = float(fit_score_numerical[-1])
                
                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            # Pop out the assistance prompt of sematic fit 
            model.conversation.pop()

             # Pop out the user prompt of sematic fit
            model.conversation.pop()

            '''TRACING'''
            print('After Poping the semantic: \n', model.conversation)

        '''Add the results'''
        result2.append(actual_fit)
        result2.append(round(avg2/sentence_no,2))

        result1.append(actual_fit)
        result1.append(round(avg1/sentence_no,2))

        '''TRACING'''
        print('result1: ',result1)
        print('result2: ',result2)
        print('---------------------DONE----------------------')

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)
        
        # Save the sentences
        data.save_result(sentence_filename, result3)

'''Reasoning Generated Sentences'''
def exp_reasoning_gen_sentences_ferretti(filename: str, role_type: str, model: Model, model_name: str):
    
    exp_name = 'gen_sentences'
    
    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(300)       

    # Get the data
    dataset = data.read_data(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','role_type','sentence 1','sub-fit score 1','sentence 2','sub-fit score 2','sentence 3','sub-fit score 3','sentence 4','sub-fit score 4', 'sentence 5','sub-fit score 5','actual_fit', 'exp_fit']
    dataset_name = filename.split('.csv')[0]
    model_name_only = model_name.split('/')[1]
    result_filename1 = f'Result/{exp_name}_reasoning_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_reasoning_categorical_{dataset_name}_{model_name_only}.csv'
    reason_filename = f'Result/reasons_{dataset_name}_{model_name_only}.csv'
    sentence_filename = f'Result/gen_sentences_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
    
    for i in range(5): #len(dataset)

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = role_type
        actual_fit = dataset[i][2]
        model.reset_conversation()

        '''TRACING'''
        print('New Record : ', predicate, argument)
        print('New COnversation : ', model.conversation , '\n')


        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , '')
        IsExist2 = data.record_exist(result_filename2, predicate, argument , '')

        if IsExist1 and IsExist2:
            continue
        
        '''Result Preparation'''  
        result1 = [predicate, argument]
        result2 = [predicate, argument]

        '''Retrive the reasons'''
        # the reasons are saved on the 4th position of the record
        reasons = data.retrive_reasons(reason_filename, predicate, argument, '')
        
        print('retived_reasons:\t', type(reasons), '\t', reasons)
        
        # add it to the conversation 
        model.conversation.extend(reasons)
        
        # '''TRACKING'''
        print('Conversation Before the fit scoring: \n', model.conversation)

        '''Generating Sentences Part'''
        sentences = data.get_back_exp_result(sentence_filename, predicate, argument, '')
        
        '''TRACING'''
        print('The sentences are: ', sentences)

        avg1 = 0
        avg2 = 0
        sentence_no = 5

        for sentence in sentences:

            '''Checking Semantic Coherent'''
            is_semantic = fit_scoring.semantic_coherent(model, predicate, argument, roleType, sentence) 

            '''TRACING'''
            print('is_semantic: ', model.conversation)

            '''Sematically Fit Sentence'''
            if is_semantic:  
                result1.append(sentence)
                result2.append(sentence)

                '''Prompting Part For Categorical Result '''
                fit_score_categorical= fit_scoring.simple_gen_sentences(model, predicate, argument, roleType, 'categorical', sentence)

                '''TRACING'''
                print('categorical_with_senetence: ', fit_score_categorical)
                
                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical

                '''Prompting Part For Numerical Result '''
                fit_score_numerical= fit_scoring.simple_gen_sentences(model, predicate, argument, roleType, 'numerical', sentence)

                '''TRACING'''
                print('numerical_with_senetence: ',fit_score_numerical)

                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            else:
                '''Back off'''
                result1.append('')
                result2.append('')
                
                '''Retrieve the data from previous exp'''
                fit_score_categorical = data.get_back_exp_result( f'Result/lemma_tuple_categorical_{dataset_name}_{model_name_only}.csv', predicate, argument, '')
                
                '''TRACING'''
                print('categorical from prevL ', fit_score_categorical)
                
                fit_score_categorical = float(fit_score_categorical[-1])
                
                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical

                
                fit_score_numerical = data.get_back_exp_result(f"Result/lemma_tuple_numerical_{dataset_name}_{model_name_only}.csv", predicate, argument, '')
                
                print('Numerical from prev: ', fit_score_numerical)
                fit_score_numerical = float(fit_score_numerical[-1])
                
                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            # Pop out the assistance prompt of sematic fit 
            model.conversation.pop()

             # Pop out the user prompt of sematic fit
            model.conversation.pop()

            '''TRACING'''
            print('After Poping the semantic: \n', model.conversation)

    '''Add the results'''
    result2.append(actual_fit)
    result2.append(round(avg2/sentence_no,2))

    result1.append(actual_fit)
    result1.append(round(avg1/sentence_no,2))

    '''TRACING'''
    print('result1: ',result1)
    print('result2: ',result2)
    print('---------------------DONE----------------------')

    # Store the result record in the result file
    data.save_result(result_filename2, result2)

    # Store the result record in the result file
    data.save_result(result_filename1, result1)

def exp_reasoning_gen_sentences_other(filename: str, model: Model, model_name: str):
    
    exp_name = 'gen_sentences'
    
    # Adjust the number of token needed for the experiments
    model.adjust_max_tokes(300)       

    # Get the data
    if 'pado' in filename:
        dataset = data.read_data_pado(filename)
    elif 'mcrae' in filename:
        dataset = data.read_data_mcrae(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','role_type','sentence 1','sub-fit score 1','sentence 2','sub-fit score 2','sentence 3','sub-fit score 3','sentence 4','sub-fit score 4', 'sentence 5','sub-fit score 5','actual_fit', 'exp_fit']
    dataset_name = filename.split('.txt')[0]
    model_name_only = model_name.split('/')[1]
    result_filename1 = f'Result/{exp_name}_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/{exp_name}_categorical_{dataset_name}_{model_name_only}.csv'
    sentence_filename = f'Result/gen_sentences_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
   
    for i in range(5): #len(dataset)

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = dataset[i][2]
        actual_fit = dataset[i][3]  
        model.reset_conversation()

        '''TRACING'''
        print('New Record : ', predicate, argument)
        print('New COnversation : ', model.conversation , '\n')


        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , roleType)
        IsExist2 = data.record_exist(result_filename2, predicate, argument , roleType)

        if IsExist1 and IsExist2:
            continue
        
        '''Result Preparation'''  
        result1 = [predicate, argument, roleType]
        result2 = [predicate, argument, roleType]

        '''Retrive the reasons'''
        reasons = data.get_back_exp_result(reason_filename, predicate, argument, roleType)

        # add it to the conversation 
        model.conversation.extend(reasons)
        
        # '''TRACKING'''
        print('Conversation Before the fit scoring: \n', model.conversation)

        '''Retrive Sentences Part'''
        sentences = data.get_back_exp_result(sentence_filename, predicate, argument, roleType)

        
        '''TRACING'''
        print('The sentences are: ', sentences)

        avg1 = 0
        avg2 = 0
        sentence_no = 5

        for sentence in sentences:

            '''Checking Semantic Coherent'''
            is_semantic = fit_scoring.semantic_coherent(model, predicate, argument, roleType, sentence) 

            '''TRACING'''
            print('is_semantic: ', model.conversation)

            '''Sematically Fit Sentence'''
            if is_semantic:  
                result1.append(sentence)
                result2.append(sentence)

                '''Prompting Part For Categorical Result '''
                fit_score_categorical= fit_scoring.simple_gen_sentences(model, predicate, argument, roleType, 'categorical', sentence)

                '''TRACING'''
                print('categorical_with_senetence: ', fit_score_categorical)
                
                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical

                '''Prompting Part For Numerical Result '''
                fit_score_numerical= fit_scoring.simple_gen_sentences(model, predicate, argument, roleType, 'numerical', sentence)

                '''TRACING'''
                print('numerical_with_senetence: ',fit_score_numerical)

                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            else:
                '''Back off'''
                result1.append('')
                result2.append('')
                
                '''Retrieve the data from previous exp'''
                fit_score_categorical = data.get_back_exp_result( f'Result/lemma_tuple_categorical_{dataset_name}_{model_name_only}.csv', predicate, argument, '')
                
                '''TRACING'''
                print('categorical from prevL ', fit_score_categorical)
                
                fit_score_categorical = float(fit_score_categorical[-1])
                
                result2.append(fit_score_categorical)
                avg2 += fit_score_categorical

                
                fit_score_numerical = data.get_back_exp_result(f"Result/lemma_tuple_numerical_{dataset_name}_{model_name_only}.csv", predicate, argument, '')
                
                print('Numerical from prev: ', fit_score_numerical)
                fit_score_numerical = float(fit_score_numerical[-1])
                
                result1.append(fit_score_numerical)
                avg1 += fit_score_numerical

            # Pop out the assistance prompt of sematic fit 
            model.conversation.pop()

             # Pop out the user prompt of sematic fit
            model.conversation.pop()

            '''TRACING'''
            print('After Poping the semantic: \n', model.conversation)

    '''Add the results'''
    result2.append(actual_fit)
    result2.append(round(avg2/sentence_no,2))

    result1.append(actual_fit)
    result1.append(round(avg1/sentence_no,2))

    '''TRACING'''
    print('result1: ',result1)
    print('result2: ',result2)
    print('---------------------DONE----------------------')

    # Store the result record in the result file
    data.save_result(result_filename2, result2)

    # Store the result record in the result file
    data.save_result(result_filename1, result1)

