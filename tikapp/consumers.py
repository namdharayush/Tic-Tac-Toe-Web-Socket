import json
import urllib.parse
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db import close_old_connections

from asgiref.sync import sync_to_async
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','tik.settings')
django.setup()

from tikapp.models import TicTacToe

class TicTacToeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        close_old_connections()
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        query_string = self.scope['query_string'].decode()
        query_params = urllib.parse.parse_qs(query_string)
        check_txt = query_params.get('q')[0]
        self.room_group_name = "game_" + self.room_code
        try:
            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )
            await self.accept()
            if('join' in check_txt):
                print('Join')
                await self.channel_layer.group_send(
                self.room_group_name, {'type':'check_for_user_connected_or_not','message' : self.room_code}
            )
        except:
            print("Some Problem Occure in conection")
        
        
    async def disconnect(self, code):
        query_string = self.scope['query_string'].decode()
        query_params = urllib.parse.parse_qs(query_string)
        check_txt = query_params.get('q')[0]
        print(check_txt)
        
        if('join' in check_txt):
            try:
                await self.update_model_data(self.room_code)
            except:
                pass
        elif('create' in check_txt):
            await self.delete_model_data(self.room_code)
            await self.channel_layer.group_send(
                self.room_group_name , {'type':'admin_disconnect_message','message':'Admin has closed the connection.'}
            )
            
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        await self.close()
        
    async def receive(self, text_data=None):
        try:
            print("txt data" , text_data)
            await self.channel_layer.group_send(
                self.room_group_name, {"type" : 'game_msg', "data" : json.loads(text_data)}
            )
        except:
            print("some problem occure!")
        
    async def game_msg(self, event):
        txt_data_json = event['data']
        msg = txt_data_json['message']
        button_position = txt_data_json['button_position']
        await self.send(text_data=json.dumps({'message':msg, 'button_position' : button_position}))
        
    async def admin_disconnect_message(self,event):
        await self.send(text_data=json.dumps({'message':event['message'],'admin_disconnected':True}))
        
    async def check_for_user_connected_or_not(self,event):
        data = await self.get_usernames(event['message'])
        create_username = data.create_user + "_" + data.move
        join_move = ''
        if(data.move == 'X'):
            join_move = "O"
        else:
            join_move = "X"
        join_username = data.join_user + "_" + join_move
        await self.send(text_data=json.dumps({'join_user':True,'userc':create_username, 'userj' : join_username}))
    
    
    @sync_to_async
    def get_usernames(self,room_code):
        return TicTacToe.objects.get(room_code = room_code)
                
    @sync_to_async
    def get_model_data(self,room_code):
        return TicTacToe.objects.get(room_code = room_code)
    
    @sync_to_async
    def update_model_data(self,room_code):
        data = TicTacToe.objects.get(room_code = room_code)
        data.total_connection-=1
        data.save()
        return
    
    @sync_to_async
    def delete_model_data(self,room_code):
        print(f"Attempting to delete data for room_code: {room_code}")
        data = TicTacToe.objects.get(room_code=room_code)
        print(f"Found data: {data}")
        data.delete()
        try:
            
            print("Data deleted successfully.")
        except TicTacToe.DoesNotExist:
            print(f"No entry found for room_code: {room_code}")
        except Exception as e:
            print(f"Error occurred while deleting data: {e}")
