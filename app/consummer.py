

# topics - websocket Api - javascripts 

import json
from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
import asyncio
from time import sleep
from asgiref.sync import async_to_sync
from .models  import *


class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("webSocket Connected...........",event)
        #channel layer
        print('channel layers',self.channel_layer)  #get defualt channel layer from a project 
        #channel name
        print("channel layer....",self.channel_name)
        
         #group name here
        self.group_name=self.scope['url_route']['kwargs']['groupname'] #urls thaka group name get korta hoba
        
        #add a  channel new or existing group
        async_to_sync(self.channel_layer.group_add)(self.group_name, #group name
                                                    self.channel_name)     
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        print("messages received from client ...........",event)
        print("Message is: ", event['text'])
        print('message type of client ',type(event['text']))
        data =json.loads(event['text'])
        print('date.....',data)
        print("data type of....",type(data))
        print('chat message ',data['msg'])
        #find group
        groups=group.objects.get(name=self.group_name)
        print("group name here..",groups)
        
        #chate a new chate object create 
        chats=chat(
            content = data['msg'],
            group=groups
        )
        chats.save()
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
            'type':'chat.message',
            'message':event['text']
        })
        
    def chat_message(self,event):
        print("Event........",event)
        print("print actual data.....",event['message'])
        self.send({
            "type": "websocket.send",
            "text":event['message'],                 
        })
        # self.send({
        #         "type": "websocket.send",
        #         "text":"sumilon", 
        #     })
           
    def websocket_disconnect(self, event):
        print("webSocket Disconnect...........")
        #channel layer
        print('channel layers',self.channel_layer)  #get defualt channel layer from a project 
        #channel name
        print("channel layer....",self.channel_name)
        #channel group disconnect
        async_to_sync(self.channel_layer.group_discard)(self.group_name, #group name
                                                    self.channel_name)
        raise StopConsumer()
        
class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("webSocket Connected...........",event)
        #channel layer
        print('channel layers',self.channel_layer)  #get defualt channel layer from a project 
        #channel name
        print("channel layer....",self.channel_name)
        
        #group name here
        self.group_name=self.scope['url_route']['kwargs']['groupname']
        print("group name here...",self.group_name)
        
        #add a  channel new or existing group
        await self.channel_layer.group_add(self.group_name, #group name
         self.channel_name)      
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        print("messages received from client ...........",event)
        print("Message is: ", event['text'])
        print('message type of client ',type(event['text']))
        await self.channel_layer.group_send(
            self.send,
            {
            'type':'chat.message',
            'message':event['text']
        })
        
    async def chat_message(self,event):
        print("Event........",event)
        print("print actual data.....",event['message'])
        self.send({
            "type": "websocket.send",
            "text":event['message'],                 
        })
        # self.send({
        #         "type": "websocket.send",
        #         "text":"sumilon", 
        #     })
           
    async def websocket_disconnect(self, event):
        print("webSocket Disconnect...........")
        #channel layer
        print('channel layers',self.channel_layer)  #get defualt channel layer from a project 
        #channel name
        print("channel layer....",self.channel_name)
        #channel group disconnect
        await self.channel_layer.group_discard(self.group_name, #group name
                                                    self.channel_name)
        raise StopConsumer()
                

