from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.
def index(request):
    return render(request, 'index.html')


def handler401(request, *args, **argv):
    return handlerGeneral(request,401)

def handler403(request, *args, **argv):
    return handlerGeneral(request,403)

def handler404(request, *args, **argv):
    return handlerGeneral(request,404)

def handler500(request, *args, **argv):
    return handlerGeneral(request,500)

def handlerGeneral(request,codigo=404):
    templ=str(codigo)+".html"
    response = render(request,templ, {}, context_instance=RequestContext(request))
    response.status_code = codigo
    return response

