from email import message
from email.policy import default
from multiprocessing import context
from unicodedata import name
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from email.errors import MessageError
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Feedback, Profile, Room, Message
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import RegisterUserForm, RoomForm
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage

# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password').lower()

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or passward does not exxists')

    context = {'page': page}
    return render(request, 'liveChat/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    page = 'register'
    form = RegisterUserForm()
    # form = UserCreationForm()


    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        # form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            profile = Profile.objects.create(user=user)
            return redirect('home')
            
        
            
        else:
            messages.error(request, 'Something error happend,Try again!')

    return render(request, 'liveChat/login_register.html', {'form': form})


# @login_required(login_url='login')
def index(request):
    return render(request, 'liveChat/index.html')


@login_required(login_url='login')
def home(request):

    
    q = request.GET.get('q')
    if request.GET.get('q') != None :
        check = (q.isnumeric())
        
        if check == True:
            rooms = Room.objects.filter(Q(id=q))
        else:
            rooms = Room.objects.filter(Q(name__contains=q))
    else:
        q = "nullsaewadfadafad"
        rooms = Room.objects.filter(Q(name__contains=q))



        
    # rooms = Room.objects.filter(password=q).values()
   
    

    room = Room.objects.all()

    context = {'rooms': rooms, 'room': room}

    return render(request, 'liveChat/home.html', context)


@login_required(login_url='login')
def chat(request, id):
    room = Room.objects.get(id=id)
    alRooms = Room.objects.all()

    room_messages = room.message_set.all()

    participents = room.participents.all()

    if request.user in participents or request.user == room.host:
        if request.method == "POST":
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
            room.participents.add(request.user)


    room_password = room.password
    room_id = room.id

    allRooms = []
    for rooms in alRooms:
        
            allRooms.append(rooms)

    



    context = {'room_messages': room_messages, 'participents': participents,
               'room': room, 'room_password': room_password, 'room_id': room_id, 'allRooms':allRooms}
    return render(request, 'liveChat/chat.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    message.delete()
    return redirect('home')


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            
            room.save()
            id = room.id
            room = Room.objects.get(id = id)
            room.participents.add(request.user)

            
            return redirect('home')

    context = {'form': form}
    return render(request, 'liveChat/room_form.html', context)


@login_required(login_url='login')
def joinRoom(request):
    allRooms = Room.objects.all()
    
    context = {'allRooms': allRooms}
    try:
        if request.method == "POST":
            try:
                room_id = request.POST['room_id']
                password = request.POST['roomPassword']

                room = Room.objects.get(id=room_id)
                if room.password == password:
                    room.participents.add(request.user)

                    joinRoom = Room.objects.get(id=id)
                    participents = room.participents.all()
                    context = {'room': room, 'room_id': room_id}

                else:
                    messages.error(request, 'Password incorrect')
                    # return HttpResponse('Password incurrect ')
            except:
                # return  HttpResponse ("<h2> You Successfully joined Room </h2>")
                return redirect(' home')

    except:
        # messages.error(request,"Enter valid ID!")
        return redirect('home')

    return render(request, 'liveChat/joinRoom.html', context)


@login_required(login_url='login')
def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'liveChat/delete.html', {'obj': room})


@login_required(login_url='login')
def profile(request,id):
    user = User.objects.get(id=id)
    name = user.profile.fullName
    email = user.profile.email
    if name == None or name=='':
        name = user.username
    if email == None or email == '':
        email = ''
    dp = user.profile.dp

    if request.user == user.profile.user:
        sameUser = True
    else:
        sameUser=False

    

    context = {'name':name, 'email':email, 'dp':dp, 'sameUser':sameUser }
    return render(request, 'liveChat/profile.html', context)

@login_required(login_url='login')
def edit_profile(request,id):
    user=User.objects.get(id=id)
    context={}
    try:
        if request.method == "POST" and request.FILES['dp']:
            dp = request.FILES['dp']
            fs = FileSystemStorage()
            dp =fs.save(dp.name,dp)

            print(user.profile.fullName)
            user.profile.fullName = request.POST['fullName']
            user.profile.email = request.POST['email']
            user.profile.dp = dp
            user.profile.save()
            
            return redirect('home')
    except:
        messages.error(request,"Profile Picture Required.")


    
    return render(request, 'liveChat/edit_profile.html', context)
    


@login_required(login_url='login')
def games(request):
    context={}
    if request.method == 'POST':

        try:
            number = int(request.POST['number'])
            numberlist = []



            for i in range(0,number+1):
                numberlist.append(i)
            length=(len(numberlist))
            
            context ={'numberlist':numberlist, 'length':length}
        except:
            return redirect('games')
        
    return render(request, 'liveChat/games.html' , context)


@login_required(login_url='login')
def feedback(request):

    if request.method == "POST":
        
        feedb = request.POST['feedb']
        new_feedback = Feedback.objects.create(
                name=request.user,
                feedback=feedb
                
            )
        # return HttpResponse ('Feedback submited')
        messages.error(request,'Feedback Submited.')
    return render(request, 'liveChat/feedback.html')


@login_required(login_url='login')
def devolopers(request):
    return render(request, 'liveChat/devolopers.html')
