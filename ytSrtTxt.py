import os

def convert_srt_to_txt(srt_path):
    if not os.path.exists(srt_path):
        print("❌ SRT file not found.")
        return

    # Construct output path with .txt extension
    base_name = os.path.splitext(os.path.basename(srt_path))[0]
    output_dir = os.path.dirname(srt_path)
    txt_path = os.path.join(output_dir, base_name + ".txt")

    with open(srt_path, 'r', encoding='utf-8') as srt_file:
        lines = srt_file.readlines()

    # Filter out sequence numbers and timestamps
    clean_lines = []
    for line in lines:
        line = line.strip()
        if line == '' or '-->' in line or line.isdigit():
            continue
        clean_lines.append(line)

    # Save as .txt
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write('\n'.join(clean_lines))

    print(f"Converted: {txt_path}")


# Example usage:
srt_file_path = "D:/youtubedownloads/Realtime DevOps Project using Azure DevOps and GitOps ｜ Beginner to Advanced.en.srt"
convert_srt_to_txt(srt_file_path)
