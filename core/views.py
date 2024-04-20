from django.shortcuts import render
from .forms import SearchForm
from .tfidf import Tfidf

tfidf_calculator = Tfidf()

def index(request): 
    if request.method == 'POST':
        form = SearchForm(request.POST)
        form.is_valid()
        search = form.cleaned_data['search']
        tfidf_scores = tfidf_calculator.get_tfidf(search)
        return render(request, 'core/index.html', {
            'tfidf_scores': tfidf_scores,
        })
    elif request.method == 'GET':
        return render(request, 'core/index.html') 