from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from polls.forms import Comment
from .models import Question, Choice, Comments
from django.contrib.auth.models import User


class IndexView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'latest_question_list'
    template_name = 'polls/index.html'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    form_class = Comment()
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        print(kwargs['object'])
        context = super().get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(
            question=Question.objects.get(question_text=kwargs['object'])
        )
        context['form'] = Comment()
        return context

    def post(self, request, *args, **kwargs):
        print(self.request.user.id)
        if request.POST.get('comment'):
            self.object = self.get_object()
            new = Comments(
                comments=request.POST.get('comment'),
                question=Question.objects.get(pk=kwargs['pk']),
                userProfile=User.objects.get(pk=self.request.user.id))
            new.save()
            return HttpResponseRedirect(self.request.path_info)
        else:
            question = get_object_or_404(Question, pk=kwargs['pk'])
            try:
                selected_choice = question.choice_set.get(
                    pk=request.POST['choice'])
            except (KeyError, Choice.DoesNotExist):
                return render(request, 'polls/detail.html', {
                    'question': question,
                    'error_message': "You didn't select a choice.",
                })
            else:
                selected_choice.votes += 1
                selected_choice.save()
                return HttpResponseRedirect(reverse(
                    'polls:results', args=(kwargs['pk'],)))


class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
