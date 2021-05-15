from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import Chat, Profile, Attachment

User = get_user_model()


def index(request):
    return render(request, 'chat/index.html', {})


@login_required
@csrf_exempt
def chat_home(request):
    user = User.objects.get(username=request.user.username)
    contacts = Profile.objects.filter(user=user)
    chats = Chat.objects.filter(user=user)

    if request.method == 'GET':
        print(request.body)

    if request.method == "POST":
        data = request.body
        if data:
            sender_id = eval(data)
            sender = User.objects.get(id=sender_id)
            try:
                conversations = Chat.objects.filter(
                Q(sender=sender)| Q(sender=user)
                ).values('sender__username', 'user__username', 'text', 'created'
                ).order_by('created')

                return JsonResponse(list(conversations), safe=False)
            except sender.DoesNotExist:
                return JsonResponse({"Error": 'Error'})
        else:
            return JsonResponse({"Error": "Not Found"})
    return render(request, 'chat/chat_home.html',
                  {
                      'user': user,
                      'chats': chats,
                      'contacts': contacts,
                  }
                  )


@login_required
def save_chat(request):
    if request.method == 'POST':
        text = request.POST.get('message')
        other_user = request.POST.get('recepient')
        try:
            other_user = User.objects.get(id=other_user)
            user = User.objects.get(id=request.user.id)
            chat = Chat(
                user=user,
                sender=other_user,
                text=text,
                )
            chat.save()
            if request.FILES:
                attachment = request.FILES.get('file')
                attachment = Attachment.objects.create(attachment=attachment)
                chat.attachment = attachment
                chat.save()
        except Exception:
            print("Hello this didn't work out as we had thought")
        return JsonResponse({'ok': "Success"})
