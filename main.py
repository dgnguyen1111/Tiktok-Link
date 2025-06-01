import requests
import os
import yt_dlp
import shutil
from colorama import init, Fore, Style

# Khởi tạo colorama
init(autoreset=True)

# Big text ASCII art
BIG_TEXT = [
    "██████╗░░██████╗░███╗░░██╗",
    "██╔══██╗██╔════╝░████╗░██║",
    "██║░░██║██║░░██╗░██╔██╗██║",
    "██║░░██║██║░░╚██╗██║╚████║",
    "██████╔╝╚██████╔╝██║░╚███║",
    "╚═════╝░░╚═════╝░╚═╝░░╚══╝"
]

# Hàm để căn giữa big text
def center_text(lines):
    # Lấy độ rộng của console
    console_width = shutil.get_terminal_size().columns
    centered_lines = []
    for line in lines:
        # Tính số khoảng trắng cần thêm để căn giữa
        padding = (console_width - len(line)) // 2
        centered_line = " " * padding + line
        centered_lines.append(centered_line)
    return centered_lines

# Hàm tải video lên Catbox
def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    if not os.path.isfile(file_path):
        print(f"{Fore.RED}✖ Tệp {file_path} không tồn tại!")
        return None
    
    files = {"fileToUpload": open(file_path, "rb")}
    data = {"reqtype": "fileupload"}
    
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            file_url = response.text
            print(f"{Fore.GREEN}✔ Tải lên Catbox: {os.path.basename(file_path)} - {file_url}")
            return file_url
        else:
            print(f"{Fore.RED}✖ Lỗi tải lên Catbox: {response.status_code}")
            return None
    except Exception as e:
        print(f"{Fore.RED}✖ Lỗi tải lên Catbox: {str(e)}")
        return None
    finally:
        files["fileToUpload"].close()

# Hàm lưu link vào file
def save_link_to_file(link, output_file="link.txt"):
    try:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(link + "\n")
        print(f"{Fore.CYAN}→ Lưu link vào {output_file}")
    except Exception as e:
        print(f"{Fore.RED}✖ Lỗi lưu file: {str(e)}")

# Hàm xóa tệp
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"{Fore.YELLOW}🗑 Xóa tệp: {file_path}")
    except Exception as e:
        print(f"{Fore.RED}✖ Lỗi xóa tệp: {str(e)}")

# Hàm tải video bằng yt-dlp
def download_and_upload_video(tiktok_link, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    ydl_opts = {
        'outtmpl': os.path.join(download_folder, '%(id)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
        'noprogress': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(tiktok_link, download=True)
            video_path = ydl.prepare_filename(info)
            if not video_path.endswith('.mp4'):
                video_path = video_path.rsplit('.', 1)[0] + '.mp4'
            
            if os.path.isfile(video_path):
                print(f"{Fore.GREEN}✔ Tải video: {video_path}")
                catbox_link = upload_to_catbox(video_path)
                if catbox_link:
                    save_link_to_file(catbox_link)
                    delete_file(video_path)
            else:
                print(f"{Fore.RED}✖ Không tìm thấy video!")
    except Exception as e:
        print(f"{Fore.RED}✖ Lỗi tải video: {str(e)}")

def main():
    # Xóa màn hình console để loại bỏ banner Command Prompt
    os.system('cls')
    
    # Căn giữa và hiển thị big text với màu sắc
    centered_big_text = center_text(BIG_TEXT)
    for line in centered_big_text:
        print(f"{Fore.CYAN}{line}")
    print(f"\n{Fore.BLUE}ℹ Tool khởi động - Tải video TikTok và upload lên Catbox\n")
    
    links_file = "tiktok_video_links.txt"
    download_folder = os.path.abspath("downloads")
    
    if not os.path.isfile(links_file):
        print(f"{Fore.RED}✖ File {links_file} không tồn tại!")
        return
    
    with open(links_file, "r", encoding="utf-8") as f:
        tiktok_links = [line.strip() for line in f if line.strip()]
    
    if not tiktok_links:
        print(f"{Fore.RED}✖ Không có link TikTok trong file!")
        return
    
    print(f"{Fore.BLUE}ℹ Tìm thấy {len(tiktok_links)} link TikTok")
    
    for i, link in enumerate(tiktok_links, 1):
        print(f"\n{Fore.MAGENTA}🔄 Link {i}/{len(tiktok_links)}: {link}")
        download_and_upload_video(link, download_folder)

if __name__ == "__main__":
    main()
