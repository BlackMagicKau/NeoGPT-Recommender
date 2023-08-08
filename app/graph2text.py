import os
from vertexai.preview.language_models import TextGenerationModel 
from english2cypher import run_text_model 

    
system = f"""
You are an assistant that helps to generate text to form nice and human understandable answers based.
The latest prompt contains the information, and you need to generate a human readable response based on the given information.
Make it sound like the information are coming from an AI assistant, but don't add any information.
Do not add any additional information that is not explicitly provided in the latest prompt.
I repeat, do not add any information that is not explicitly given.
"""

def generate_response(messages):
    # Convert the messages into a single string for the model
    prompt = "\n".join([f"{message['role']}: {message['content']}" for message in messages])
    
    # Make a request to Vertex AI
    response = run_text_model(prompt)
    
    # The following checks and modifications remain the same:
    print(response)
    if "apologi" in response:
        if "\n" in response:
            response = " ".join(response.split("\n")[1:])
        else:
            response = " ".join(response.split(".")[1:])
    return response

if __name__ == '__main__':
    data = [{'actor': 'Sigourney Weaver', 'role': "Witch"}, {'actor': 'Holly Hunter', "role": "Assassin"}, {
        'actor': 'Dermot Mulroney'}, {'actor': 'William McNamara'}]
    print(generate_response([{'role': 'user', 'content': str(data)}]))