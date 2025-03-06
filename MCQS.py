from flask import request, jsonify
from langchain_core.prompts import ChatPromptTemplate
from llm import init_llm

def generate():
    data = request.json
    job = data.get("job")
    
    # Create a prompt that emphasizes randomness but is still efficient
    prompt = ChatPromptTemplate.from_template(
        f"Generate 15 completely random multiple-choice questions (MCQs) for a test related to {job}. "
        "Make sure each set of questions is different each time this prompt is run. "
        "Include a diverse and unpredictable mix of easy, medium, and difficult questions covering different aspects of the field. "
        "Each question should have four options labeled A, B, C, and D, and provide the correct answer. "
        "Try to be creative and unpredictable in the topics you cover within the {job} field. "
        "Format each question and answer pair like 'Q: <question> Options: A. <option1>, B. <option2>, C. <option3>, D. <option4>. Answer: <correct option>'."
    )
    
    # Initialize the language model with parameters that encourage randomness
    # Higher temperature (0.9) for more diverse and random responses
    llm = init_llm(0.9, 600)
    
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
            try:
                question_part, answer_part = qa.split("Answer: ", 1)
                if "Options: " in question_part:
                    question_text, options_text = question_part.split("Options: ", 1)
                    options = options_text.split(", ")
                    
                    # Ensure we have exactly 4 options before processing
                    if len(options) == 4:
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
            except Exception as e:
                # Skip malformed questions
                continue
    
    # Return the formatted response as JSON
    return jsonify({'mcqs': formatted_response}), 200
