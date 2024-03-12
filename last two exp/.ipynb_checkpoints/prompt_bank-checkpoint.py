system_prompt = "You are a linguist who understands semantic roles and can provide a rating on the semantic fit of predicate-arguments for a specific semantic role, given the predicate, the argument, and the semantic role."
def get_prompt(prompt_type: str, predicate: str, argument: str, roleType: str, json_key: str, sentence = ''):

    simple_lemma_tuple = f"Given the predicate '{predicate}', how much does the argument '{argument}' fit the role of {roleType}?"
    simple_gen_sentences = f"Given the following sentence '{sentence}', for the predicate '{predicate}', how much does the argument '{argument}' fit the role of {roleType}?"
    
    gen_sentences = f"Generate five semantically coherent sentences with the predicate '{predicate}', argument '{argument}', and the role of {roleType}"
    check_semantic = f"Is the given sentence '{sentence} semantically coherent and containing the predicate '{predicate}' and the argument '{argument}' in the role of {roleType}?"
    
    answer_categorical= f"Reply only with a valid JSON object containing the key \"{json_key}\" and a value that is one of 'Near-Perfect', 'High', 'Medium', 'Low' or 'Near-Impossible', according to the following structure {{\"{json_key}\": String}}. Avoid adding any text outside this JSON object."
    answer_numerical=f"Reply only with a valid JSON object containing the key \"{json_key}\" and a value that is a float number from 0 to 1, according to the following structure {{\"{json_key}\": String}}. Avoid adding any text outside this JSON object."
    answer_gen_sentences = f"Reply only with a valid JSON object containing the key \"{json_key}\" and a value that is a list of five semantically coherent sentences, each with the given predicate, argument, and role according to the following structure {{\"{json_key}\": String}}. Avoid adding any text outside this JSON object."
    answer_check_semantic = f"Reply only with a valid JSON object containing the key \"{json_key}\" and a value 'Yes' or 'No', according to the following structure {{\"{json_key}\": String}}. Avoid adding any text outside this JSON object."
    
    answer_reason = f"Reply only with a valid JSON object containing the key \"{json_key}\" and a value that is the answer for the question, according to the following structure {{\"{json_key}\": String}}. Avoid adding any text outside this JSON object."
    reasons = [f"Given the predicate '{predicate}', what properties should the {roleType} role have? {answer_reason}",
                
               f"Given the predicate '{predicate}', and the argument '{argument}', what relevant properties does the argument have? {answer_reason}",
              
               f"Given the above, how will the argument '{argument}' fit the {roleType} role for the predicate '{predicate}'? {answer_reason}"]
    
    if prompt_type == 'simple_lemma_tuple_categorical':
        return f"{simple_lemma_tuple} {answer_categorical}"
    elif prompt_type == 'simple_lemma_tuple_numerical':
        return f"{simple_lemma_tuple} {answer_numerical}"
    elif prompt_type == 'reasoning_lemma_tuple':
        return reasons
    elif prompt_type == 'gen_sentences':
        return f"{gen_sentences} {answer_gen_sentences}"
    elif prompt_type == 'check_semantic':
        return f"{check_semantic} {answer_check_semantic}"
    elif prompt_type == 'simple_gen_sentences_categorical':
        return f"{simple_gen_sentences} {answer_categorical}"
    elif prompt_type == 'simple_gen_sentences_numerical':
        return f"{simple_gen_sentences} {answer_numerical}"