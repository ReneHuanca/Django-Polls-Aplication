from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F   # para evitar condiciones de carrera

from .models import Question, Choice

'''
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    # question = get_object_or_404(Question, pk=question_id)   #shortcuts
    jeturn render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    return render(request, 'polls/results.html', {
        'question': get_object_or_404(Question, pk=question_id)    
    })
'''

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes') + 1  # cuando 2 personas al mismo tiempo votan F hace que esto lo maneje la BD, para obtener los datos reales de la BD leer la documentacion
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
