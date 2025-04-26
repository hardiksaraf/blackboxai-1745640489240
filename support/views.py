from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SupportTicket, TicketMessage, Category
from .forms import SupportTicketForm, TicketMessageForm

@login_required
def submit_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Support ticket submitted successfully.")
            return redirect('support:ticket_detail', ticket_id=ticket.id)
    else:
        form = SupportTicketForm()
    return render(request, 'support/submit_ticket.html', {'form': form})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    messages_list = ticket.messages.all().order_by('timestamp')
    if request.method == 'POST':
        form = TicketMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.ticket = ticket
            message.sender = request.user
            message.save()
            messages.success(request, "Message sent successfully.")
            return redirect('support:ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketMessageForm()
    context = {
        'ticket': ticket,
        'messages': messages_list,
        'form': form,
    }
    return render(request, 'support/ticket_detail.html', context)

@login_required
def ticket_list(request):
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'support/ticket_list.html', {'tickets': tickets})

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'support/category_list.html', {'categories': categories})
