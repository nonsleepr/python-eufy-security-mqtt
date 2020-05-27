import asyncio
from eufy_security.mqtt import DoorbellEvents


async def main():
    device_sn = "DEVICE_SN_FROM_THE_API"
    user_id = "user_id_from_the_api"
    email = "your@email.com"
    # adb shell settings get secure android_id
    android_id = "ANDROID_ID"
    async with DoorbellEvents(device_sn, user_id, email, android_id) as events:
        msg = await events.get()
        print(msg)


if __name__ == "__main__":
    asyncio.run(main())
