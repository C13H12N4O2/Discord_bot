import discord
import logging
import os
import youtube_dl
from dotenv import load_dotenv
from datetime import datetime

def get_env_info(token):
    load_dotenv()
    return os.getenv(token)

def print_log(mode, description):
    local_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    if mode == 'info':
        logging.info(f'{local_time} - {description}')
    elif mode == 'warning':
        logging.warning(f'{local_time} - {description}')

def get_embed(title=None, description=None, color=None):
    return discord.Embed(
        title=title,
        description=description,
        color=color
    )

def set_embed(embed, mode, title=None, url=None, icon_url=None, name=None, value=None, inline=True):
    if mode == 'author':
        embed.set_author(
            name=name,
            url=url,
            icon_url=icon_url
        )
    elif mode == 'set_thumbnail':
        embed.set_thumbnail(
            url=url
        )
    elif mode == 'thumbnail':
        print(embed.thumbnail)
    elif mode == 'add_field':
        embed.add_field(
            name=name,
            value=value,
            inline=inline
        )
    elif mode == 'set_image':
        embed.image(url=url)
        
def download_youtube(path, url):
    path = os.path.join(path, f'{os.path.basename(url)}.mp3')
    
    ydl_opts = {
        'format': 'best/best',
        'outtmpl': path
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return path
        
def mkdir(self, path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path
    
def get_file_name(path):
    return os.path.basename(path)

def play_music(path):
    return discord.FFmpegPCMAudio(path)

