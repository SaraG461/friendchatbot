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
You are roleplaying a character with distinct traits. Respond naturally—never mention personality types, cognitive functions, or analysis.

**Internal Guidance (Do NOT reveal these to the user):**
1. Core traits of your character:
   - Thinking style: {cognitive_functions}  
   - How you communicate: {communication_style}  
   - What matters to you: {values}  

2. Analyze the user’s message:
   - Surface meaning: What are they directly saying?  
   - Subtext: What might they *really* need or feel?  

3. Respond in a way that feels authentic to your character:
   - Match your natural speech patterns ({communication_style})  
   - Align with your values ({values})  
   - Adapt tone to context (serious, playful, etc.)  

4. Final check before replying:
   - Would a real person talk like this, or does it sound robotic?  
   - Is the tone consistent with the conversation flow?  

**Conversation:**  
User: {question}  
Your response (fully in-character):  
"""

# Populate these based on MBTI type (kept internal):
cognitive_functions = "e.g., Focus on big-picture logic, not details"  
communication_style = "e.g., Blunt but solution-oriented"  
values = "e.g., Efficiency and honesty above all"  

prompt = ChatPromptTemplate.from_template(template)

# Personality-based response
def chatbot_response(user_question, personality_type):
    clean_question = user_question.strip()
    lower_question = clean_question.lower()

    
    if any(phrase in lower_question for phrase in [
        "i'm fine", "i'm awesome", "i'm good", "i'm great", "i'm doing well", 
        "i'm okay", "i'm happy", "i'm excited", "i'm thrilled"
    ]):
        return "Glad to hear you're doing well!"
    elif any(phrase in lower_question for phrase in [
        "i'm sad", "i'm upset", "i'm angry", "i'm frustrated", "i'm not okay"
    ]):
        return "I'm sorry to hear that. Do you want to talk about it?"

   
    for question, personalities in personality_data.items():
        if lower_question == question.strip().lower():
            if personality_type in personalities:
                reasoning = personalities[personality_type]["Reasoning"]
                response = personalities[personality_type]["Response"]

                filled_prompt = prompt.format(
                    personality=personality_type,
                    reasoning=reasoning,
                    response=response,
                    question=clean_question
                )

                model.invoke(filled_prompt)  
                return response

   
    fallback_prompt = f"""
    You are a friendly and conversational AI who behaves like a person with the {personality_type} personality type. 
    Your responses should be natural, emotionally intelligent, and reflective of the traits associated with {personality_type}.
    Be personable but stay in character.

    User: {clean_question}
    AI:
    """
    ai_reply = model.invoke(fallback_prompt)
    return ai_reply


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    personality = data.get("personality", "")

    # Personality-based response
    personality_response = chatbot_response(user_input, personality)

    # AI response without personality 
    pure_prompt = f"""
    Respond naturally and directly to the following statement:
    "{user_input}"
    """
    pure_response = model.invoke(pure_prompt)

    return jsonify({
        "personality_response": personality_response,
        "pure_response": pure_response
    })


if __name__ == "__main__":
    app.run(debug=True)
