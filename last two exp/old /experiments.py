import fit_scoring
from models import Model
import data

def exp_lemma_tuple_ferretti(filename: str, role_type: str, model: Model, model_name: str):

    exp_name = 'lemma_tuple'
    max_tokens = 100
    
    # get the data
    dataset = data.read_data(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument', 'actual_fit', 'exp_fit']
    dataset_name = filename.split('.csv')[0]
    model_name_only = model_name.split('/')[1]
    result_filename1 = f'Result/lemma_tuple_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/lemma_tuple_categorical_{dataset_name}_{model_name_only}.csv'

    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
   
    for i in range(len(dataset)): #len(dataset)

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = role_type
        actual_fit = dataset[i][2]
        model.conversation = []
        print('conversation', model.conversation)

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , '')
        IsExist2 = data.record_exist(result_filename2, predicate, argument , '')

        if IsExist1 and IsExist2:
            continue
        else:
            print(f'the record is missing in either in E11 {IsExist1} or in {IsExist2}')

        '''TRACING'''
        print('New Record:', predicate, argument)
    
        '''Result Preparation'''  
        result1 = [predicate, argument, actual_fit]
        result2 = [predicate, argument, actual_fit]

        '''Prompting Part For Categorical Result '''
        fit_score_categorical= fit_scoring.categorical(model, max_tokens,predicate, argument, roleType)

        # Add the fit score to the result list
        result2.append(fit_score_categorical)

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        '''Prompting Part For Categorical Result '''
        print(result1)
        fit_score_numerical= fit_scoring.numerical(
            model, max_tokens, predicate, argument, roleType)

        # Add the fit score to the result list
        result1.append(fit_score_numerical)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)



def exp_lemma_tuple_reasoning_ferretti(filename: str, role_type: str, model: Model, model_name: str):

    exp_name = 'lemma_tuple'
    
    # adjust the number of token needed for the experiments
    model.adjust_max_tokes(600)    
    
    # get the data
    dataset = data.read_data(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument', 'reason1', 'reason2', 'reason3','actual_fit', 'exp_fit']
    dataset_name = filename.split('.csv')[0]
    model_name_only = model_name.split('/')[1]
    result_filename1 = f'Result/reasoning_lemma_tuple_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/reasoning_lemma_tuple_categorical_{dataset_name}_{model_name_only}.csv'


    if not data.is_file_exits(result_filename1):
        data.open_result_file(filename= result_filename1, fields= fields)
    if not data.is_file_exits(result_filename2):
        data.open_result_file(filename= result_filename2, fields= fields)
   
    for i in range(len(dataset)): #len(dataset)

        '''Data Extraction'''
        predicate = dataset[i][0]
        argument = dataset[i][1]
        roleType = role_type
        actual_fit = dataset[i][2]
        model.conversation = []
        print('conversation', model.conversation)

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , '')
        IsExist2 = data.record_exist(result_filename2, predicate, argument , '')

        if IsExist1 and IsExist2:
            continue
        else:
            print(f'the record is missing in either in E11 {IsExist1} or in {IsExist2}')

        '''TRACING'''
        print('New Record:', predicate, argument)
    
        '''Result Preparation'''  
        result1 = [predicate, argument, actual_fit]
        result2 = [predicate, argument, actual_fit]


        '''Reasoning'''
        reasons_results = fit_scoring.reasoning(model,predicate, argument, roleType)
        
        '''TRACKING'''
        print(reasons_results)
        
        # Return the answer as a JSON Object  with the structure {"Response": String}
        
        result1.extend(reasons_results)
        result2.extend(reasons_results)

        '''Prompting Part For Categorical Result '''
        fit_score_categorical= fit_scoring.categorical(model,predicate, argument, roleType)

        # Add the fit score to the result list
        result2.append(fit_score_categorical)

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        '''Prompting Part For Categorical Result '''
        print(result1)
        fit_score_numerical= fit_scoring.numerical(
            model, predicate, argument, roleType)

        # Add the fit score to the result list
        result1.append(fit_score_numerical)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)


def exp_gen_sentences_ferretti(filename: str, role_type: str, model: Model, model_name: str):

    exp_name = 'gen_sentences'
    
    # adjust the number of token needed for the experiments
    model.adjust_max_tokes(300) 
    
    # get the data
    dataset = data.read_data(filename)

    # Create files for the results if not exits 
    fields = ['predicate', 'argument','sentence 1','sub-fit score 1','sentence 2','sub-fit score 2','sentence 3','sub-fit score 3','sentence 4','sub-fit score 4', 'sentence 5','sub-fit score 5','actual_fit', 'exp_fit']
    dataset_name = filename.split('.csv')[0]
    model_name_only = model_name.split('/')[1]
    result_filename1 = f'Result/gen_sentence_numerical_{dataset_name}_{model_name_only}.csv'
    result_filename2 = f'Result/gen_sentence_categorical_{dataset_name}_{model_name_only}.csv'

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
        
        print('conversation', model.conversation)

        '''Check if this record exists already'''
        IsExist1 = data.record_exist(result_filename1, predicate, argument , '')
        IsExist2 = data.record_exist(result_filename2, predicate, argument , '')

        if IsExist1 and IsExist2:
            continue
        else:
            print(f'the record is missing in either in E11 {IsExist1} or in {IsExist2}')

        '''TRACING'''
        print('New Record:', predicate, argument)
    
        '''Result Preparation'''  
        result1 = [predicate, argument]
        result2 = [predicate, argument]
        
        '''Generating Sentences Part'''
        sentences = fit_scoring.generate_sentence(model, predicate, argument, roleType)
        
        avg1 = 0
        avg2 = 0
        sentence_no = 5
        
        for sentence in sentences:
                        
            '''Checking Semantic Coherent'''
            is_semantic = fit_scoring.semantic_coherent(model, predicate, argument, roleType, sentence) 
            
            print(' \n\n\n new senetence ',model.conversation , '\n\n\n')
            
            '''Sematically Fit Sentence'''
            if is_semantic:  
                result1.append(sentence)
                result2.append(sentence)
                
                fit_score = fit_scoring.categorical_with_senetence(model, predicate, argument, roleType, sentence)
                
                '''TRACING'''
                print('categorical_with_senetence',fit_score)
                
                result2.append(fit_score)
                avg2 += fit_score
                
                fit_score = fit_scoring.numerical_with_senetence(model, predicate, argument, roleType, sentence)
                
                '''TRACING'''
                print('numerical_with_senetence',fit_score)
                
                result1.append(fit_score)
                avg1 += fit_score
                
            else:
                result1.append('')
                result2.append('')
                
                '''retrieve the data from previous exp'''
                categorical = data.get_back_exp_result( f'Result/lemma_tuple_categorical_{dataset_name}_{model_name_only}.csv', predicate, argument, '')
                
                print('categorical from prev', categorical)
                fit_score = float(categorical[-1])
                result2.append(fit_score)
                avg2 += fit_score

                
                numerical = data.get_back_exp_result(f"Result/lemma_tuple_numerical_{dataset_name}_{model_name_only}.csv", predicate, argument, '')
                print('numerical from prev', numerical)
                fit_score = float(numerical[-1])
                result1.append(fit_score)
                avg1 += fit_score
                
             # Pop out the user prompt of sematic fit
            model.conversation.pop()

             # Pop out the assistance prompt of sematic fit
            model.conversation.pop()
            
            print(' after poping ',model.conversation , '\n\n\n *****************')
            
            
        '''Add the results'''
        result2.append(actual_fit)
        result2.append(round(avg2/sentence_no,2))

        result1.append(actual_fit)
        result1.append(round(avg1/sentence_no,2))

        '''TRACING'''
        print(result1)
        print(result2)

        # Store the result record in the result file
        data.save_result(result_filename2, result2)

        # Store the result record in the result file
        data.save_result(result_filename1, result1)



        




        