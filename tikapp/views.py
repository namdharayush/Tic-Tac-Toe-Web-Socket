from django.shortcuts import render,redirect
from .models import TicTacToe
from django.views.decorators.csrf import csrf_exempt

ROOM_OWNER_MOVE = ''

def Index(request):
    return render(request,'index.html')

def create_or_join_room(request):
    
    return render(request,'create_join.html')

def create_room(request):
    return render(request, 'room.html')

@csrf_exempt
def join_room(request):
    
    error_msg = None
    move = ''
    
    if(request.method == 'POST'):
        room_code = request.POST.get('room_code')
        username = request.POST.get('username')
        try:
            data = TicTacToe.objects.get(room_code=room_code)
            if(data.move == 'O'):
                move = 'X'
            else:
                move = 'O'
            if(data.total_connection>2):
                error_msg = 'This room is full! please join another room.'
            return redirect(f"/game/tic-tac-toe/{room_code}?joinmove={move}&join_user={username}")
                
        except Exception as e:
            error_msg = 'This room is not availabel'
    return render(request, 'join.html', {'error':error_msg})

def tic_tac_toe_room(request,room_code):
    move = ''
    create_username = request.GET.get('user')
    
    current_uri = request.build_absolute_uri()
    if('createmove' in current_uri):
        move = request.GET.get('createmove')
    elif('joinmove' in current_uri):
        
        try:
            set_total_connection = TicTacToe.objects.get(room_code = room_code)
            if(set_total_connection.total_connection == 2):
                # return redirect('/game/join-room')
                pass
            else:
                join_username = request.GET.get('join_user')
                set_total_connection.total_connection = set_total_connection.total_connection + 1
                set_total_connection.join_user = join_username
                set_total_connection.save()
            if(TicTacToe.objects.get(room_code = room_code).move == 'X'):
                move = 'O'
            else:
                move = 'X'
        except:
            return redirect('/game/join-room')
    if(move):
        try:
            TicTacToe.objects.get(room_code = room_code)
        except:
            data = TicTacToe(room_code = room_code, move = move , total_connection = 1,create_user=create_username)
            data.save()
    else:
        return redirect('/game/create-or-join-room')
    return render(request, 'tic_tac_toe.html', {'room_code':room_code,'move':move})