# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.


from . import get_help

__doc__ = get_help("help_database")


import re

from . import Redis, eor, get_string, udB, ayra_cmd


@ayra_cmd(pattern="setdb( (.*)|$)", fullsudo=True)
async def _(ayra):
    match = ayra.pattern_match.group(1).strip()
    if not match:
        return await ayra.eor("Berikan kunci dan nilai untuk ditetapkan!")
    try:
        delim = " " if re.search("[|]", match) is None else " | "
        data = match.split(delim, maxsplit=1)
        if data[0] in ["--extend", "-e"]:
            data = data[1].split(maxsplit=1)
            data[1] = f"{str(udB.get_key(data[0]))} {data[1]}"
        udB.set_key(data[0], data[1])
        await ayra.eor(
            f"**Pasangan Nilai Kunci DB Diperbarui\nKunci :** `{data[0]}`\n**Value :** `{data[1]}`"
        )

    except BaseException:
        await ayra.eor(get_string("com_7"))


@ayra_cmd(pattern="deldb( (.*)|$)", fullsudo=True)
async def _(ayra):
    key = ayra.pattern_match.group(1).strip()
    if not key:
        return await ayra.eor("Beri saya nama kunci untuk dihapus!", time=5)
    _ = key.split(maxsplit=1)
    try:
        if _[0] == "-m":
            for key in _[1].split():
                k = udB.del_key(key)
            key = _[1]
        else:
            k = udB.del_key(key)
        if k == 0:
            return await ayra.eor("`Tidak Ada Kunci Seperti Itu.`")
        await ayra.eor(f"`Kunci berhasil dihapus {key}`")
    except BaseException:
        await ayra.eor(get_string("com_7"))


@ayra_cmd(pattern="rendb( (.*)|$)", fullsudo=True)
async def _(ayra):
    match = ayra.pattern_match.group(1).strip()
    if not match:
        return await ayra.eor("`Berikan nama Kunci untuk mengganti nama..`")
    delim = " " if re.search("[|]", match) is None else " | "
    data = match.split(delim)
    if Redis(data[0]):
        try:
            udB.rename(data[0], data[1])
            await eor(
                ult,
                f"**Penggantian Nama Kunci DB Berhasil\nKunci Lama :** `{data[0]}`\n**New Key :** `{data[1]}`",
            )

        except BaseException:
            await ayra.eor(get_string("com_7"))
    else:
        await ayra.eor("Kunci tidak ditemukan")
