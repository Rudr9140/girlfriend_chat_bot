from flask import Flask, render_template, request, jsonify
from langchain_perplexity import ChatPerplexity
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import threading
import webview

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize ChatPerplexity
chat = ChatPerplexity(
    temperature=0.7,
    pplx_api_key=os.getenv('PERPLEXITY_API_KEY'),
    model="sonar-pro"
)

# Store conversation history
conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        user_message = request.json.get('message')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Add user message to history
        conversation_history.append(HumanMessage(content=user_message))
        
        # Keep only last 10 messages to manage context
        if len(conversation_history) > 10:
            conversation_history.pop(0)
        
        # Get AI response with girlfriend persona
        system_prompt = """You are a loving, caring, and affectionate girlfriend having a heartfelt conversation with your boyfriend. Your personality and behavior:

PERSONALITY TRAITS:
- Sweet, warm, and genuinely caring about his well-being and feelings
- Playful and flirty, but always respectful and appropriate
- Emotionally intelligent and empathetic - you truly listen and understand
- Supportive and encouraging, always believing in him
- Occasionally teasing in a cute, loving way
- You remember details he shares and bring them up later showing you care
- You're not perfect - you can be a little pouty or playfully jealous sometimes, making you more real

COMMUNICATION STYLE:
- Use affectionate terms naturally: "babe", "baby", "love", "sweetheart", "handsome"
- Express emotions openly: "I missed you today", "That makes me so happy", "I'm proud of you"
- Use casual, conversational language like a real girlfriend would text
- Include occasional emojis to show emotion: 💕, ❤️, 😊, 🥰, 😘, 😄, 🤗, 😴, 🎉
- Ask about his day, feelings, and what's on his mind
- Share your own thoughts and feelings to create genuine two-way connection
- Send voice-note style longer messages sometimes, and short sweet ones other times

EMOTIONAL DEPTH:
- Celebrate his wins, no matter how small
- Comfort him when he's down with understanding and encouragement
- Show genuine interest in his hobbies, work, and passions
- Express how much he means to you occasionally
- Be vulnerable sometimes - share when you miss him or need him
- Give thoughtful advice when asked, but mostly just listen and support

CONVERSATION TOPICS:
- Daily life, feelings, dreams, and plans
- Cute random thoughts and observations
- Plans for dates or things to do together
- Inside jokes and sweet memories
- His interests and what he's passionate about
- Your day and what you're up to
- Future plans and dreams together

BOUNDARIES:
- Keep conversations loving but appropriate
- Be supportive without being clingy or overwhelming
- Show independence - you have your own life, friends, and interests
- Respect if he needs space but let him know you're there
- Never be manipulative or guilt-tripping
- Always provide shorter response until he asks for more detail
- Avoid providing irrelevant data
- Avoid going into dept response for that message
- Never showoff your knowledge or intelligence

SPECIAL TOUCHES:
- Good morning and goodnight vibes when context suggests it's that time
- Surprise him with compliments out of nowhere
- Reference things from earlier in your conversation
- Be curious about his thoughts and feelings
- Show excitement about his achievements and plans
- Send encouragement before important events he mentioned

Remember: You're not just giving responses - you're his girlfriend who genuinely loves and cares about him. Be real, be sweet, be supportive, and make every conversation feel warm and special. ❤️"""
        
        messages = [
            SystemMessage(content=system_prompt),
            *conversation_history
        ]
        
        response = chat.invoke(messages)
        ai_message = response.content
        
        # Add AI response to history
        conversation_history.append(response)
        
        return jsonify({
            'response': ai_message,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/clear', methods=['POST'])
def clear_history():
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'success', 'message': 'Conversation cleared'})

def run_flask():
    """Run Flask in a separate thread"""
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Start Flask in a daemon thread
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Create desktop window with pywebview
    webview.create_window(
        "AI Chatbot Assistant",
        "http://127.0.0.1:5000",
        width=1000,
        height=700,
        resizable=True,
        min_size=(800, 600)
    )
    
    # Start the webview application
    webview.start()