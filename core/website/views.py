from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView,FormView,CreateView
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
    
    

    
    