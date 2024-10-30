import random
import spacy
from django.http import HttpResponse

llm = spacy.load("en_core_web_lg")

from django.shortcuts import render, redirect

from website.forms import WordForm
from website.models import Word


# Create your views here.
def index(request):
    return render(request, 'website/index.html')

def add_word(request):
    words = Word.objects.all()

    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_word")
    else:
        form = WordForm()

    return render(request, "cemantox/add_word.html", {"form": form, "words": words})


def start_cemantox(request):
    secret_word = Word.objects.all()[random.randint(0, Word.objects.count() -1)].text
    request.session['secret_word'] = secret_word
    request.session['guessed_words'] = []
    return redirect("play_cemantox")


def play_cemantox(request):
    secret_word = request.session.get("secret_word")
    guessed_words = request.session.get("guessed_words", [])

    if request.method == "POST":
        given_word = request.POST.get("word")
        token_secret = llm(secret_word)
        token_given = llm(given_word)
        similarity = token_secret.similarity(token_given)
        guessed_words.append({"word": given_word, "similarity": round(similarity * 100, 2)})
        request.session["guessed_words"] = guessed_words
        return redirect("play_cemantox")

    return render(request, "cemantox/play.html", {"guessed_words": guessed_words})


def reset_cemantox(request):
    request.session.pop("secret_word", None)
    request.session.pop("guessed_words", None)
    return redirect("start_cemantox")