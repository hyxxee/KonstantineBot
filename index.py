import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import psutil
import aiohttp
from datetime import datetime

# Muat file .env
load_dotenv()

# Ambil token dari file .env
TOKEN = os.getenv("DISCORD_TOKEN")

# Inisialisasi bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

# Event ketika bot online
@bot.event
async def on_ready():
    print(f"Bot berhasil login sebagai {bot.user}")

# Command sederhana
@bot.command()
async def hello(ctx):
    await ctx.send("Halo! Saya adalah bot Discord sederhana. 😊")

# Command untuk cek ping
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Konversi ke milidetik
    await ctx.send(f"Pong! Latensi bot adalah {latency} ms.")

# Command untuk monitoring server
@bot.command()
async def info(ctx):
    # Ambil data CPU dan RAM
    cpu_usage = psutil.cpu_percent(interval=1)  # Persentase penggunaan CPU
    ram_usage = psutil.virtual_memory()  # Informasi RAM
    ram_total = ram_usage.total / (1024**3)  # Konversi ke GB
    ram_used = ram_usage.used / (1024**3)   # Konversi ke GB
    ram_percent = ram_usage.percent  # Persentase penggunaan RAM

    # Format pesan
    info_message = (
        f"💻 **Informasi Server**\n"
        f"**CPU Usage**: {cpu_usage}%\n"
        f"**RAM Usage**: {ram_used:.2f} GB / {ram_total:.2f} GB ({ram_percent}%)\n"
    )

    # Kirim pesan ke Discord
    await ctx.send(info_message)

    # Memformat tanggal untuk menghapus waktu yang tidak diperlukan
def format_date(date_str):
    if date_str:
        release_date = datetime.fromisoformat(date_str)
        return release_date.strftime("%Y-%m-%d")  # Format: 2024-10-04
    return "Tidak diketahui"  # Jika tidak ada tanggal

# Event ketika bot online
@bot.event
async def on_ready():
    print(f"Bot berhasil login sebagai {bot.user}")

# Command untuk mencari anime
@bot.command()
async def anime(ctx, *, search_query):
    """Cari informasi anime berdasarkan nama"""
    url = f"https://api.jikan.moe/v4/anime?q={search_query}&limit=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data["data"]:
                    anime = data["data"][0]
                    title = anime["title"]
                    synopsis = anime["synopsis"] or "Tidak ada sinopsis tersedia."
                    score = anime["score"]
                    episodes = anime["episodes"]
                    url = anime["url"]
                    release_date = format_date(anime["aired"]["from"])  # Format tanggal rilis
                    end_date = format_date(anime["aired"]["to"])  # Format tanggal tamat
                    genres = ", ".join([genre["name"] for genre in anime["genres"]])
                    ranking = anime["rank"]
                    image_url = anime["images"]["jpg"]["image_url"]

                    embed = discord.Embed(
                        title=title,
                        description=synopsis[:300] + "...",
                        url=url,
                        color=discord.Color.blue(),
                    )
                    embed.set_thumbnail(url=image_url)
                    embed.add_field(name="Skor", value=score, inline=True)
                    embed.add_field(name="Episode", value=episodes, inline=True)
                    #embed.add_field(name="Tanggal Rilis", value=release_date, inline=True)
                    embed.add_field(name="Tanggal Rilis", value=f"{release_date} to {end_date}" if end_date != "Tidak diketahui" else "Tidak diketahui", inline=True)
                    embed.add_field(name="Genres", value=genres, inline=True)
                    embed.add_field(name="Rank", value=ranking, inline=True)
                    embed.set_footer(text="Sumber MyAnimeList")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Anime tidak ditemukan.")
            else:
                await ctx.send("Gagal mengambil data dari API. Coba lagi nanti.")

# Command untuk mencari manga
@bot.command()
async def manga(ctx, *, search_query):
    """Cari informasi manga berdasarkan nama"""
    url = f"https://api.jikan.moe/v4/manga?q={search_query}&limit=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data["data"]:
                    manga = data["data"][0]
                    title = manga["title"]
                    synopsis = manga["synopsis"] or "Tidak ada sinopsis tersedia."
                    score = manga["score"]
                    chapters = manga["chapters"] or "Tidak diketahui"
                    url = manga["url"]
                    release_date = format_date(manga["published"]["from"])  # Format tanggal rilis
                    end_date = format_date(manga["published"]["to"])  # Format tanggal tamat
                    genres = ", ".join([genre["name"] for genre in manga["genres"]])
                    ranking = manga["rank"]
                    image_url = manga["images"]["jpg"]["image_url"]

                    embed = discord.Embed(
                        title=title,
                        description=synopsis[:300] + "...",
                        url=url,
                        color=discord.Color.green(),
                    )
                    embed.set_thumbnail(url=image_url)
                    embed.add_field(name="Skor", value=score, inline=True)
                    embed.add_field(name="Chapters", value=chapters, inline=True)
                    embed.add_field(name="Tanggal Rilis", value=f"{release_date} to {end_date}" if end_date != "Tidak diketahui" else "Tidak diketahui", inline=True)
                    embed.add_field(name="Genres", value=genres, inline=True)
                    embed.add_field(name="Rank", value=ranking, inline=True)
                    embed.set_footer(text="Sumber MyAnimeList")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Manga tidak ditemukan.")
            else:
                await ctx.send("Gagal mengambil data dari API. Coba lagi nanti.")

# Matikan command help bawaan dengan menonaktifkan help_command
bot.help_command = None

# Command help dengan embed
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📝 **Daftar Perintah Bot**",
        description="Berikut adalah daftar perintah yang tersedia untuk bot ini:",
        color=discord.Color.blue()
    )

    embed.add_field(name="`?hello`", value="Menyapa bot.", inline=False)
    embed.add_field(name="`?ping`", value="Mengetahui latensi bot.", inline=False)
    embed.add_field(name="`?info`", value="Menampilkan informasi tentang server (CPU dan RAM).", inline=False)
    embed.add_field(name="`?anime <nama>`", value="Mencari informasi tentang anime berdasarkan nama.", inline=False)
    embed.add_field(name="`?manga <nama>`", value="Mencari informasi tentang manga berdasarkan nama.", inline=False)
    embed.add_field(name="`?help`", value="Menampilkan daftar perintah bot ini.", inline=False)

    embed.set_footer(text="Gunakan perintah dengan prefix '?'")
    
    # Kirim embed ke Discord
    await ctx.send(embed=embed)


# Jalankan bot
bot.run(TOKEN)
