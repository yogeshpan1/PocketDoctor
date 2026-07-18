from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .predictor import predict_disease


@login_required
def triage_view(request):
    result = None
    if request.method == 'POST':
        symptom_text = request.POST.get('symptoms', '').strip()
        if symptom_text:
            result = predict_disease(symptom_text)
        else:
            messages.error(request, 'Please describe your symptoms.')
    return render(request, 'triage/triage.html', {'result': result})