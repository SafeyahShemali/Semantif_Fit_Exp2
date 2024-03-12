'''Dependecy'''
from openai import OpenAI
from tenacity import (retry, stop_after_attempt, wait_random_exponential)

''' Model class Structure'''
class Model:
    model_name_: str
    api_key_: str
    api_base_: str
    client: None
    conversation: [{}]
    temp: float
    top_p: float
    max_tokens: int

    def __init__(self, model_name_:str , api_key_: str, api_base_: str, temp_: float, top_p_: float,max_tokens_: float):
        self.model_name_= model_name_
        self.api_key_ = api_key_
        self.api_base_ = api_base_
        self.client = OpenAI(api_key = api_key_, base_url= api_base_)
        self.temp = temp_
        self.top_p = top_p_
        self.max_tokens = max_tokens_
        self.conversation = [{"role": "system", "content": "You are a linguist who understands semantic roles and can provide a rating on the semantic fit of predicate-arguments for a specific semantic role, given the predicate, the argument, and the semantic role."}] 
    
    def adjust_max_tokes(self, max_tokens_: int):
        self.max_tokens = max_tokens_
        
    def reset_conversation(self):
         self.conversation = [{"role": "system", "content": "You are a linguist who understands semantic roles and can provide a rating on the semantic fit of predicate-arguments for a specific semantic role, given the predicate, the argument, and the semantic role."}] 
    
    @retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
    def chat_with_model(self):
        completion = self.client.chat.completions.create(
            model= self.model_name_,
            messages= self.conversation,
            temperature= self.temp,
            top_p = self.top_p,
            max_tokens = self.max_tokens
        )
        
        return completion.choices[0].message.content



