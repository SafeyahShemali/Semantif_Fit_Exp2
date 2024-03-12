from models import Model
import json
import data
import prompt_bank

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
    
def simple_lemma_tuple(model: Model, predicate: str, argument: str, roleType: str, result_type: str):
    
    json_key = 'Fit score'
    # The User Prompt
    user_prompt = prompt_bank.get_prompt(f"simple_lemma_tuple_{result_type}", predicate, argument, roleType, json_key)
    
    '''TRACING'''
    print('user_prompt : ', user_prompt)
    
    # Add the user prompt to the conversation 
    model.conversation.append({"role": "user", "content": user_prompt})

    # Interact with model
    response_fit_score =  model.chat_with_model()       

    '''TRACING'''
    print('response_fit_score: ', response_fit_score)

    # Processing JSON
    fit_score = data.processing_json(response_fit_score,json_key, f"error_{json_key}.csv", predicate, argument, roleType)    

    # Pop out the last user prompt to prevent bias in the evaluation
    model.conversation.pop()

    '''TRACING'''
    print('conversation after:', model.conversation)
    
     # Convert it to a float number according to the resultType scale
    if result_type == 'categorical':
        return textual_to_numerical_scale(fit_score)
    elif result_type == 'numerical':
        try:
            return float(fit_score)
        except:
            print('error ', predicate, argument, roleType)
            return None

def reasoning(model: Model, predicate: str, argument: str, roleType: str, reason_filename: str):

    reasons_result  = [predicate, argument, roleType]
    json_key = 'Response'
    reasons=  prompt_bank.get_prompt('reasoning_lemma_tuple', predicate, argument, roleType, json_key)
    print('reasons: \n', reasons)

    for reason_prompt in reasons:
        
        '''TRACING'''
        print('Before Adding Reason /n', model.conversation)

        # Add the user prompt to the conversation 
        model.conversation.append({"role": "user", "content": reason_prompt})

        # Interact with model
        response_reason = model.chat_with_model()
        
        '''TRACING'''
        print('response_reason: \n', response_reason)
        
        # Processing JSON
        reason = data.processing_json(response_reason,json_key, f"error_{json_key}.csv", predicate, argument, roleType)   

        # Checking:
        if not reason:
            sys.exit("No Reason")   

        # Store the reason for latter
        reasons_result.append(reason)
                
        # Add it to the conversation
        model.conversation.append({"role": "assistant", "content": reason})

        print('join reasons: ', reasons_result)
        
    # Saving the Reasons
    data.save_result(reason_filename, reasons_result)


def generate_sentence(model: Model, predicate: str, argument: str, roleType: str):
    
    json_key = 'Sentences'

    # The User Prompt
    gen_sentence_prompt = prompt_bank.get_prompt('gen_sentences', predicate, argument, roleType, json_key)
   
    '''TRACING'''
    print('user_prompt : ', gen_sentence_prompt) 

    # Add the user prompt to the conversation 
    model.conversation.append({"role": "user", "content": gen_sentence_prompt})

    # Interact with model
    response_sentences =  model.chat_with_model()       

    '''TRACING'''
    print('response_sentences: ', response_sentences)

    # Processing JSON
    sentences = data.processing_json(response_sentences, json_key, f"error_{json_key}.csv", predicate, argument, roleType)    

    # Pop out the last user prompt to prevent bias in the evaluation
    model.conversation.pop()
    
    '''TRACING'''
    print('sentences: ', type(sentences))
    print('sentences: ', sentences)

    return sentences 

def semantic_coherent(model: Model, predicate: str, argument: str, roleType: str, sentence: str):
    
    json_key = 'Is Fit'

    # The User Prompt
    check_semantic_prompt = prompt_bank.get_prompt('check_semantic', predicate, argument, roleType, json_key, sentence=sentence)
   
    '''TRACING'''
    print('check_semantic_prompt : ', check_semantic_prompt) 
    
    # Add the user prompt to the conversation 
    model.conversation.append({"role": "user", "content": check_semantic_prompt})
    
    # Interact with model
    response_check_semantic = model.chat_with_model()
    
    '''TRACING'''
    print('response_check_semantic: ', response_check_semantic)
    
    is_semantic = data.processing_json(response_check_semantic,json_key, f"error_{json_key}.csv", predicate, argument, roleType)
    
    model.conversation.append({"role": "assistant", "content": f"{is_semantic}"})

    if 'No' in is_semantic:
        return False
    elif 'Yes' in is_semantic:
        return True
    
def simple_gen_sentences(model: Model, predicate: str, argument: str, roleType: str, result_type: str, sentence: str):

    json_key = 'Fit score'
    # The User Prompt
    user_prompt = prompt_bank.get_prompt(f"simple_gen_sentences_{result_type}", predicate, argument, roleType, json_key, sentence=sentence)
    
    '''TRACING'''
    print('user_prompt : ', user_prompt)
    
    # Add the user prompt to the conversation 
    model.conversation.append({"role": "user", "content": user_prompt})

    # Interact with model
    response_fit_score =  model.chat_with_model()       

    '''TRACING'''
    print('response_fit_score: ', response_fit_score)

    # Processing JSON
    fit_score = data.processing_json(response_fit_score,json_key, f"error_{json_key}.csv", predicate, argument, roleType)    

    # Pop out the last user prompt to prevent bias in the evaluation
    model.conversation.pop()

    '''TRACING'''
    print('conversation after:', model.conversation)
    
     # Convert it to a float number according to the resultType scale
    if result_type == 'categorical':
        return textual_to_numerical_scale(fit_score)
    elif result_type == 'numerical':
        return float(fit_score)
