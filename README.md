# Random MCQ Generator API

A Flask-based API that generates random multiple-choice questions (MCQs) for various job roles using the Groq LLM API and LangChain.

## Overview

This project provides a simple yet powerful API that generates diverse and randomized multiple-choice questions tailored to specific job roles or fields. The system uses LangChain and the Groq API with the llama-3.3-70b-versatile model to generate high-quality questions with a focus on randomness and variety.

Key features:
- Generates 15 random MCQs per request
- Customizes questions based on job role or field
- Creates a diverse mix of easy, medium, and difficult questions
- Introduces variability through randomized model parameters
- Returns well-formatted JSON for easy integration with frontend applications

## System Architecture

The project consists of three main Python modules:

1. **MCQS.py**: Contains the main `generate()` function that processes requests, creates prompts, and formats responses
2. **llm.py**: Handles the initialization of the language model with randomized parameters
3. **app.py**: Sets up the Flask application and routes

## Prerequisites

- Python 3.8+
- Groq API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/random-mcq-generator.git
   cd random-mcq-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory and add your Groq API key:
   ```
   GROQ_API=your_groq_api_key_here
   ```

## Usage

### Starting the Server

Run the Flask application:

```bash
python app.py
```

The server will start on port 8000 and will accept requests from any origin due to CORS configuration.

### API Endpoint

**Endpoint**: `/generate`  
**Method**: POST  
**Content-Type**: application/json

**Request Body**:
```json
{
  "job": "Software Engineer"
}
```

Replace "Software Engineer" with any job role or field for which you want to generate questions.

**Response Format**:
```json
{
  "mcqs": [
    {
      "question": "What is the time complexity of a binary search algorithm?",
      "options": {
        "A": "O(n)",
        "B": "O(log n)",
        "C": "O(n log n)",
        "D": "O(n²)"
      },
      "answer": "B"
    },
    // ... more questions
  ]
}
```

### Example API Call

Using cURL:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"job":"Data Scientist"}'
```

Using JavaScript:

```javascript
fetch('http://localhost:8000/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    job: 'Data Scientist',
  }),
})
.then(response => response.json())
.then(data => console.log(data))
.catch((error) => console.error('Error:', error));
```

## Technical Details

### Randomization Techniques

The system employs several techniques to ensure questions are random and diverse:

1. **Prompt Engineering**: The prompt explicitly requests random questions and emphasizes diversity.
2. **Temperature Variation**: A base temperature of 0.9 is used with a small random adjustment of ±0.05.
3. **Top-p Sampling**: Set to 0.95 to allow for diverse token selection.
4. **Frequency Penalty**: Set to 0.5 to reduce repetition in the generated text.

### Response Processing

The API processes the LLM's response by:
1. Splitting the text into individual question-answer pairs
2. Extracting the question text, options, and correct answer
3. Formatting the data into a structured JSON response
4. Skipping any malformed questions that don't match the expected format

### Error Handling

The system includes basic error handling to:
- Skip malformed questions rather than failing the entire request
- Ensure each question has exactly four options before including it in the response

## Customization

### Modifying the Number of Questions

To change the number of generated questions, modify the prompt in the `generate()` function in `MCQS.py`:

```python
prompt = ChatPromptTemplate.from_template(
    f"Generate 15 completely random multiple-choice questions..."  # Change 15 to your desired number
)
```

### Adjusting Model Parameters

To modify the randomness parameters, edit the `init_llm()` function in `llm.py`. Possible adjustments include:

- Changing the base temperature (default: 0.9)
- Adjusting the random temperature variation (default: ±0.05)
- Modifying the top_p value (default: 0.95)
- Changing the frequency_penalty (default: 0.5)
- Increasing or decreasing the max_tokens value (default: 600)

## Deployment

### Docker Deployment

1. Create a Dockerfile:
```
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

2. Build and run the Docker container:
```bash
docker build -t mcq-generator .
docker run -p 8000:8000 -e GROQ_API=your_groq_api_key_here mcq-generator
```

### Cloud Deployment

This application is suitable for deployment on platforms like:
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- Azure App Service

Remember to set the environment variable for your Groq API key in your cloud provider's settings.

## Limitations

- The quality and relevance of questions depend on the LLM's understanding of the specified job field
- Generation time depends on Groq API response time
- The system may occasionally produce malformed questions that get filtered out

## Future Improvements

- Add authentication to the API
- Implement caching to reduce API calls
- Add the ability to specify difficulty levels
- Create endpoints for generating specific types of questions
- Add a feedback mechanism to improve question quality over time
- Implement batching for generating larger sets of questions

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- This project uses the Groq API and LangChain library
- Built with Flask for API serving
