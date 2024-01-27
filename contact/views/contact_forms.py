from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from contact.forms import ContactForm
from contact.models import ContactModel


@login_required(login_url="contact:login")
def create(request):
    form_action = reverse("contact:create")
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)

        context = {
            "site_title": "Contatos - ",
            "form": form,
            "form_action": form_action,
            "form_title": "Contato",
        }
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect(
                "contact:index",
            )
        return render(request, "contact/pages/create.html", context)
    context = {
        "site_title": "Contatos - ",
        "form": ContactForm(),
        "form_action": form_action,
        "form_title": "Contato",
    }

    return render(request, "contact/pages/create.html", context)


@login_required(login_url="contact:login")
def update(request, contact_id):
    form_action = reverse(
        "contact:update",
        kwargs={
            "contact_id": contact_id,
        },
    )
    contact = get_object_or_404(ContactModel, pk=contact_id, owner=request.user)
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES, instance=contact)
        context = {
            "site_title": "Contatos - ",
            "form": form,
            "form_action": form_action,
            "form_title": "Contato",
        }

        if form.is_valid():
            form.save()
            messages.success(request, "Contato atualizado com sucesso!")
            return redirect(
                "contact:index",
            )
        return render(request, "contact/pages/create.html", context)

    context = {
        "site_title": "Contatos - ",
        "form": ContactForm(instance=contact),
        "form_title": "Contato",
    }

    return render(request, "contact/pages/create.html", context)


@login_required(login_url="contact:login")
def delete(request, contact_id):
    contact = get_object_or_404(ContactModel, pk=contact_id, owner=request.user)

    contact.delete()
    messages.success(request, "Contato removido com sucesso!")
    return redirect("contact:index")
