from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .predictor import predict_disease
from .llm_explainer import explain_prediction


@login_required
def triage_view(request):
    result = None
    explanation = None

    if request.method == 'POST':
        symptom_text = request.POST.get('symptoms', '').strip()

        if symptom_text:
            result = predict_disease(symptom_text)

            try:
                if result['confident']:
                    explanation = explain_prediction(
                        symptom_text, result['disease'], result['department']
                    )
                else:
                    explanation = None
            except Exception:
                explanation = None
                messages.warning(request, 'AI explanation unavailable right now, but here is your result.')
        else:
            messages.error(request, 'Please describe your symptoms.')

    return render(request, 'triage/triage.html', {'result': result, 'explanation': explanation})