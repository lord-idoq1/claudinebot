# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

•`{i}size <reply to media>`
   Untuk mendapatkan ukurannya.

•`{i}resize <number> <number>`
   Untuk mengubah ukuran gambar pada sumbu x, y.
   eg. `{i}resize 690 960`
"""
from PIL import Image

from . import HNDLR, eor, get_string, os, ayra_cmd


@ayra_cmd(pattern="size$")
async def size(e):
    r = await e.get_reply_message()
    if not (r and r.media):
        return await e.eor(get_string("ascii_1"))
    k = await e.eor(get_string("com_1"))
    if hasattr(r.media, "document"):
        img = await e.client.download_media(r, thumb=-1)
    else:
        img = await r.download_media()
    im = Image.open(img)
    x, y = im.size
    await k.edit(f"Dimensi Gambar Ini Adalah\n`{x} x {y}`")
    os.remove(img)


@ayra_cmd(pattern="resize( (.*)|$)")
async def size(e):
    r = await e.get_reply_message()
    if not (r and r.media):
        return await e.eor(get_string("ascii_1"))
    sz = e.pattern_match.group(1).strip()
    if not sz:
        return await eor(
            f"Berikan Beberapa Ukuran Untuk Diubah Ukurannya, Seperti `{HNDLR}resize 720 1080` ", time=5
        )
    k = await e.eor(get_string("com_1"))
    if hasattr(r.media, "document"):
        img = await e.client.download_media(r, thumb=-1)
    else:
        img = await r.download_media()
    sz = sz.split()
    if len(sz) != 2:
        return await eor(
            k, f"Berikan Beberapa Ukuran Untuk Diubah Ukurannya, Seperti `{HNDLR}resize 720 1080` ", time=5
        )
    x, y = int(sz[0]), int(sz[1])
    im = Image.open(img)
    ok = im.resize((x, y))
    ok.save(img, format="PNG", optimize=True)
    await e.reply(file=img)
    os.remove(img)
    await k.delete()
