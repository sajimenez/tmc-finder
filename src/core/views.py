from django.shortcuts import render
from django.http import JsonResponse

from .forms import LoanForm


def index(request):
    form = LoanForm()
    return render(request, 'core/index.html', {'form': form})


def search(request):
    form = LoanForm(request.GET)
    if form.is_valid():
        msg = form.find_tmc()
        return JsonResponse({'message': msg})
    return JsonResponse(form.errors, status=400)
