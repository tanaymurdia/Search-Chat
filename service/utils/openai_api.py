from openai import OpenAI
import re
from duckduckgo_search import DDGS

def get_ddgs_ai_result(userInput, prev_conv):
    prompt = "This is the previous conversation: "+ str(prev_conv) + ". The user sent this message: \"" + userInput +"\". Please provide Search results, the format of the output should be for each search result, first the source url and then the description. Return the source url as <a href='https://www.example.com'>Url Title</button> and removing numbering from the final tetx "
    results = DDGS().chat(prompt)
    print(results)
    return results

def get_open_ai_resp(userInput):

    # Define the prompt you want to send to the GPT model
    global api_key
    client = OpenAI(api_key=api_key)
    prompt = " The user sent this message: \"" + userInput +"\". Answer this question"
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
           {"role": "system", "content": "You are a chatbot on the website of PartSelect(https://www.partselect.com/)."},
        {"role": "user", "content": prompt}
    ]
    )
    print("get_open_ai_non_relevant_resp: ",completion.choices[0].message.content)
    return completion.choices[0].message.content
    

