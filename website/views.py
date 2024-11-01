import random
import spacy
from django.http import HttpResponse

llm = spacy.load("en_core_web_lg")

from django.shortcuts import render, redirect, get_object_or_404

from website.forms import WordForm
from website.models import Word, MorpionJeu


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


def start_pendu(request):
    secret_word = Word.objects.all()[random.randint(0, Word.objects.count() -1)].text
    request.session['guessed_letters'] = []
    request.session['secret_word'] = secret_word
    request.session['tries'] = 10
    request.session['new_word'] =  "_ " * len(secret_word)
    return redirect("play_pendu")

def play_pendu(request):
    secret_word = request.session.get("secret_word")
    guessed_letters = request.session.get("guessed_letters", [])
    tries = request.session.get("tries", 10)
    message = request.session.get("message", "")

    if request.method == "POST":
        letter = request.POST.get("letter")
        if letter in secret_word:
            if letter not in guessed_letters:
                guessed_letters.append(letter)
                request.session['guessed_letters'] = guessed_letters
        else:
            tries -= 1
            request.session['tries'] = tries

        new_word = ""
        for letter in secret_word:
            if letter in guessed_letters:
                new_word += letter
            else:
                new_word += "_ "
        request.session['new_word'] = new_word

        new_word = new_word.replace(" ", "")

        if new_word == secret_word:
            request.session['message'] = "Bravo tu as trouvé le mot !"
        elif tries <= 0:
            request.session['message'] = "Perdu le mot était : " + secret_word

        return redirect("play_pendu")

    return render(request, "pendu/play.html", {
        "new_word": request.session["new_word"],
        "guessed_letters": guessed_letters,
        "tries": tries,
        "message": message
    })

def reset_pendu(request):
    request.session.pop("secret_word", None)
    request.session.pop("guessed_letters", None)
    request.session.pop("tries", None)
    request.session.pop("new_word", None)
    request.session.pop("message", None)
    return redirect("start_pendu")

def start_morpion(request):
    request.session['board'] = [''] * 9
    request.session['player'] = 'X'
    return redirect("play_morpion")



def play_morpion(request):
    board = request.session['board']
    player = request.session['player']

    if request.method == 'POST':
        case_index = int(request.POST.get('case_index'))

        if board[case_index] == '':
            board[case_index] = player
            if player == "X":
                request.session['player'] = "O"
            else:
                request.session['player'] = "X"
            request.session['board'] = board
            return redirect('play_morpion')


    board_with_indices = []


    for i in range(9):
        board_with_indices.append({'index': i, 'value': board[i]})

    board_rows = []


    board_rows.append(board_with_indices[0:3])
    board_rows.append(board_with_indices[3:6])
    board_rows.append(board_with_indices[6:9])

    return render(request, 'morpion/jeu.html', {
        'board_rows': board_rows,
        'player': player,
    })



def reset_morpion(request):
    request.session['board'] = [''] * 9
    request.session['player'] = 'X'
    return redirect('start_morpion')









