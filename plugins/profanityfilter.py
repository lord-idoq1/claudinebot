# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

•`{i}addprofanity`
   Jika seseorang mengirim kata-kata buruk dalam obrolan, maka bot akan menghapus pesan itu.

•`{i}remprofanity`
   Dari obrolan dari daftar senonoh.

"""

from Ayra.dB.nsfw_db import profan_chat, rem_profan

from . import get_string, ayra_cmd


@ayra_cmd(pattern="addprofanity$", admins_only=True)
async def addp(e):
    profan_chat(e.chat_id, "mute")
    await e.eor(get_string("prof_1"), time=10)


@ayra_cmd(pattern="remprofanity", admins_only=True)
async def remp(e):
    rem_profan(e.chat_id)
    await e.eor(get_string("prof_2"), time=10)
