from openai import OpenAI
from app.core.config import HF_TOKEN
from app.core.config import HF_MODEL

# Fallback to a dummy key if HF_TOKEN is empty/None to avoid crashing on import
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN or "dummy_key",
)


def generate_ans(question, context):
    # Only join context if it is passed as a list/iterable of strings
    if isinstance(context, list):
        if not context:
            return "I could not find the answer in the document."
        context = "\n\n".join(context)
    if not context:
        return "I could not find the answer in the document."
    context = context[:4000]

    prompt = f"""
     You are an AI research assistant.

     Answer clearly and concisely using ONLY the provided context.

     If the answer is not found in the context,
     say: "I could not find the answer in the document."

     Context:
     {context}

     Question:
       {question}

      Answer:
     """

    try:
        if not HF_TOKEN:
            return "Error: HF_TOKEN is not configured."

        completion = client.chat.completions.create(
            model=HF_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=150,
            temperature=0.3
        )

        answer = completion.choices[0].message.content

        return answer

    except Exception as e:
        return f"Error: {str(e)}"
