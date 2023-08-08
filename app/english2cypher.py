import os
from vertexai.preview.language_models import TextGenerationModel
from retry import retry


def run_text_model(
    prompt: str,
    project_id: str = project_id,
    model_name: str = model_name,
    temperature: float = 0.0,
    max_decode_steps: int = 100,  # Assuming a default value
    top_p: float = 1.0,  # Assuming a default value
    top_k: int = 10,    # Assuming a default value
    location: str = location,
    tuned_model_name: str = ""
) -> str:
    """Text Completion Use a Large Language Model."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_name)
    if tuned_model_name:
        model = model.get_tuned_model(tuned_model_name)
    response = model.predict(
        prompt,
        temperature=temperature,
        max_output_tokens=max_decode_steps,
        top_k=top_k,
        top_p=top_p
    )
    return response.text

@retry(tries=2, delay=5)
def generate_cypher(messages):
    # Convert the messages into a single string for the model
    prompt = "\n".join([f"{message['role']}: {message['content']}" for message in messages])
    
    # Make a request to Vertex AI
    response = run_text_model(prompt)
    
    # The following checks and modifications remain the same:
    if not "MATCH" in response and "{" in response:
        raise Exception(
            "Model bypassed system message and is returning response based on previous conversation history" + response)
    if "apologi" in response:
        response = " ".join(response.split("\n")[1:])
    if "`" in response:
        response = response.split("```")[1].strip("`")
    print(response)
    return response

if __name__ == '__main__':
    print(generate_cypher([{'role': 'user', 'content': 'What are some good cartoon?'},
                           {'role': 'assistant', 'content': 'Shrek 3'},
                           {'role': 'user',
                               'content': 'Which actors appeared in it?'}
                           ]))
    print(generate_cypher([{'role': 'user', 'content': 'What are some good cartoon?'},
                           {'role': 'assistant', 'content': 'Shrek 3'},
                           {'role': 'user',
                               'content': 'Who was the first person on the moon?'}
                           ]))

