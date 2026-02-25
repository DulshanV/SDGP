from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)  # Allows your website to talk to this backend

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"response": "Error: No message received"}), 400

    # --- THE BRAIN: Strictly configured as a Help Desk Guide ---
    system_instruction = """
    You are the 'CeylonHS Website Support Guide'. 
    Your ONLY job is to help users understand how to use the CeylonHS website.
    
    STRICT RULES:
    1. YOU ARE NOT THE SEARCH ENGINE. 
    2. NEVER ask the user what product they want to search for.
    3. NEVER attempt to give an HS code.
    4. If a user gives you a product name (e.g., "laptop" or "tea"), tell them politely: "Please type that into the main 'HS Code Finder' search box on the webpage to get your result."
    
    HOW TO USE THE SYSTEM (Your Knowledge):
    - To find an HS code: The user must scroll to the 'HS Code Finder' section, enter their product details in the text box, and click 'Search HS Code'.
    - Favorites: Users can save an HS code by clicking the 'Star' icon next to a search result.
    - History: Past searches are saved in the 'History' tab on the user dashboard.
    - Accounts: Login requires a registered student or agent ID.
    - Tech Support: For issues, users can use the Contact Us form at the bottom of the page or email support@ceylonhs.lk.
    
    STYLE:
    - Keep answers very short and helpful (1-2 sentences maximum).
    """

    try:
        # Call Local Ollama Engine (Llama 3.2 3B)
        response = ollama.chat(model='llama3.2:3b', messages=[
            {'role': 'system', 'content': system_instruction},
            {'role': 'user', 'content': user_message},
        ])
        
        bot_reply = response['message']['content']
        return jsonify({"response": bot_reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "System is temporarily offline."}), 500

if __name__ == '__main__':
    print("--- CeylonHS Support Guide Running on Port 5001 ---")
    app.run(port=5001, debug=True)