# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

• `{i}instadl <Instagram Url>`
  `Unduh Media Instagram...`

• `{i}instadata <username>`
  `Dapatkan Data Instagram seseorang atau diri sendiri`

• `{i}instaul <reply video/photo> <caption>`
  `Unggah Media ke Instagram...`

• `{i}igtv <reply video> <caption>`
  `Unggah Media ke Igtv...`

• `{i}reels <reply video> <caption>`
  `Unggah Media ke Instagram reels...`

• Sejajarkan dengan Asisten Anda dengan kueri `instatm`
   Untuk mendapatkan postingan beranda...

• Isi `INSTA_USERNAME` dan `INSTA_PASSWORD`
  sebelum menggunakannya..
"""

import os
from re import compile

from telethon.errors.rpcerrorlist import ChatSendInlineForbiddenError
from telethon.tl.types import (
    DocumentAttributeFilename,
    InputWebDocument,
    MessageMediaWebPage,
    WebPage,
)

from Ayra.fns.helper import numerize
from Ayra.fns.misc import create_instagram_client

from . import (
    LOGS,
    Button,
    asst,
    callback,
    eor,
    get_string,
    in_pattern,
    udB,
    ayra_cmd,
)


@ayra_cmd(pattern="instadl( (.*)|$)")
async def insta_dl(e):
    match = e.pattern_match.group(1).strip()
    replied = await e.get_reply_message()
    tt = await e.eor(get_string("com_1"))
    if match:
        text = match
    elif e.is_reply and "insta" in replied.message:
        text = replied.message
    else:
        return await eor(tt, "Berikan Tautan untuk Mengunduh...")
    CL = await create_instagram_client(e)
    if CL:
        try:
            mpk = CL.media_pk_from_url(text)
            media = CL.media_info(mpk)
            if media.media_type == 1:  # photo
                media = CL.photo_download(mpk)
            elif media.media_type == 2 and media.product_type == "feed":  # video:
                media = CL.video_download(mpk)
            elif media.media_type == 2 and media.product_type == "igtv":  # igtv:
                media = CL.igtv_download(mpk)
            elif (
                media.media_type == 2 and media.product_type == "clips"
            ):  # clips/reels:
                media = CL.clip_download(mpk)
            elif media.media_type == 8:  # Album:
                media = CL.album_download(mpk)
            else:
                LOGS.info(f"Jenis Media yang Tidak Dapat Diprediksi : {mpk}")
                return
            await e.reply(
                f"**• Berhasil Diupload\n• Tautan :** {text}\n",
                file=media,
            )
            await tt.delete()
            if not isinstance(media, list):
                os.remove(media)
            else:
                [os.remove(media) for media in media]
            return
        except Exception as B:
            LOGS.exception(B)
            return await eor(tt, str(B))
    if isinstance(e.media, MessageMediaWebPage) and isinstance(
        e.media.webpage, WebPage
    ):
        if photo := e.media.webpage.photo or e.media.webpage.document:
            await tt.delete()
            return await e.reply(
                f"**Link** :{text}\n\nJika Ini Bukan Hasil yang Diharapkan, Silahkan Isi `INSTA_USERNAME` dan `INSTA_PASSWORD`...",
                file=photo,
            )
    # await eor(tt, "Please Fill Instagram Credential to Use this Command...")


@ayra_cmd(pattern="instadata( (.*)|$)")
async def soon_(e):
    cl = await create_instagram_client(e)
    if not cl:
        return
    match = e.pattern_match.group(1).strip()
    ew = await e.eor(get_string("com_1"))
    if match:
        try:
            iid = cl.user_id_from_username(match)
            data = cl.user_info(iid)
        except Exception as g:
            return await eor(ew, f"**ERROR** : `{g}`")
    else:
        data = cl.account_info()
        data = cl.user_info(data.pk)
    photo = data.profile_pic_url
    unam = f"https://instagram.com/{data.username}"
    msg = f"• **Full Name** : __{data.full_name}__"
    if hasattr(data, "biography") and data.biography:
        msg += f"\n• **Bio** : `{data.biography}`"
    msg += f"\n• **UserName** : [@{data.username}]({unam})"
    msg += f"\n• **Verified** : {data.is_verified}"
    msg += f"\n• **Posts Count** : {numerize(data.media_count)}"
    msg += f"\n• **Followers** : {numerize(data.follower_count)}"
    msg += f"\n• **Following** : {numerize(data.following_count)}"
    msg += f"\n• **Category** : {data.category_name}"
    await e.reply(
        msg,
        file=photo,
        force_document=True,
        attributes=[DocumentAttributeFilename("InstaAyra.jpg")],
    )
    await ew.delete()


@ayra_cmd(pattern="(instaul|reels|igtv)( (.*)|$)")
async def insta_karbon(event):
    cl = await create_instagram_client(event)
    if not cl:
        return
    msg = await event.eor(get_string("com_1"))
    replied = await event.get_reply_message()
    type_ = event.pattern_match.group(1).strip()
    if not (replied and (replied.photo or replied.video)):
        return await event.eor("`Membalas Foto Atau Video...`")
    caption = (
        event.pattern_match.group(2) + "\n\n• By #Ayra"
        or replied.message + "\n\n• By #Ayra"
        or "Upload Telegram Ke Instagram\nBy #Ayra.."
    )
    dle = await replied.download_media()
    title = None
    if replied.photo:
        method = cl.photo_upload
    elif type_ == "instaul":
        method = cl.video_upload
    elif type_ == "igtv":
        method = cl.igtv_upload
        title = caption
    elif type_ == "reels":
        method = cl.clip_upload
    else:
        return await eor(msg, "`Gunakan Dalam Format Yang Tepat...`")
    try:
        if title:
            uri = method(dle, caption=caption, title=title)
        else:
            uri = method(dle, caption=caption)
        os.remove(dle)
    except Exception as er:
        LOGS.exception(er)
        return await msg.edit(str(er))
    if not event.client._bot:
        try:
            que = await event.client.inline_query(
                asst.me.username, f"instp-{uri.code}_{uri.pk}"
            )
            await que[0].click(event.chat_id, reply_to=replied.id)
            await msg.delete()
        except ChatSendInlineForbiddenError:
            pass
        except Exception as er:
            return await msg.edit(str(er))
    await msg.edit(
        f"__Diunggah ke Instagram!__\n~ https://instagram.com/p/{uri.code}",
        buttons=Button.inline("•Menghapus•", f"instd{uri.pk}"),
        link_preview=False,
    )


@in_pattern("instp-(.*)", owner=True)
async def instapl(event):
    match = event.pattern_match.group(1).strip().split("_")
    uri = f"https://instagram.com/p/{match[0]}"
    await event.answer(
        [
            await event.builder.article(
                title="Posting ke Instagram",
                text="**Diunggah di Instagram**",
                buttons=[
                    Button.url("•Lihat•", uri),
                    Button.inline("•Hapus•", f"instd{match[1]}"),
                ],
            )
        ]
    )


@callback(compile("instd(.*)"), owner=True)
async def dele_post(event):
    CL = await create_instagram_client(event)
    if not CL:
        return await event.answer("Isi Kredensial Instagram", alert=True)
    await event.answer("• Menghapus...")
    try:
        CL.media_delete(event.data_match.group(1).decode("utf-8"))
    except Exception as er:
        return await event.edit(f"ERROR: {str(er)}")
    await event.edit("**• Dihapus!**")


@in_pattern(pattern="instatm", owner=True)
async def bhoot_ayaa(event):
    if not udB.get_key("INSTA_SET"):
        return await event.answer(
            [], switch_pm="Isi Kredensial Instagram Terlebih Dahulu.", switch_pm_param="start"
        )
    insta = await create_instagram_client(event)
    posts = insta.get_timeline_feed()
    res = []
    switch_pm = f"Menampilkan {posts['num_results']} Umpan.."
    for rp in posts["feed_items"]:
        try:
            me = rp["media_or_ad"]
            url = me["image_versions2"]["candidates"][1]["url"] + ".jpg"
            text = (
                f"| Pencarian Inline Instagram |\n~ https://instagram.com/p/{me['code']}"
            )
            file = InputWebDocument(url, 0, "image/jpeg", [])
            res.append(
                await event.builder.article(
                    title="Instagram",
                    type="photo",
                    content=file,
                    thumb=file,
                    text=text,
                    include_media=True,
                )
            )
        except Exception as er:
            LOGS.exception(er)
    await event.answer(res, gallery=True, switch_pm=switch_pm, switch_pm_param="start")
