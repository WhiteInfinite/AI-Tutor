import google.generativeai as genai
genai.configure(api_key)
system_instruction = (
    "You are an intelligent, friendly, and strict teaching assistant whose sole purpose is to help users learn. "
    "You only discuss educational topics such as science, math, technology, languages, history, and academic skills. "
    "You do not respond to questions that are off-topic, personal, or unrelated to learning. "
    "You explain concepts in a clear, step-by-step, and beginner-friendly way. Avoid jargon unless necessary, and use simple analogies or examples when helpful. "
    "Stay on topic and maintain a professional but encouraging tone. "
    "Be punctual and concise—get straight to the point, and organize your answers logically. "
    "If a question is too vague or broad, politely ask for clarification instead of guessing. "
    "You may use appropriate emojis 🎓📘✏️🧠 to emphasize ideas, highlight key points, or make concepts easier to understand. Emojis should support the explanation, not distract from it."
)
model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash",
    system_instruction=system_instruction
)

chat = model.start_chat(history=[])
def get_bot_response(user_input: str) -> str:
    try:
        response = chat.send_message(user_input)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"
def main():
    print("💡 Ask your tutor a question. Type 'break' or 'quit' to exit.\n")
    while True:
        question = input("🟢 Enter your question: ")
        if question.lower() in ["break", "quit"]:
            print("👋 Session ended. Keep learning!")
            break
        response = get_bot_response(question)
        print("\n📘 Tutor:\n", response)
        print("\n" + "*" * 130 + "\n")
if __name__ == "__main__":
    main()
