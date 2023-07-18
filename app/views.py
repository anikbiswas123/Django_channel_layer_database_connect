from django.shortcuts import render
from .models import chat,group
# Create your views here.
def index(request,group_name):
    print("group name here......",group_name)
    gp=group.objects.filter(name=group_name).first()
    chats=[]
    if gp:
        chats=chat.objects.filter(group=gp)
    else:
        gp = group(name=group_name)
        gp.save()
    return render(request,'index.html',{'groupname':group_name,'chats':chats})