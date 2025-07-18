# 🎬 YouTube Video & Caption Downloader (Python + yt_dlp)

A Python-based utility to:
- 📥 Download YouTube videos in up to **2K resolution** with audio-video merging
- 📝 Extract **auto-generated or manual subtitles**
- 🔄 Convert `.srt` subtitles into clean `.txt` files (no timestamps)
- 🧹 Automatically clean up intermediate files

> Built for developers, students, and analysts who need content for research, transcription, or offline use.

---

## 🚀 Features

- ✅ Download the **highest quality** video (up to 2K)
- ✅ Downloads best **separate audio and video streams** and merges using FFmpeg
- ✅ Auto-detect and download **auto-generated English subtitles**
- ✅ Convert `.srt` files to clean `.txt` files using the actual video title
- ✅ Deletes intermediate `.srt` files to keep your workspace clean

---

## 📂 Project Structure

```
yt_downloader/
│
├── ytDownloader.py       # Main script to download videos
├── captionExtractor.py   # Script to extract and convert captions
├── README.md             # This file
└── /downloads            # All videos and caption files are saved here
```

---

## 🔧 Prerequisites

- Python 3.8+
- [`yt_dlp`](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/) installed and accessible in system PATH

Install dependencies:

```bash
pip install yt-dlp
```

---

## 🖥️ How to Use

### 1. 📥 **Download Video up to 2K Resolution**

Run the following command:

```bash
python ytDownloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

✅ This script:
- Selects the **best video and audio streams**
- Merges them using FFmpeg
- Saves to `D:/youtubedownloads`

---

### 2. 📝 **Download & Convert Captions**

Run:

```bash
python captionExtractor.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

✅ This script:
- Downloads English subtitles (including auto-generated ones)
- Saves as `.srt`
- Converts to clean `.txt` file using the YouTube title
- Deletes the `.srt` file to save space

---

## 📁 Output Example

After running the caption extractor, you'll get:

```
D:/youtubedownloads/
├── Realtime DevOps Project using Azure DevOps and GitOps ｜ Beginner to Advanced.mp4
├── Realtime DevOps Project using Azure DevOps and GitOps ｜ Beginner to Advanced.txt
```

---

## ⚠️ Known Limitations

- YouTube videos without auto or manual subtitles will not generate `.txt` output.
- Captions are currently extracted only in English (`en`). You can modify the `language_code` in the script.
- Special characters in titles are sanitized for file safety.

---

## 📌 Customization

To change subtitle language (e.g., Hindi):

```python
language_code = "hi"
```

To change download directory:

```python
output_dir = "D:/your/path"
```

---

## 📚 References

- [`yt_dlp` GitHub](https://github.com/yt-dlp/yt-dlp)
- [`FFmpeg`](https://ffmpeg.org/)
- [YouTube Data API (optional for batch enhancement)](https://developers.google.com/youtube/v3)

---

## 🛡️ License

This project is for **educational and personal use only**. Please ensure compliance with [YouTube’s Terms of Service](https://www.youtube.com/t/terms).

---

## 🙌 Author

**Sujay** — *Data Analyst & Data Scientist*  
Passionate about building tools that bridge automation, education, and accessibility.

---
