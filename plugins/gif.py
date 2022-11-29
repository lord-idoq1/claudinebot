# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

•`{i}invertgif`
  Membuat Gif Terbalik(negative).

•`{i}bwgif`
  Jadikan Gif hitam putih

•`{i}rvgif`
  Balikkan gif

•`{i}vtog`
  Balas Ke Video, Ini akan Membuat Gif
  Video ke Gif

•`{i}gif <query>`
   Kirim video tentang kueri.
"""
import os
import random
import time
from datetime import datetime as dt

from . import HNDLR, LOGS, bash, downloader, get_string, mediainfo, ayra_cmd


@ayra_cmd(pattern="(bw|invert)gif$")
async def igif(e):
    match = e.pattern_match.group(1).strip()
    a = await e.get_reply_message()
    if not (a and a.media):
        return await e.eor("`Reply To gif only`", time=5)
    wut = mediainfo(a.media)
    if "gif" not in wut:
        return await e.eor("`Reply To Gif Only`", time=5)
    xx = await e.eor(get_string("com_1"))
    z = await a.download_media()
    if match == "bw":
        cmd = f'ffmpeg -i "{z}" -vf format=gray ayra.gif -y'
    else:
        cmd = f'ffmpeg -i "{z}" -vf lutyuv="y=negval:u=negval:v=negval" ayra.gif -y'
    try:
        await bash(cmd)
        await e.client.send_file(e.chat_id, "ayra.gif", supports_streaming=True)
        os.remove(z)
        os.remove("ayra.gif")
        await xx.delete()
    except Exception as er:
        LOGS.info(er)


@ayra_cmd(pattern="rvgif$")
async def reverse_gif(event):
    a = await event.get_reply_message()
    if not (a and a.media) and "video" not in mediainfo(a.media):
        return await e.eor("`Balas ke Video saja`", time=5)
    msg = await event.eor(get_string("com_1"))
    file = await a.download_media()
    await bash(f'ffmpeg -i "{file}" -vf reverse -af areverse reversed.mp4 -y')
    await event.respond("- **Video/GIF Terbalik**", file="reversed.mp4")
    await msg.delete()
    os.remove(file)
    os.remove("reversed.mp4")


@ayra_cmd(pattern="gif( (.*)|$)")
async def gifs(ayra):
    get = ayra.pattern_match.group(1).strip()
    xx = random.randint(0, 5)
    n = 0
    if ";" in get:
        try:
            n = int(get.split(";")[-1])
        except IndexError:
            pass
    if not get:
        return await ayra.eor(f"`{HNDLR}gif <query>`")
    m = await ayra.eor(get_string("com_2"))
    gifs = await ayra.client.inline_query("gif", get)
    if not n:
        await gifs[xx].click(
            ayra.chat_id, reply_to=ayra.reply_to_msg_id, silent=True, hide_via=True
        )
    else:
        for x in range(n):
            await gifs[x].click(
                ayra.chat_id, reply_to=ayra.reply_to_msg_id, silent=True, hide_via=True
            )
    await m.delete()


@ayra_cmd(pattern="vtog$")
async def vtogif(e):
    a = await e.get_reply_message()
    if not (a and a.media):
        return await e.eor("`Reply To video only`", time=5)
    wut = mediainfo(a.media)
    if "video" not in wut:
        return await e.eor("`Reply To Video Only`", time=5)
    xx = await e.eor(get_string("com_1"))
    dur = a.media.document.attributes[0].duration
    tt = time.time()
    if int(dur) < 120:
        z = await a.download_media()
        await bash(
            f'ffmpeg -i {z} -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 ayra.gif -y'
        )
    else:
        filename = a.file.name
        if not filename:
            filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
        vid = await downloader(filename, a.media.document, xx, tt, get_string("com_5"))
        z = vid.name
        await bash(
            f'ffmpeg -ss 3 -t 100 -i {z} -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 ayra.gif'
        )

    await e.client.send_file(e.chat_id, "ayra.gif", support_stream=True)
    os.remove(z)
    os.remove("ayra.gif")
    await xx.delete()
