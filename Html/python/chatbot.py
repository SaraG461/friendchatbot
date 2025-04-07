from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)
CORS(app) 


with open(r"C:\Users\Sara\Documents\friendchatbot\Html\python\personality.json", "r", encoding="utf-8") as file:

    personality_data = json.load(file)


model = OllamaLLM(model="llama3.2")


template = """
You are an advanced AI that responds based on personality traits using Chain of Thought (CoT) reasoning.
{personality}
{reasoning}
In this scenario, I would likely react this way.
Response: {response}
User Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

def chatbot_response(user_question, personality_type):
    # Check for casual or emotional responses
    user_question = user_question.strip().lower()
    if any(phrase in user_question for phrase in ["i'm fine", "i'm awesome", "i'm good", "i'm great", "i'm doing well", "i'm okay", "i'm happy", "i'm excited", "i'm thrilled"]):
        return "Glad to hear you're doing well"
    elif any(phrase in user_question for phrase in ["i'm sad", "i'm upset", "i'm angry", "i'm frustrated", "i'm not okay"]):
        return "I'm sorry to hear that. Do you want to talk about it?"

    
    for question, personalities in personality_data.items():
        if user_question.strip().lower() == question.strip().lower():
            if personality_type in personalities:
                reasoning = personalities[personality_type]["Reasoning"]
                response = personalities[personality_type]["Response"]
                
                filled_prompt = prompt.format(
                    personality=personality_type,
                    reasoning=reasoning,
                    response=response,
                    question=user_question
                )

                # Send to Ollama
                ai_reply = model.invoke(filled_prompt)
                return response

    # Fallback if no match found
    fallback_prompt = f"""
    You are an advanced AI with the following personality traits: {personality_type}.
    Respond to the following statement with a reply that reflects these traits:
    "{user_question}"
    """
    ai_reply = model.invoke(fallback_prompt)
    return ai_reply



@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    personality = data.get("personality", "")
    response = chatbot_response(user_input, personality)
    return jsonify({"response": response}) 

if __name__ == "__main__":
    app.run(debug=True)
