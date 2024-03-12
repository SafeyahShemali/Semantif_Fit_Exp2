from models import Model
import json
import data

def categorical(model: Model, predicate: str, argument: str, roleType: str):
    
    # The User Prompt
    prompt_fit_score_textual= f"Given the predicate '{predicate}', how much does the argument '{argument}' fit the role of {roleType}?"
    
    answer_structure= f" Reply only with a valid JSON object containing the key 'Fit score' and a value that is one of 'Near-Perfect', 'High', 'Medium', 'Low' or 'Near-Impossible', following the structure {{'Fit score': String}}. Avoid adding any text outside this JSON object."

    '''TRACING'''
    print(prompt_fit_score_textual+answer_structure)
    print('conversation before:', model.conversation)
    
    # Add the user prompt to the conversation 
    model.conversation.append({"role": "user", "content": prompt_fit_score_textual+answer_structure})

    # Interact with model
    response_fit_score =  model.chat_with_model()       

    print('response_fit_score', response_fit_score)
    # Processing JSON
    fit_score = json.loads(response_fit_score)['Fit score']

        
    # Pop out the last user prompt to prevent bias in the evaluation
    model.conversation.pop()

    '''TRACING'''
    print('conversation after:', model.conversation)
    
    # Convert it to a float number
    fit_score = textual_to_numerical_scale(fit_score)

    return fit_score

def categorical_with_senetence(model: Model, predicate: str, argument: str, roleType: str, sentence: str):
    
    prompt_fit_score_textual= f"Given the following sentence, '{sentence}', for the predicate '{predicate}', how much does the argument '{argument}' fit the role of {roleType}?"
    
    answer_structure= f" Reply only with a valid JSON object containing the key 'Fit score' and a value that is one of 'Near-Perfect', 'High', 'Medium', 'Low' or 'Near-Impossible', following the structure {{'Fit score': String}}. Avoid adding any text outside this JSON object."

    '''TRACING'''
    print(prompt_fit_score_textual+answer_structure)
    print('conversation before:', model.conversation)
    
    # Add the user prompt to the conversation 
    model.conversation.append({"role": "user", "content": prompt_fit_score_textual+answer_structure})

    # Interact with model
    response_fit_score =  model.chat_with_model()       

    print('response_fit_score', response_fit_score)
    
    # Processing JSON
    fit_score = data.processing_json(response_fit_score, 'error.csv', predicate, argument, roleType)['Fit score']    
    
    # Pop out the last user prompt to prevent bias in the evaluation
    model.conversation.pop()

    '''TRACING'''
    print('conversation after:', model.conversation)
    
    # Convert it to a float number
    fit_score = textual_to_numerical_scale(fit_score)

    return fit_score

def numerical(model: Model, predicate: str, argument: str, roleType: str):
    
    # The User Prompt
    prompt_fit_score= f"Given the predicate '{predicate}', how much does the argument '{argument}' fit the role of {roleType}?"
    
    answer_structure= f" Reply only with a valid JSON object containing the key 'Fit score' and a value that is a float number from 0 to 1, following the structure {{'Fit score': Float}}. Avoid adding any text outside this JSON object. Do not include ```json in the response."

    '''TRACING'''
    print(prompt_fit_score+answer_structure)
    print('conversation before:', model.conversation)
    
    # Add the user prompt to the conversation 
    model.conversation.append({"role": "user", "content": prompt_fit_score+answer_structure})
    
    # Interact with model
    response_fit_score = model.chat_with_model()                             
    print('response_fit_score', response_fit_score)

    # Processing JSON
    fit_score = float(json.loads(response_fit_score)['Fit score'])
    
    # Pop out the last user prompt to prevent bias in the evaluation
    model.conversation.pop()

    '''TRACING'''
    print('conversation before:', model.conversation)
    
    return fit_score

def numerical_with_senetence(model: Model, predicate: str, argument: str, roleType: str, sentence: str):
    
    # The User Prompt
    prompt_fit_score= f"Given the following sentence '{sentence}', for the predicate '{predicate}', how much does the argument '{argument}' fit the role of {roleType}?"
    
    answer_structure= f" Reply only with a valid JSON object containing the key 'Fit score' and a value that is a float number from 0 to 1, following the structure {{'Fit score': Float}}. Avoid adding any text outside this JSON object."

    '''TRACING'''
    print(prompt_fit_score+answer_structure)
    print('conversation before:', model.conversation)
    
    # Add the user prompt to the conversation 
    model.conversation.append({"role": "user", "content": prompt_fit_score+answer_structure})
    
    # Interact with model
    response_fit_score = model.chat_with_model()                             
    print('response_fit_score', response_fit_score)

   # Processing JSON
    fit_score = float(data.processing_json(response_fit_score, 'error.csv', predicate, argument, roleType)['Fit score'])   
    
    
    # Pop out the last user prompt to prevent bias in the evaluation
    model.conversation.pop()

    '''TRACING'''
    print('conversation after:', model.conversation)
    
    return fit_score

def textual_to_numerical_scale(level):

    if "Near-Impossible" in level:
        return 0.0
    elif "Low" in level:
        return 0.25
    elif "Medium" in level:
        return 0.5
    elif "High" in level:
        return 0.75
    elif "Near-Perfect" in level:
        return 1.0
    

def reasoning(model: Model, predicate: str, argument: str, roleType: str):

    reasons_result  = []
    reasons = [f"Given the predicate '{predicate}', what properties should the {roleType} role have?",
                
               f"Given  the predicate '{predicate}', and the argument '{argument}', what relevant properties does the argument have?",
              
               f"Given the above, how will the argument '{argument}' fit the {roleType} role for the predicate '{predicate}'?"]
    
    response_format = ' Reply only with a valid JSON object with the structure {"Response": String}. Avoid adding any text outside this JSON object. Do not include ```json in the response. Make sure that the answer length fits in the JSON object.'
    
    # Do not return any non-json text or numbering. 
 
    for reason_prompt in reasons:
        
        '''TRACING'''
        print('#############reason_prompt:#################\n', reason_prompt+response_format)
        
        # Add the user prompt to the conversation 
        model.conversation.append({"role": "user", "content": f"{reason_prompt} {response_format}"})
        print('After /n/n', model.conversation)

        # Interact with model
        response_reason = model.chat_with_model()
        
        '''TRACING'''
        print('response_reason', response_reason , '\n-----------\n')
        
        # Processing JSON
        try:
            reason = json.loads(response_reason)['Response']    
        except:
            reason = response_reason        

        # Saving the results
        reasons_result.append(reason)
                
        # Add it to the conversation
        model.conversation.append({"role": "assistant", "content": f"{reason}"})

    return reasons_result

def generate_sentence(model: Model, predicate: str, argument: str, roleType: str):
    
    prompt_generate_sentence = f"Generate five semantically coherent sentences with the predicate '{predicate}', argument '{argument}', and the role of {roleType}."

    answer_structure= f" Reply only with a valid JSON object containing the key 'Sentences' and a value that is a list of  five semantically coherent sentences, each with the given predicate, argument, and role in the following the structure {{'Sentences': [String]}}. Avoid adding any text outside this JSON object."

    '''TRACING'''
    print(prompt_generate_sentence+answer_structure)
    print('conversation before:', model.conversation)
    
    # Add the user prompt to the conversation 
    model.conversation.append({"role": "user", "content": prompt_generate_sentence+answer_structure})
        
    response_generate_sentence = model.chat_with_model()

    '''TRACING'''
    print('response_generate_sentence', response_generate_sentence)
    
    sentences = json.loads(response_generate_sentence)["Sentences"]
    
    # Pop out the last user prompt to prevent bias in the evaluation
    model.conversation.pop()
    
    return sentences 

def semantic_coherent(model: Model,  predicate: str, argument: str, roleType: str, sentence: str):
    prompt_check_semantic = f"Is the given sentence '{sentence}' semantically coherent and containing the given predicate  '{predicate}' and the argument '{argument}' in the role of {roleType}?"
    
    answer_structure = f" Reply only with a valid JSON object containing the key 'Is Fit' and the value 'Yes' or 'No' in the following structure {{'Is Fit': String}}. Avoid adding any text outside this JSON object."
    
    '''TRACING'''
    print(prompt_check_semantic+answer_structure)
    print('conversation before:', model.conversation)
    
    # Add the user prompt to the conversation 
    model.conversation.append({"role": "user", "content": prompt_check_semantic+answer_structure})
    
    response_check_semantic = model.chat_with_model()
    
    '''TRACING'''
    print('response_check_semantic', response_check_semantic)
    
    
    check_semantic = data.processing_json(response_check_semantic, 'error.csv', predicate, argument, roleType)["Is Fit"] 
    print(check_semantic)
    # check_semantic = json.loads(response_check_semantic)["Is Fit"]  
    
    model.conversation.append({"role": "assistant", "content": f"{check_semantic}"})

    if 'No' in check_semantic:
        return False
    else:
        return True
    
