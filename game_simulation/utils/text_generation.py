import openai
import re
import os
from dotenv import load_dotenv
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import numpy as np
# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
hf_generator = None


def generate(prompt, use_openai=True):
    """
    Generates a text completion for a given prompt using either the OpenAI GPT-3 API or the Hugging Face GPT-3 model.
    
    Args:
    - prompt (str): The text prompt to generate a completion for.
    - use_openai (bool): A boolean flag indicating whether to use the OpenAI API (True) or the Hugging Face GPT-3 model (False).
    
    Returns:
    - str: The generated text completion.
    """
    if use_openai:
        # model_engine = "text-davinci-002"
        # response = openai.Completion.create(
        #     engine=model_engine,
        #     prompt=prompt,
        #     max_tokens=1024,
        #     n=1,
        #     stop=None,
        #     temperature=0.5,
        # )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages = [
            {"role": "user", "content" : f"{prompt}"},  ],
            max_tokens=1024,
            temperature=0.5,
        )

        message = response.choices[0]["message"]["content"]
        return message.strip()

    else:
        global hf_generator
        if hf_generator is None:
            hf_generator = pipeline(model='declare-lab/flan-alpaca-xl', device=0)
        output = hf_generator(prompt, max_length=len(prompt)+128, do_sample=True)
        out = output[0]['generated_text']
        if '### Response:' in out:
            out = out.split('### Response:')[1]
        if '### Instruction:' in out:
            out = out.split('### Instruction:')[0]
        return out.strip()


def get_rating(x):
    """
    Extracts a rating from a string.
    
    Args:
    - x (str): The string to extract the rating from.
    
    Returns:
    - int: The rating extracted from the string, or None if no rating is found.
    """
    nums = [int(i) for i in re.findall(r'\d+', x)]
    if len(nums)>0:
        return min(nums)
    else:
        return None

# Summarize simulation loop with OpenAI GPT-4
def summarize_simulation(log_output):
    prompt = f"Summarize the simulation loop:\n\n{log_output}"
    response = generate(prompt)
    return response

def embedding(prompt,use_openai=True):
    if use_openai:
        resp = openai.Embedding.create(
            input=[prompt],
            engine="text-similarity-davinci-001")
        return resp['data'][0]['embedding'] 
    else:
        model = SentenceTransformer('all-MiniLM-L6-v2') #using a relatively smaller size model from the api
        return model.encode(prompt, convert_to_tensor=True)

def similar(x, y):
    """
    input: Two numpy arrays, x and y
    output: similarity score range between 0 and 1
    """ 
    return util.cos_sim(x,y)