# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

• {i}unsplash <search query> ; <no of pics>
    Hapus Penelusuran Gambar.
"""

from Ayra.fns.misc import unsplashsearch

from . import asyncio, download_file, get_string, os, ayra_cmd


@ayra_cmd(pattern="unsplash( (.*)|$)")
async def searchunsl(ayra):
    match = ayra.pattern_match.group(1).strip()
    if not match:
        return await ayra.eor("Beri aku Sesuatu untuk Dicari")
    num = 5
    if ";" in match:
        num = int(match.split(";")[1])
        match = match.split(";")[0]
    tep = await ayra.eor(get_string("com_1"))
    res = await unsplashsearch(match, limit=num)
    if not res:
        return await ayra.eor(get_string("unspl_1"), time=5)
    CL = [download_file(rp, f"{match}-{e}.png") for e, rp in enumerate(res)]
    imgs = [z for z in (await asyncio.gather(*CL)) if z]
    await ayra.client.send_file(
        ayra.chat_id, imgs, caption=f"Uploaded {len(imgs)} Images!"
    )
    await tep.delete()
    [os.remove(img) for img in imgs]
