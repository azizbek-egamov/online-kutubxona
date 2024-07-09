from django.shortcuts import render, HttpResponse
from main.models import Kitob
from rest_framework import generics
from .serializers import KitoblarSerializer
from googletrans import Translator
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *
import wikipedia
tr = Translator()
from main.models import Shortner

import time

def uniqid(prefix='', more_entropy=False):
    m_time = time.time()
    base = '%8x%05x' % (int(m_time), int((m_time - int(m_time)) * 10000000))

    if more_entropy:
        import random
        base += '%.8f' % random.random()

    return prefix + base

# Create your views here.

class APIBooks(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        book = Kitob.objects.all().values()
        return Response({'book': book})
        


class KitoblarViews(generics.ListAPIView):
    queryset = Kitob.objects.all()
    serializer_class = KitoblarSerializer


class kitoblarCreateView(generics.CreateAPIView):
    queryset = Kitob.objects.all()
    serializer_class = KitoblarSerializer


class KitoblarListCreateView(generics.ListCreateAPIView):
    queryset = Kitob.objects.all()
    serializer_class = KitoblarSerializer


class KitoblarDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Kitob.objects.all()
    serializer_class = KitoblarSerializer


class KitoblarUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Kitob.objects.all()
    serializer_class = KitoblarSerializer
    
class BooksApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kitob.objects.all()
    serializer_class = KitoblarSerializer


def TranslatePage(request):
    sl = request.GET.get("sl")
    tl = request.GET.get("tl")
    text = request.GET.get("text")
    if not sl or not tl or not text:
        txt = json.dumps([{"status": "false"}], indent=4)
        return HttpResponse(txt, content_type="application/json")
    else:
        y = tr.translate(text=text, dest=tl)
        r = {"status": "true", "text": y.text}
        txt = json.dumps([r], indent=4)
        return HttpResponse(txt, content_type='application/json')
    
def wikipediaPage(request):
    text = request.GET.get("text")
    lang = request.GET.get("lang")
    try:
        wikipedia.set_lang(f"{lang}")
        info = wikipedia.summary(f"{text}")
    except Exception as e:
        info = False
        
    if not text or not lang or info == False:
        txt = json.dumps([{'status': 'false'}], indent=4)
        return HttpResponse(txt, content_type='application/json')
    else:
        r = {"status": "true", "lang": lang, "text": text, "information": info}
        txt = json.dumps([r], indent=4)
        return HttpResponse(txt, content_type='application/json')
    
def UrlShortnerPage(request):
    url = request.GET.get("url")
    domen = "127.0.0.1:8000"
    if not url:
        txt = json.dumps([{'status': 'false'}], indent=4)
        return HttpResponse(txt, content_type='application/json')
    else:
        if str(url).startswith("https://") or str(url).startswith("http://"):
            if str(url).startswith(f"http://{domen}") == True or str(url).startswith(f"https://{domen}") == True: 
                txt = json.dumps([{'status': 'false'}], indent=4)
                return HttpResponse(txt, content_type='application/json')
            else:

            
                code = uniqid()
                Shortner.objects.create(code=code, url=url)
                r = {"status": "true", "url": f"http://{domen}/sh/{code}"}
                txt = json.dumps([r], indent=4)
                return HttpResponse(txt, content_type='application/json')
        else:
            txt = json.dumps([{'status': 'false'}], indent=4)
            return HttpResponse(txt, content_type='application/json')