from flask import request, jsonify
from langchain_core.prompts import ChatPromptTemplate
from llm import init_llm

def generate():
    data = request.json
    job = data.get("job")
    
    # Add a timestamp to ensure different seeds even for identical requests
    import time
    timestamp = str(time.time())
    
    # Create a prompt with multiple randomness factors
    prompt = ChatPromptTemplate.from_template(
        f"Generate 15 completely random multiple-choice questions (MCQs) for a test related to {job}. "
        "Make sure each set of questions is different each time this prompt is run. "
        "Incorporate these randomness factors:"
        "\n1. Varying question length - mix of short and long questions"
        "\n2. Varying complexity - mix of straightforward and complex questions"
        "\n3. Varying topics - cover both common and obscure aspects of {job}"
        "\n4. Varying answer patterns - avoid having the same letter be the correct answer too often"
        "\n5. Varying question types - include definition, scenario-based, comparative, and analytical questions"
        "\n6. Varying option structures - sometimes have very similar options, sometimes clearly different ones"
        "\n7. Varying difficulty levels - easy (25%), medium (50%), and hard (25%)"
        "\n\nInclude a diverse and unpredictable mix covering different aspects of the field. "
        "Each question should have four options labeled A, B, C, and D, and provide the correct answer. "
        "Try to be creative and unpredictable in the topics you cover within the {job} field. "
        "Format each question and answer pair like 'Q: <question> Options: A. <option1>, B. <option2>, C. <option3>, D. <option4>. Answer: <correct option>'."
    )
    
    # Initialize the language model with parameters that encourage randomness
    # Higher temperature (0.9) for more diverse and random responses
    llm = init_llm(0.9, 600)
    
    # Combine the prompt and language model
    chain = prompt | llm
    
    # Invoke the chain with the job data and timestamp to ensure different outputs
    response = chain.invoke({"job": job, "timestamp": timestamp})
    
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
