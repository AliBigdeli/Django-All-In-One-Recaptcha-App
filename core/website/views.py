from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView,FormView,CreateView
from django.contrib import messages

from .forms import NewsLetterForm
from .models import NewsLetter
# Create your views here.


class UploadView(CreateView):
    template_name = 'website/index.html'
    form_class = NewsLetterForm
    success_url = '/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsletter_list'] = NewsLetter.objects.all()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Thank you for subscribing to this newsletter')
        return super().form_valid(form)

    
    

    
    