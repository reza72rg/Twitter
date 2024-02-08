from django.shortcuts import render
from django.views import View
# Create your views here.



class HomeView(View):
    template_name = 'twitter/home.html'
    def get(self, request, *args, **kwargs):
        return render (request , self.template_name)
        

class Aboutpage(View):
    template_name = 'twitter/about.html'
    def get(self, request, *args, **kwargs):
        return render (request , self.template_name)