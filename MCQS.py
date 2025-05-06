from flask import request, jsonify
from langchain_core.prompts import ChatPromptTemplate
from llm import init_llm
import re

def validate_mcq_data(mcq_list):
    """
    Validates the structure of MCQ data.
    Returns (is_valid, reason) tuple.
    """
    if not isinstance(mcq_list, list):
        return False, "Response is not a list"
    
    if len(mcq_list) < 10:  # We expect at least 10 valid questions
        return False, f"Too few valid questions: {len(mcq_list)}"
    
    for item in mcq_list:
        # Check if each item is a dictionary with required keys
        if not isinstance(item, dict):
            return False, "MCQ item is not a dictionary"
        
        required_keys = ["question", "options", "answer"]
        if not all(key in item for key in required_keys):
            return False, f"MCQ item missing required keys: {required_keys}"
        
        # Check options structure
        if not isinstance(item["options"], dict):
            return False, "Options is not a dictionary"
        
        option_keys = ["A", "B", "C", "D"]
        if not all(key in item["options"] for key in option_keys):
            return False, f"Options missing required keys: {option_keys}"
        
        # Check if answer is one of A, B, C, or D
        if item["answer"] not in option_keys:
            return False, f"Invalid answer format: {item['answer']}"
        
        # Check content of questions and options
        if not item["question"] or len(item["question"]) < 5:
            return False, "Question text too short or empty"
            
        for key in option_keys:
            if not item["options"][key] or len(item["options"][key]) < 1:
                return False, f"Option {key} is empty or too short"
    
    return True, "Valid"

def parse_mcqs(content):
    """
    Parse the raw MCQ content from LLM into structured format.
    """
    mcqs_with_answers = content.split("\n\n")
    formatted_response = []
    
    for qa in mcqs_with_answers:
        if not qa.strip():
            continue
            
        try:
            # Handle different possible formats
            if "Answer: " in qa:
                question_part, answer_part = qa.split("Answer: ", 1)
                
                # Extract the answer
                answer = answer_part.strip()
                # Convert answers like "A" or "A. Something" to just "A"
                if answer and answer[0] in "ABCD":
                    answer = answer[0]
                else:
                    # Try to find the letter in the answer text
                    answer_match = re.search(r'[ABCD]', answer)
                    if answer_match:
                        answer = answer_match.group(0)
                    else:
                        continue  # Skip if we can't find a valid answer
                
                # Extract question and options
                if "Options: " in question_part:
                    question_text, options_text = question_part.split("Options: ", 1)
                    question_text = question_text.replace("Q: ", "").strip()
                else:
                    # Try to find the question and options in different format
                    match = re.search(r'(?:Q: |Question: |)\s*(.+?)\s*(?=A\.)', question_part, re.DOTALL)
                    if not match:
                        continue
                    question_text = match.group(1).strip()
                    options_text = question_part[match.end():].strip()
                
                # Parse options
                options = {}
                option_pattern = re.compile(r'([ABCD])\.?\s*([^\n,]+(?:[^\n,]*[^\n,.])?)')
                option_matches = option_pattern.findall(options_text)
                
                if len(option_matches) < 4:
                    continue  # Skip if we don't have enough options
                
                for opt_letter, opt_text in option_matches[:4]:
                    options[opt_letter] = opt_text.strip()
                
                # Ensure we have all required options
                if len(options) == 4 and all(key in options for key in ["A", "B", "C", "D"]):
                    formatted_response.append({
                        "question": question_text,
                        "options": options,
                        "answer": answer
                    })
        except Exception as e:
            continue
    
    return formatted_response

def generate(max_attempts=3):
    """
    Generate MCQs with validation and retry logic.
    """
    data = request.json
    job = data.get("job")
    
    if not job:
        return jsonify({"error": "Job field is required"}), 400
    
    # Create a prompt that emphasizes randomness and proper formatting
    prompt = ChatPromptTemplate.from_template(
        f"Generate 15 completely random multiple-choice questions (MCQs) for a test related to {job}. "
        "Make sure each set of questions is different each time this prompt is run. "
        "Include a diverse and unpredictable mix of easy, medium, and difficult questions covering different aspects of the field. "
        "Format is CRITICAL. For EACH question, use EXACTLY this format:\n\n"
        "Q: [Question text]\n"
        "Options: A. [option1], B. [option2], C. [option3], D. [option4]\n"
        "Answer: [ONE letter A, B, C, or D]\n\n"
        "Ensure there are exactly 4 options (A, B, C, D) for each question, and the answer is ONE of these letters."
    )
    
    llm = init_llm(0.9, 600)
    chain = prompt | llm
    
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        
        try:
            # Invoke the chain with the job data
            response = chain.invoke({"job": job})
            
            # Parse the response
            formatted_response = parse_mcqs(response.content)
            
            # Validate the parsed data
            is_valid, reason = validate_mcq_data(formatted_response)
            
            if is_valid:
                return jsonify({'mcqs': formatted_response}), 200
            else:
                if attempt == max_attempts:
                    # If we've used all attempts and still have some data, return what we have
                    if formatted_response and len(formatted_response) >= 5:
                        return jsonify({'mcqs': formatted_response, 'warning': 'Some questions may be invalid'}), 200
        except Exception as e:
            pass
    
    # If we've reached here, all attempts failed
    return jsonify({
        'error': 'Failed to generate valid MCQs after multiple attempts', 
        'job': job
    }), 500
