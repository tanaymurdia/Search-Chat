from openai import OpenAI
import re
from duckduckgo_search import DDGS

def get_ddgs_ai_result(userInput, prev_conv):
    prompt = "This is the previous conversation: "+ str(prev_conv) + ". The user sent this message: \"" + userInput +"\". Please provide Search results with relevant and existing links, the format of the output should be for each search result, first the source url and then the description. Return the source url as <a href='https://www.example.com'>Url Title</button> and removing numbering from the final text. Alos make sure the links are working by testing them "
    results = DDGS().chat(prompt)
    prompt2 = "Make sure that this reponse: { response: "+ str(results) + " }, has all the links leading to pages that contain information, if not replace that info to pages that exist and are relevent using the same format"
    results2= DDGS().chat(prompt2)
    print(results2)
    return results2

