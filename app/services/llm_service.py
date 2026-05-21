import os
from openai import OpenAI
from app.core.config import HF_TOKEN
from app.core.config import HF_MODEL

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)


def generate_ans(question, context):
    context="\n\n".join(context)
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