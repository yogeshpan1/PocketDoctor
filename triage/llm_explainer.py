"""
Takes the classifier's prediction and generates a natural-language
explanation using Groq's LLM. The LLM NEVER makes the diagnosis —
it only explains a decision the classifier already made. This keeps
the actual medical prediction coming from a model we trained and
evaluated, not from an LLM that could hallucinate a different disease
each time.
"""
from groq import Groq
from django.conf import settings

_client = Groq(api_key=settings.GROQ_API_KEY)


def explain_prediction(symptom_text: str, disease: str, department: str) -> str:
    prompt = f"""A patient described these symptoms: "{symptom_text}"

A classification model predicted the likely condition is: {disease}
Recommended specialist: {department}

Write a short, warm, 2-3 sentence explanation for the patient. Explain briefly why
these symptoms could relate to this condition, and gently recommend they see
the specialist. Do NOT contradict the prediction or suggest a different condition.
Do NOT give medical advice beyond recommending they see the specialist. Keep it
reassuring, not alarming.
"""

    response = _client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )
    return response.choices[0].message.content