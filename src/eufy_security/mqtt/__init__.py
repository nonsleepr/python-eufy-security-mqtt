import asyncio

from importlib.resources import path as ir_path

from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1

from .doorbell_pb2 import DeviceSettingMessage


class DoorbellEvents:
    def __init__(self, device_sn, user_id, email, android_id="deadc0dedeadc0de"):
        self._device_sn = device_sn
        self._user_id = user_id
        self._email = email
        self._android_id = android_id

    @property
    def _client_id(self):
        return f"android_EufySecurity_{self._user_id}_{self._android_id}"

    @property
    def _username(self):
        return f"eufy_{self._user_id}"

    @property
    def _password(self):
        return self._email

    @property
    def _topic(self):
        return f"/phone/doorbell/{self._device_sn}/push_message"

    async def __aenter__(self):
        self._cli = MQTTClient(client_id=self._client_id)
        with ir_path("eufy_security.mqtt", "eufy.crt") as crt:
            await self._cli.connect(
                f"mqtts://{self._username}:{self._password}@security-mqtt.eufylife.com:8789",
                cafile=str(crt))
        await self._cli.subscribe([(self._topic, QOS_1)])
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._cli.unsubscribe([self._topic])
        await self._cli.disconnect()
        self._cli = None

    async def get(self):
        if self._cli:
            message = await self._cli.deliver_message()
            packet = message.publish_packet
            data = packet.payload.data
            msg = DeviceSettingMessage.FromString(data)
            return msg
