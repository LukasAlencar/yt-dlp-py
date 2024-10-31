import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
from threading import Thread
import yt_dlp
import re

def browse_location():
    download_folder = filedialog.askdirectory(initialdir=os.path.expanduser("~/Downloads"))
    if download_folder:
        save_path_var.set(download_folder)

def start_download():
    url = url_entry.get()
    save_path = save_path_var.get()

    if not url:
        Messagebox.show_warning("Por favor, insira uma URL do YouTube.", title="Input Error")
        return

    if not os.path.exists(save_path):
        Messagebox.show_warning("O local de salvamento não é válido.", title="Input Error")
        return
    
    download_button.config(state=DISABLED)
    progress_bar["value"] = 0
    Thread(target=download_video, args=(url, save_path)).start()

def download_video(url, save_path):
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'progress_hooks': [on_progress],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        root.after(0, lambda: Messagebox.show_info("O download foi concluído!", title="Sucesso"))
    except Exception as e:
        root.after(0, lambda: Messagebox.show_error(f"Erro ao baixar o vídeo: {e}", title="Erro"))
    finally:
        root.after(0, lambda: download_button.config(state=NORMAL))

def extract_percentage(percentage_str):
    match = re.search(r'\d+\.\d+', percentage_str)  # Captura o valor numérico com casas decimais
    if match:
        return float(match.group())  # Retorna o valor como float
    else:
        return 0.0
    
def on_progress(d):
    if d['status'] == 'downloading':
        percent_complete_str = d.get('_percent_str', '0.0%').replace('%', '').strip()
        try:
            percent_complete = extract_percentage(percent_complete_str)
            progress_bar["value"] = percent_complete
            root.update_idletasks()
        except ValueError:
            progress_bar["value"] = 0

# Configuração da janela principal com tema ttkbootstrap
root = ttk.Window(themename="darkly")  # Escolha entre vários temas disponíveis em ttkbootstrap
root.title("YouTube Downloader")
root.geometry("600x300")
icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
root.wm_iconbitmap(icon_path)

# Variáveis
save_path_var = ttk.StringVar(value=os.path.expanduser("~/Downloads"))

# Layout
ttk.Label(root, text="URL do vídeo do YouTube:").pack(pady=5)
url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=5)

ttk.Label(root, text="Local de salvamento:").pack(pady=5)
ttk.Entry(root, textvariable=save_path_var, width=50).pack(pady=5)
ttk.Button(root, text="Procurar", command=browse_location, bootstyle=PRIMARY).pack(pady=5)

download_button = ttk.Button(root, text="Baixar", command=start_download, bootstyle=SUCCESS)
download_button.pack(pady=10)

# Barra de progresso
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode="determinate", bootstyle=INFO)
progress_bar.pack(pady=10)

# Loop da interface
root.mainloop()
