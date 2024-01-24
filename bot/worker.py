import os
import asyncio
from datetime import datetime as dt
from pathlib import Path
from telethon import Button

async def stats(e, dl, out):
    try:
        dl_path = Path(dl)
        out_path = Path(out)

        if dl_path.exists() and out_path.exists():
            processing_file_name = dl_path.name.replace("_", " ")
            dl_size = hbs(int(dl_path.stat().st_size))
            out_size = hbs(int(out_path.stat().st_size))

            # Calculate estimated time based on your encoding logic
            estimated_time = "YourLogicHere"

            # Calculate encoding percentage
            org_size = int(dl_path.stat().st_size)
            com_size = int(out_path.stat().st_size)
            encoding_percentage = 100 - ((com_size / org_size) * 100)
            encoding_percentage_str = f"{encoding_percentage:.2f}%"

            ans = (
                f"Processing Media:\n{processing_file_name}\n\n"
                f"Downloaded:\n{dl_size}\n\n"
                f"Compressed:\n{out_size}\n\n"
                f"Estimated Time: {estimated_time}\n\n"
                f"Encoding Percentage: {encoding_percentage_str}"
            )

            await e.answer(ans, cache_time=0, alert=True)
        else:
            await e.answer("File not found or processing incomplete.", cache_time=0, alert=True)

    except Exception as er:
        LOGS.info(er)
        await e.answer(
            "Something Went Wrong.\nSend Media Again.", cache_time=0, alert=True
        )

async def process_media(e, dl, out, filename_prefix="video"):
    try:
        dl_path = Path(dl)
        out_path = Path(out)

        if not (dl_path.exists() and dl_path.is_file()):
            return

        processing_file_name = dl_path.name.replace("_", " ")
        rr = "encode"
        bb = f"{filename_prefix}_{dt.now().isoformat('_', 'seconds')}.mkv"
        out = f"{rr}/{bb}"

        # Your encoding logic here
        # ...

        hehe = f"{out};{dl};0"
        wah = code(hehe)

        nn = await e.edit(
            "**🗜 Compressing...**",
            buttons=[
                [Button.inline("STATS", data=f"stats{wah}")],
                [Button.inline("CANCEL", data=f"skip{wah}")],
            ],
        )

        cmd = f"""ffmpeg -i "{dl}" {ffmpegcode[0]} "{out}" -y"""
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        er = stderr.decode()
        try:
            if er:
                await e.edit(str(er) + "\n\n**ERROR**")
                os.remove(dl)
                os.remove(out)
                return
        except BaseException:
            pass

        await upload_and_send(e, out)

    except BaseException as er:
        LOGS.info(er)

async def upload_and_send(e, file_path):
    ttt = time.time()
    nnn = await e.client.send_message(e.chat_id, "**📤 Uploading...**")

    with open(file_path, "rb") as f:
        ok = await upload_file(
            client=e.client,
            file=f,
            name=file_path,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, nnn, ttt, "**📤 Uploading...**")
            ),
        )

    await nnn.delete()
    await send_stats_and_cleanup(e, file_path, ok)

async def send_stats_and_cleanup(e, dl, out):
    org = int(Path(dl).stat().st_size)
    com = int(Path(out).stat().st_size)
    pe = 100 - ((com / org) * 100)
    per = f"{pe:.2f}%"

    a1 = await info(dl, e)
    a2 = await info(out, e)
    dk = (
        f"<b>File Name:</b> {dl}\n\n"
        f"<b>Original File Size:</b> {hbs(org)}\n"
        f"<b>Encoded File Size:</b> {hbs(com)}\n"
        f"<b>Encoded Percentage:</b> {per}\n\n"
        f"<b>Get Mediainfo Here:</b> <a href='{a1}'>Before</a>/<a href='{a2}'>After</a>\n\n"
        f"<i>Downloaded in {ts(int((dt.now() - dt.utcfromtimestamp(org)).seconds) * 1000)}\n"
        f"Encoded in {ts(int((dt.now() - dt.utcfromtimestamp(com)).seconds) * 1000)}\n"
        f"Uploaded in {ts(int((dt.now() - dt.utcfromtimestamp(com)).seconds) * 1000)}</i>"
    )

    ds = await e.client.send_file(
        e.chat_id, file=out, force_document=True, caption=dk, link_preview=False, parse_mode="html"
    )

    await ds.forward_to(-1001790957739)
    await dk.forward_to(-1001790957739)

    os.remove(dl)
    os.remove(out)

async def dl_link(event):
    if not event.is_private:
        return
    link, name = "", ""
    try:
        link = event.text.split()[1]
        name = event.text.split()[2]
    except BaseException:
        pass

    if not link:
        return

    if WORKING or QUEUE:
        QUEUE.update({link: name})
        return await event.reply(f"**✅ Added {link} in QUEUE**")

    WORKING.append(1)
    xxx = await event.reply("**📥 Downloading...**")

    try:
        dl = await fast_download(xxx, link, name)
    except Exception as er:
        WORKING.clear()
        LOGS.info(er)
        return

    await process_media(xxx, dl, "")

async def encod(event):
    try:
        if not event.is_private:
            return

        event.sender

        if not event.media:
            return

        if not event.media.document.mime_type.startswith(("video", "application/octet-stream")):
            return

        if WORKING or QUEUE:
            time.sleep(2)
            xxx = await event.reply("**Adding To Queue...**")
            doc = event.media.document

            if doc.id in list(QUEUE.keys()):
                return await xxx.edit("**This File is Already Added in Queue**")

            name = event.file.name

            if not name:
                name = f"video_{dt.now().isoformat('_', 'seconds')}.mp4"

            QUEUE.update({doc.id: [name, doc]})
            return await xxx.edit("**Added This File in Queue**")

        WORKING.append(1)
        xxx = await event.reply("**📥 Downloading...**")

        s = dt.now()
        ttt = time.time()
        dir = "downloads/"

        if hasattr(event.media, "document"):
            file = event.media.document
            filename = event.file.name

            if not filename:
                filename = f"video_{dt.now().isoformat('_', 'seconds')}.mp4"

            dl = dir + filename

            with open(dl, "wb") as f:
                ok = await download_file(
                    client=event.client,
                    location=file,
                    out=f,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, xxx, ttt, f"**📥 Downloading**\n__{filename}__"),
                    ),
                )
        else:
            dl = await event.client.download_media(
                event.media,
                dir,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, xxx, ttt, f"**📥 Downloading**\n__{filename}__"),
                ),
            )

        await process_media(xxx, dl, "")

    except BaseException as er:
        LOGS.info(er)
        WORKING.clear()
