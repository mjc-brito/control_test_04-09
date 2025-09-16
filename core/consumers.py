import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .redis_queue import get_queue, get_first, add_to_queue, remove_from_queue

class FilaConsumer(AsyncWebsocketConsumer):
    group_name = "queue"

    async def connect(self):
        self.user = self.scope["user"]
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # entra na fila ao conectar
        await sync_to_async(add_to_queue)(self.user.username)

        await self.accept()
        await self._send_position()
        await self._broadcast_queue()

    async def receive(self, text_data):
        data = json.loads(text_data or "{}")
        
        if data.get("action") == "refresh":
            await self._send_position()
        elif data.get("action") == "leave":
            await sync_to_async(remove_from_queue)(self.user.username)
            await self._broadcast_queue()
            await self._send_position()

    # envia posição ao próprio cliente
    async def _send_position(self):
        fila = await sync_to_async(get_queue)()
        user = self.user.username
        pos = (fila.index(user) + 1) if user in fila else None
        is_first = (fila[0] == user) if fila and user in fila else False
        await self.send(text_data=json.dumps({"posicao": pos, "is_first": is_first, "fila": fila}))

    async def queue_update(self, event):
        fila = event["fila"]
        user = self.user.username
        pos = (fila.index(user) + 1) if user in fila else None
        is_first = (fila[0] == user) if fila and user in fila else False
        await self.send(text_data=json.dumps({"posicao": pos, "is_first": is_first, "fila": fila}))