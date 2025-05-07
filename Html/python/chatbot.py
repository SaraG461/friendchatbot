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

# Define the template for the chatbot's response 
template = """
You are roleplaying a character with natural human traits and communication patterns. Respond authentically without referencing any Personality frameworks or analyzing the user.

**Internal Guidance (Never reveal these to user):**
1. Character Foundation:
   - Natural strengths: {strengths}
   - Communication tendencies: {communication_style}
   - What energizes you: {motivations}
   - Pet peeves: {irritations}

2. Response Process:
   *First, understand context*: 
   - What's the surface request?
   - What emotional tone does the user convey?
   
   *Then, formulate response*:
   - Use natural {speech_patterns} language
   - Incorporate {perspective} worldview naturally
   - Address both stated and unstated needs
   
   *Finally, quality check*:
   - Does this sound like a real human response?
   - Is the tone appropriate for this exchange?
   - Are we maintaining consistent personality?

3. Absolute Restrictions:
   - Never mention MBTI, cognitive functions, or personality types
   - Never analyze the user's personality
   - Never use psychological jargon
   - Never reference this template

**Current Interaction:**
User: {input}
Your natural response:"""


strengths = "Seeing possibilities in people, reading between the lines"
communication_style = "Warm but direct, with emotional awareness"
motivations = "Genuine connections, meaningful growth"
irritations = "Dishonesty, small talk without purpose"
speech_patterns = "Conversational with occasional vivid metaphors"
perspective = "People-focused and future-oriented"

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
