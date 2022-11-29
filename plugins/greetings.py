# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

---- Welcomes ----
• `{i}setwelcome <message/reply to message>`
    Tetapkan pesan selamat datang di obrolan saat ini.

• `{i}clearwelcome`
    Hapus sambutan di obrolan saat ini.

• `{i}getwelcome`
    Dapatkan pesan selamat datang di obrolan saat ini.

---- GoodByes ----
• `{i}setgoodbye <message/reply to message>`
    Tetapkan pesan selamat tinggal di obrolan saat ini.

• `{i}cleargoodbye`
    Hapus selamat tinggal di obrolan saat ini.

• `{i}getgoodbye`
    Dapatkan pesan selamat tinggal di obrolan saat ini.

• `{i}thankmembers on/off`
    Kirim stiker terima kasih untuk mencapai jumlah anggota 100*x di grup Anda.
"""
import os

from telegraph import upload_file as uf
from telethon.utils import pack_bot_file_id

from Ayra.dB.greetings_db import (
    add_goodbye,
    add_thanks,
    add_welcome,
    delete_goodbye,
    delete_welcome,
    get_goodbye,
    get_welcome,
    must_thank,
    remove_thanks,
)
from Ayra.fns.tools import create_tl_btn, format_btn, get_msg_button

from . import HNDLR, eor, get_string, mediainfo, ayra_cmd
from ._inline import something

Note = "\n\nNote: `{mention}`, `{group}`, `{count}`, `{name}`, `{fullname}`, `{username}`, `{userid}` can be used as formatting parameters.\n\n"


@ayra_cmd(pattern="setwelcome", groups_only=True)
async def setwel(event):
    x = await event.eor(get_string("com_1"))
    r = await event.get_reply_message()
    btn = format_btn(r.buttons) if (r and r.buttons) else None
    try:
        text = event.text.split(maxsplit=1)[1]
    except IndexError:
        text = r.text if r else None
    if r and r.media:
        wut = mediainfo(r.media)
        if wut.startswith(("pic", "gif")):
            dl = await r.download_media()
            variable = uf(dl)
            os.remove(dl)
            m = f"https://graph.org{variable[0]}"
        elif wut == "video":
            if r.media.document.size > 8 * 1000 * 1000:
                return await eor(x, get_string("com_4"), time=5)
            dl = await r.download_media()
            variable = uf(dl)
            os.remove(dl)
            m = f"https://graph.org{variable[0]}"
        elif wut == "web":
            m = None
        else:
            m = pack_bot_file_id(r.media)
        if r.text:
            txt = r.text
            if not btn:
                txt, btn = get_msg_button(r.text)
            add_welcome(event.chat_id, txt, m, btn)
        else:
            add_welcome(event.chat_id, None, m, btn)
        await eor(x, get_string("grt_1"))
    elif text:
        if not btn:
            txt, btn = get_msg_button(text)
        add_welcome(event.chat_id, txt, None, btn)
        await eor(x, get_string("grt_1"))
    else:
        await eor(x, get_string("grt_3"), time=5)


@ayra_cmd(pattern="clearwelcome$", groups_only=True)
async def clearwel(event):
    if not get_welcome(event.chat_id):
        return await event.eor(get_string("grt_4"), time=5)
    delete_welcome(event.chat_id)
    await event.eor(get_string("grt_5"), time=5)


@ayra_cmd(pattern="getwelcome$", groups_only=True)
async def listwel(event):
    wel = get_welcome(event.chat_id)
    if not wel:
        return await event.eor(get_string("grt_4"), time=5)
    msgg, med = wel["welcome"], wel["media"]
    if wel.get("button"):
        btn = create_tl_btn(wel["button"])
        return await something(event, msgg, med, btn)
    await event.reply(f"**Welcome Note in this chat**\n\n`{msgg}`", file=med)
    await event.delete()


@ayra_cmd(pattern="setgoodbye", groups_only=True)
async def setgb(event):
    x = await event.eor(get_string("com_1"))
    r = await event.get_reply_message()
    btn = format_btn(r.buttons) if (r and r.buttons) else None
    try:
        text = event.text.split(maxsplit=1)[1]
    except IndexError:
        text = r.text if r else None
    if r and r.media:
        wut = mediainfo(r.media)
        if wut.startswith(("pic", "gif")):
            dl = await r.download_media()
            variable = uf(dl)
            os.remove(dl)
            m = f"https://graph.org{variable[0]}"
        elif wut == "video":
            if r.media.document.size > 8 * 1000 * 1000:
                return await eor(x, get_string("com_4"), time=5)
            dl = await r.download_media()
            variable = uf(dl)
            os.remove(dl)
            m = f"https://graph.org{variable[0]}"
        elif wut == "web":
            m = None
        else:
            m = pack_bot_file_id(r.media)
        if r.text:
            txt = r.text
            if not btn:
                txt, btn = get_msg_button(r.text)
            add_goodbye(event.chat_id, txt, m, btn)
        else:
            add_goodbye(event.chat_id, None, m, btn)
        await eor(x, "`Catatan selamat tinggal disimpan`")
    elif text:
        if not btn:
            txt, btn = get_msg_button(text)
        add_goodbye(event.chat_id, txt, None, btn)
        await eor(x, "`Catatan selamat tinggal disimpan`")
    else:
        await eor(x, get_string("grt_7"), time=5)


@ayra_cmd(pattern="cleargoodbye$", groups_only=True)
async def clearwgb(event):
    if not get_goodbye(event.chat_id):
        return await event.eor(get_string("grt_6"), time=5)
    delete_goodbye(event.chat_id)
    await event.eor("`Catatan Selamat Tinggal Dihapus`", time=5)


@ayra_cmd(pattern="getgoodbye$", groups_only=True)
async def listgd(event):
    wel = get_goodbye(event.chat_id)
    if not wel:
        return await event.eor(get_string("grt_6"), time=5)
    msgg = wel["goodbye"]
    med = wel["media"]
    if wel.get("button"):
        btn = create_tl_btn(wel["button"])
        return await something(event, msgg, med, btn)
    await event.reply(f"**Catatan Selamat Tinggal di obrolan ini**\n\n`{msgg}`", file=med)
    await event.delete()


@ayra_cmd(pattern="thankmembers (on|off)", groups_only=True)
async def thank_set(event):
    type_ = event.pattern_match.group(1).strip()
    if not type_ or type_ == "":
        await eor(
            event,
            f"**Pengaturan Obrolan Saat Ini:**\n**Berterima kasih kepada Anggota:** `{must_thank(event.chat_id)}`\n\n Gunakan `{HNDLR}thankmembers on` or `{HNDLR}thankmembers off` untuk beralih pengaturan saat ini!",
        )
        return
    chat = event.chat_id
    if type_.lower() == "on":
        add_thanks(chat)
    elif type_.lower() == "off":
        remove_thanks(chat)
    await eor(
        event,
        f"**Selesai! Terima kasih anggota telah berubah** `{type_.lower()}` **untuk obrolan ini**!",
    )
