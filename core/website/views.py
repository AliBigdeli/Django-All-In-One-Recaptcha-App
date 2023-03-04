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
    
    
    

    
    