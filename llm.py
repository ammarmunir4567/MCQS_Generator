from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import random

load_dotenv()

def init_llm(temp, token_size):
    # Add additional randomness parameters
    # 1. Use a slightly randomized temperature each time
    random_temp = temp + (random.random() * 0.1 - 0.05)  # +/- 0.05 random variation
    
    # 2. Add top_p sampling for more diversity
    top_p = 0.95
    
    # 3. Add frequency_penalty to reduce repetition
    frequency_penalty = 0.5
    
    llm = ChatGroq(
        temperature=random_temp,
        verbose=True,
        max_tokens=token_size,
        groq_api_key=os.getenv('GROQ_API'),
        model_name="llama-3.3-70b-versatile",
        top_p=top_p,
        frequency_penalty=frequency_penalty
    )
    
    print(f"Using parameters: temperature={random_temp:.2f}, top_p={top_p}, frequency_penalty={frequency_penalty}, token size={token_size}")
    return llm
