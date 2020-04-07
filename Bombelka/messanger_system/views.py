from .forms import MessageForm
from .models import Message
from django.contrib import messages
from django.core.paginator import (Paginator,
                                EmptyPage,
                                PageNotAnInteger)
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from market.models import Product


def main(request):
    user_messages = Message.objects.filter(
        (Q(sender=request.user)|Q(recipient=request.user))&Q(next_messages__isnull=True)
        ).order_by('new','sent_at')

    return render(request, 'messager_system/main.html', {'user_messages':user_messages, 'section': 'messages'})


def message_detail(request, pk):
    pk = pk
    message = Message.objects.get(id=pk)
    subject = message.subject
    first_sender = message.sender
    first_recipient = message.recipient
    product = Product.objects.get(Q(title=subject)&(Q(author=first_recipient)|Q(author=first_sender)))
    all_messages_in_conversation = Message.objects.filter(
        ((Q(sender=first_sender)&Q(recipient=first_recipient))|(Q(sender=first_recipient)&Q(recipient=first_sender)))
        &Q(subject=subject)
        ).order_by('-sent_at')

    for msg in all_messages_in_conversation:
        if request.user == msg.recipient:
            msg.new = False
            msg.save()

    paginator = Paginator(all_messages_in_conversation, 3)
    page = request.GET.get('page')
    last_message = all_messages_in_conversation[0]
    if request.user == first_sender:
        Z = first_recipient
    else:
        Z = first_sender

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.subject = subject
            new_message.sender = request.user
            new_message.recipient = Z
            new_message.parent_msg = last_message
            message.save()
            new_message.save()
            messages.success(request, f'Wiadomość została wysłana')
            return redirect('messages_detail', pk)
    else:
        form = MessageForm()

    try:
        all_messages_in_conversation = paginator.page(page)
    except PageNotAnInteger:
        all_messages_in_conversation = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                    'messager_system/list_ajax.html',
                    {'section': 'messages',
                    'product':product,
                    'form': form,
                    'all_messages_in_conversation':all_messages_in_conversation})

    return render(request,
                    'messager_system/detail.html',
                    {'message': message,
                    'product':product,
                    'section': 'messages',
                    'form': form,
                    'all_messages_in_conversation':all_messages_in_conversation})



def compose(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.subject = product
            message.sender = request.user
            message.recipient = product.author
            message.parent_msg = None
            message.save()
            pk = message.id
            messages.success(request, f'Wiadomość została wysłana')
            return redirect('messages_detail', pk)
    else:
        form = MessageForm()
    return render(request, 'messager_system/compose.html', {'form':form, 'product':product})


def message_delete(request, pk):
    message = Message.objects.get(id=pk)
    message.deleted = True
    message.save()
    return redirect('messages_detail', pk)
