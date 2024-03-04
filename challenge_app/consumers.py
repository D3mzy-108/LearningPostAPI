import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async

from website.models import User


class WaitingRoom(AsyncWebsocketConsumer):
    room_name = ''
    challengeConfig = {
        'rounds': 1,
        'questions': 10,
        'quest': {
            'testid': None,
            'title': '',
        },
        'time': 10,
    }
    is_started = False

    async def connect(self):
        # GET CURRENT USER INSTANCE INFORMATION
        query_string = self.scope['query_string'].decode('utf-8')
        params = parse_qs(query_string)

        self.username = params.get('username', [None])[0]

        if not self.username:
            await self.close()
            return

        # GET ROOM DETAILS
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

        # SETUP DEFAULT VARIABLES FOR USER INSTANCE
        await self.send(text_data=json.dumps({
            "type": 'connectionStatus',
            "message": 'Connected to socket',
        }))
        user = await self.get_user(self.username)
        self.connected_user = {
            'profilePhoto': user.profile_photo,
            'displayName': user.first_name,
            'username': user.username,
        }
        await self.request_users_info()

    @database_sync_to_async
    def get_user(self, username):
        return get_object_or_404(User, username=username)

    async def disconnect(self, close_code):
        await self.leave_room()
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json["type"]
        if message_type == 'request_users_info':
            await self.channel_layer.group_send(
                self.room_name, {
                    "type": "request_users_info",
                    "connected_user": self.connected_user,
                })
        elif message_type == 'send_user_list_from_host':
            await self.channel_layer.group_send(
                self.room_name, {
                    "type": "send_user_list_from_host",
                    "user_list": text_data_json['user_list'],
                })
        elif message_type == 'leave_room':
            await self.channel_layer.group_send(
                self.room_name, {
                    "type": "leave_room",
                    "connected_user": self.connected_user,
                })
        elif message_type == 'kick_user':
            await self.channel_layer.group_send(
                self.room_name, {
                    "type": "kick_user",
                    "user": text_data_json['user'],
                })
        elif message_type == 'receive_message':
            await self.channel_layer.group_send(
                self.room_name, {
                    "type": "receive_message",
                    "message": text_data_json["message"],
                    "user": text_data_json['user'],
                })
        elif message_type == 'set_room_config':
            await self.channel_layer.group_send(
                self.room_name, {
                    "type": "set_room_config",
                    "config": text_data_json["config"],
                })

    async def leave_room(self):
        await self.send(text_data=json.dumps({
            "type": "leave_room",
            "connected_user": self.connected_user,
        }))

    async def kick_user(self, event):
        user = event['user']
        await self.send(text_data=json.dumps({
            "type": "kick_user",
            "user": user,
        }))

    async def request_users_info(self):
        await self.send(text_data=json.dumps({
            "type": "request_users_info",
            "connected_user": self.connected_user,
        }))

    async def send_user_list_from_host(self, event):
        await self.send(text_data=json.dumps({
            "type": "send_user_list_from_host",
            "user_list": event['user_list'],
        }))

    async def receive_message(self, event):
        message = event['message']
        displayName = event['user']
        await self.send(text_data=json.dumps({
            "type": "receive_message",
            "message": message,
            "user": displayName,
        }))

    async def set_room_config(self, event):
        config = event['config']
        await self.send(text_data=json.dumps({
            "type": "set_room_config",
            "config": config,
        }))
