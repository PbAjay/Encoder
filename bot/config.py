#    Copyright (c) 2021 Danish_00
#    Improved By @Zylern

from decouple import config

try:
    APP_ID = 16008660
    DEV = 1412592290
    OWNER = config("OWNER", "1412592290")
    API_HASH = "a40f901dbfdca8909907caabf840f606"
    BOT_TOKEN = config("BOT_TOKEN", "6449773863:AAGbaqJuEGcJ2cIkk884W7fSrHEKmznph2U")
    ffmpegcode = ["-c:v libx265 -x265-params 'crf=24:bframes=10:psy-rd=1:ref=3:aq-mode=3:aq-strength=0.8:deblock=1,1:profile=main10:level=3.1' -pix_fmt yuv420p10le -preset veryslow -s 1280x720 -metadata 'title=Encoded By D2K' -c:a libopus -b:a 32k -c:s copy -map 0 -ac 2 -ab 32k -vbr 2 -threads 1"]
    THUMBNAIL = "https://telegra.ph/file/711777fbb7317a73c211a.jpg"
except Exception as e:
    print("Environment vars Missing! Exiting App.")
    print(str(e))
    exit(1)
