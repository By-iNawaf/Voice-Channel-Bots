import discord
import asyncio
import time

# توكنات البوتات
TOKENS = [
    "هنا التوكن", # توكن للبوت 1
    "هنا التوكن", # توكن للبوت 2
    "هنا التوكن", # توكن للبوت 3
    "هنا التوكن", # توكن للبوت 4
    "هنا التوكن",
    "هنا التوكن",
    "هنا التوكن",

]

# إعدادات كل بوت
# guild_id ايدي السيرفر 
# #voice_id ايدي القناة 
# #status حالة البوت #
#  log_channel_id قناة اللوقات خليها وحده
SETTINGS = [
    {"guild_id": 1111111111111111111, "voice_id": 1111111111111111111, "status": "idle", "log_channel_id": 1111111111111111111},
    {"guild_id": 1111111111111111111, "voice_id": 1111111111111111111, "status": "idle", "log_channel_id": 1111111111111111111},
    {"guild_id": 1111111111111111111, "voice_id": 1111111111111111111, "status": "idle", "log_channel_id": 1111111111111111111},
    {"guild_id": 1111111111111111111, "voice_id": 1111111111111111111, "status": "idle", "log_channel_id": 1111111111111111111},
    {"guild_id": 1111111111111111111, "voice_id": 1111111111111111111, "status": "idle", "log_channel_id": 1111111111111111111},
    {"guild_id": 1111111111111111111, "voice_id": 1111111111111111111, "status": "idle", "log_channel_id": 1111111111111111111},

]

# تخزين أوقات التشغيل
start_times = {}

async def run_bot(token, settings):
    intents = discord.Intents.default()
    intents.voice_states = True
    intents.guilds = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is ready.")
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(name=" "))

        guild = client.get_guild(settings["guild_id"])
        voice_channel = guild.get_channel(settings["voice_id"])
        
        if voice_channel:
            try:
                vc = await voice_channel.connect()
                await asyncio.sleep(1)
                await vc.guild.me.edit(deafen=True)
                print(f"{client.user} joined {voice_channel.name} and deafened.")
            except Exception as e:
                print(f"Error connecting to voice: {e}")
        else:
            print(f"Voice channel not found for {client.user}.")

        start_times[client.user.id] = time.time()
        asyncio.create_task(update_log(client, settings["log_channel_id"]))

    async def update_log(client, log_channel_id):
        await client.wait_until_ready()
        channel = client.get_channel(log_channel_id)
        if not channel:
            print(f"Log channel not found for {client.user}")
            return
        
        message = None

        while not client.is_closed():
            embed = discord.Embed(
                title="🔵 حالة البوت",
                description=f"معلومات تشغيل البوت {client.user.name}",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow()
            )

            uptime = time.time() - start_times.get(client.user.id, time.time())
            days = int(uptime // 86400)
            hours = int((uptime % 86400) // 3600)
            minutes = int((uptime % 3600) // 60)
            seconds = int(uptime % 60)

            connected = any(vc.guild.id == settings["guild_id"] for vc in client.voice_clients)
            voice_status = "متصل ✅" if connected else "غير متصل ❌"

            embed.add_field(name="الحالة الصوتية", value=voice_status, inline=False)
            embed.add_field(
                name="مدة التشغيل",
                value=f"{days} يوم - {hours} ساعة - {minutes} دقيقة - {seconds} ثانية",
                inline=False
            )

            embed.set_footer(text="Auto Update Every 30s")

            try:
                if message:
                    await message.edit(embed=embed)
                else:
                    message = await channel.send(embed=embed)
            except Exception as e:
                print(f"Error updating log: {e}")

            await asyncio.sleep(30)

    try:
        await client.start(token)
    except Exception as e:
        print(f"Error starting bot {token[:10]}: {e}")

async def main():
    await asyncio.gather(*[
        run_bot(TOKENS[i], SETTINGS[i])
        for i in range(len(TOKENS))
    ])

asyncio.run(main())
