json_key = "Fit Score"

answer_categorical= f"Reply only with a valid JSON object containing the key \"{json_key}\" and a value that is one of 'Near-Perfect', 'High', 'Medium', 'Low' or 'Near-Impossible', according to the following structure {{\"{json_key}\": String}}. Avoid adding any text outside this JSON object."
answer_numerical=f"Reply only with a valid JSON object containing the key \"{json_key}\" and a value that is a float number from 0 to 1, according to the following structure {{\"{json_key}\": String}}. Avoid adding any text outside this JSON object."
answer_gen_sentences = f"Reply only with a valid JSON object containing the key \"{json_key}\" and a value that is a list of five semantically coherent sentences, each with the given predicate, argument, and role according to the following structure {{\"{json_key}\": String}}. Avoid adding any text outside this JSON object."
answer_check_semantic = f"Reply only with a valid JSON object containing the key \"{json_key}\" and a value 'Yes' or 'No', according to the following structure {{\"{json_key}\": String}}. Avoid adding any text outside this JSON object."
answer_reason = f"Reply only with a valid JSON object containing the key \"{json_key}\" and a value that is the answer for the question, according to the following structure {{\"{json_key}\": String}}. Avoid adding any text outside this JSON object."
    
    
print(answer_categorical)
print(answer_numerical)
print(answer_gen_sentences)
print(answer_check_semantic)
print(answer_reason)