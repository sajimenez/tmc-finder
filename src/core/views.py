from django.shortcuts import render

from .forms import LoanForm


def index(request):
    form = LoanForm()
    return render(request, 'core/index.html', {'form': form})


def search(request):
    form = LoanForm(request.GET)
    context = {'form': form}
    if form.is_valid():
        msg = form.find_tmc()
        context.update({'msg': msg})
    return render(request, 'core/index.html', context)
