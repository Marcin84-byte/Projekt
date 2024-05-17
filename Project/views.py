from django.contrib.auth.forms import AuthenticationForm
from blog.models import BlogPost
from .forms import ContactForm, CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, get_user_model, logout

User = get_user_model()


def home_page(request):
    latest_post = BlogPost.objects.all()[:3]
    context = {'blog_list': latest_post}
    return render(request, "home.html", context)


def blogs_page(request):
    all_post = BlogPost.objects.all()
    context = {'blog_list': all_post}
    return render(request, "list_blog.html", context)


def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form = ContactForm()
            messages.success(request, 'Twoje zapytanie zostało przesłane')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'form.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Pomyślnie zalogowano!')
        return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Konto utworzono pomyślnie')
            return redirect('register')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
