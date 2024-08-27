

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
def init_llm(temp,token_size):
    llm = ChatGroq(temperature=temp,verbose=True,max_tokens=token_size, groq_api_key=os.getenv('GROQ_API'), model_name="llama-3.1-70b-versatile")
    print("token size is ",token_size)
    return llm