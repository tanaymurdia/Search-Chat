from openai import OpenAI
import re
from duckduckgo_search import DDGS

def get_ddgs_ai_result(userInput, prev_conv):
    prompt = "This is the previous conversation: "+ str(prev_conv) + ". The user sent this message: \"" + userInput +"\". Please provide Search results, the format of the output should be for each search result, first the source url and then the description. Return the source url as <a href='https://www.example.com'>Url Title</button> and removing numbering from the final tetx "
    results = DDGS().chat(prompt)
    print(results)
    return results

