from flask import Flask, render_template, request, jsonify
from agent.agent import ask_agent
import logging

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()
    user_text = data.get("user_text", "")
    logging.info("User asked: %s", user_text)
    try:
        reply = ask_agent(user_text)
    except Exception as e:
        logging.error("Agent error", exc_info=e)
        reply = "Sorry, something went wrong."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
