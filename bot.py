import discord
from discord.ext import commands
import yt_dlp as youtube_dl

# Enable intents
intents = discord.Intents.default()
intents.message_content = True  # Required for command processing

# Initialize bot with intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Join voice channel
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

# Leave voice channel
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel.")

# Play music
@bot.command()
async def play(ctx, url):
    voice_client = ctx.voice_client
    if not voice_client:
        await ctx.invoke(join)

    voice_client = ctx.voice_client
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
        voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: print(f"Finished playing: {e}"))

    await ctx.send(f"Now playing: {info['title']}")

# Stop music
@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    else:
        await ctx.send("No music is playing.")

# Run the bot
bot.run("MTMzNDUwOTg3MDMwNDU5NjAzMA.G00Ty_.Y18GT8EWkWezDv8a60C1Z3Cc04XZM1ksbn5vDY")
