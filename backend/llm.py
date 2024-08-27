

from langchain_groq import ChatGroq

def init_llm(temp,token_size):
    llm = ChatGroq(temperature=temp,verbose=True,max_tokens=token_size, groq_api_key="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", model_name="Llama3-70b-8192")
    print("token size is ",token_size)
    return llm