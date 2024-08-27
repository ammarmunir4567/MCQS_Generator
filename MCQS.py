from flask import request, jsonify
from langchain_core.prompts import ChatPromptTemplate
from llm import init_llm

def generate():
    data = request.json
    job = data.get("job")

    
    # Create the prompt for generating MCQs
    prompt = ChatPromptTemplate.from_template(
        f"Generate 5000 random multiple-choice questions (MCQs) for a MCQS test related to {job}. "
        "Each question should have four options labeled A, B, C, and D, and provide the correct answer. "
        f"Give me total of exact  15 mcqs ,no more than 15 MCQS else you will be punished"
        "Format each question and answer pair like 'Q: <question> Options: A. <option1>, B. <option2>, C. <option3>, D. <option4>. Answer: <correct option>'."
    )
    
    # Initialize the language model with specified parameters
    llm = init_llm(0.9,1000)
    
    # Combine the prompt and language model
    chain = prompt | llm
    
    # Invoke the chain with the job data
    response = chain.invoke({"job": job})
    

    # Store the generated MCQs and answers
    mcqs_with_answers = response.content.split("\n\n")  # Assuming each question-answer pair is separated by a double newline
    
    # Format the response for sending to the frontend
    formatted_response = []
    for qa in mcqs_with_answers:
        if "Answer: " in qa:
            question_part, answer_part = qa.split("Answer: ", 1)
            question_text, options_text = question_part.split("Options: ", 1)
            options = options_text.split(", ")
            formatted_response.append({
                "question": question_text.replace("Q: ", "").strip(),
                "options": {
                    "A": options[0].replace("A. ", "").strip(),
                    "B": options[1].replace("B. ", "").strip(),
                    "C": options[2].replace("C. ", "").strip(),
                    "D": options[3].replace("D. ", "").strip()
                },
                "answer": answer_part.strip()
            })
    
    # Return the formatted response as JSON
    return jsonify({'mcqs': formatted_response}), 200