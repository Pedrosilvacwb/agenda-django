from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from contact.forms import RegisterForm, RegisterUpdateForm


def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        context = {"site_title": "Usuário - ", "form": form, "form_title": "Usuário"}
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect(
                "contact:index",
            )
        return render(request, "contact/pages/create.html", context)
    context = {
        "site_title": "Usuário - ",
        "form": form,
        "form_title": "Registrar Usuário",
    }

    return render(request, "contact/pages/create.html", context)


@login_required(login_url="contact:login")
def update_user(request):
    form = RegisterUpdateForm(instance=request.user)
    context = {
        "site_title": "Usuário - ",
        "form": form,
        "form_title": "Atualizar Usuário",
    }
    if request.method == "POST":
        form = RegisterUpdateForm(instance=request.user, data=request.POST)
        context["form"] = form
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso")
            return redirect("contact:index")
    return render(request, "contact/pages/create.html", context)


def auth_view(request):
    form = AuthenticationForm(request)
    context = {"form": form}
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, "Usuário logado com sucesso")
            return redirect("contact:index")
        messages.warning(request, "Usuário ou senha invalidos")

    return render(request, "contact/pages/login.html", context)


@login_required(login_url="contact:login")
def logout_view(request):
    auth.logout(request)
    return redirect("contact:login")
