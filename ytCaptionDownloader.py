import yt_dlp
import os
from sys import argv

# ======== CONFIG ========
url = argv[1]
output_dir = "D:/youtubedownloads"
language_code = "en"
sub_format = "srt"
fixed_caption_name = "caption"  
# ========================

os.makedirs(output_dir, exist_ok=True)

# Step 1: Get video title without downloading
def get_video_title(url):
    ydl_opts_info = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("title", "youtube_caption")


def convert_srt_to_txt_and_cleanup(srt_path, final_txt_name):
    txt_path = os.path.join(os.path.dirname(srt_path), final_txt_name + ".txt")

    with open(srt_path, 'r', encoding='utf-8') as srt_file:
        lines = srt_file.readlines()

    # Clean lines: remove timestamps, numbers, and empty lines
    clean_lines = []
    for line in lines:
        line = line.strip()
        if not line or '-->' in line or line.isdigit():
            continue
        clean_lines.append(line)

    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write('\n'.join(clean_lines))

    os.remove(srt_path)
    print(f"Captions saved to: {txt_path}")
    print(f"Deleted .srt file: {srt_path}")


def extract_and_process_captions(url):
    video_title = get_video_title(url)

    # Sanitize title to be a valid filename
    safe_title = "".join(c for c in video_title if c.isalnum() or c in " -_().").strip()

    # Prepare fixed .srt output
    srt_fixed_name = f"{fixed_caption_name}.{language_code}.{sub_format}"
    srt_fixed_path = os.path.join(output_dir, srt_fixed_name)

    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [language_code],
        'subtitlesformat': sub_format,
        'outtmpl': os.path.join(output_dir, f'{fixed_caption_name}.%(ext)s'),
        'quiet': True,
        'force_overwrites': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print("❌ Failed to download captions:", e)
            return

    if os.path.exists(srt_fixed_path):
        convert_srt_to_txt_and_cleanup(srt_fixed_path, safe_title)
    else:
        print("❌ Captions (.srt) file was not found after download.")


extract_and_process_captions(url)
