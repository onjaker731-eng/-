import threading
from pathlib import Path
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
import yt_dlp

# Папка для збереження файлів у пам'ять Android
DOWNLOAD_DIR = "/sdcard/Download"

class DownloaderApp(App):
    def build(self):
        self.title = "YouTube Downloader"
        
        # Головний вертикальний контейнер
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Візуальний заголовок додатка
        layout.add_widget(Label(text="🎬 YouTube Downloader", font_size=24, size_hint_y=None, height=40))
        
        # Поле для введення посилання
        self.url_input = TextInput(hint_text="Введіть посилання на YouTube...", multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.url_input)
        
        # Вибір формату завантаження
        self.format_spinner = Spinner(
            text='Відео (Найвища якість)',
            values=('Відео (Найвища якість)', 'Аудіо (MP3)'),
            size_hint_y=None, height=50
        )
        layout.add_widget(self.format_spinner)
        
        # Кнопка запуску
        self.btn_download = Button(text="🚀 ЗАВАНТАЖИТИ", background_color=(0, 0.7, 0.3, 1), size_hint_y=None, height=60)
        self.btn_download.bind(on_press=self.start_download_thread)
        layout.add_widget(self.btn_download)
        
        # Текстовий статус для логів
        self.status_label = Label(text="Очікування посилання...", halign="center", valign="middle")
        self.status_label.bind(size=self.status_label.setter('text_size'))
        layout.add_widget(self.status_label)
        
        return layout

    def start_download_thread(self, instance):
        # Запуск в окремому потоці, щоб екран Android не "зависав"
        threading.Thread(target=self.run_downloader, daemon=True).start()

    def update_status(self, text):
        self.status_label.text = text

    def progress_hook(self, d):
        if d.get('status') == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            self.update_status(f"📥 Завантаження: {percent}\nШвидкість: {speed}")
        elif d.get('status') == 'finished':
            self.update_status("✓ Обробка та збереження файлу...")

    def run_downloader(self):
        url = self.url_input.text.strip()
        if not url:
            self.update_status("❌ Помилка: Введіть посилання!")
            return

        self.btn_download.disabled = True
        self.update_status("⏳ Аналіз відео...")

        audio_only = (self.format_spinner.text == 'Аудіо (MP3)')
        ydl_opts = {
            'outtmpl': f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            'progress_hooks': [self.progress_hook],
            'quiet': True,
        }

        if audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            ydl_opts.update({'format': 'best'})

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.update_status("🎉 Успішно завантажено в папку Download!")
        except Exception as e:
            self.update_status(f"❌ Помилка:\n{str(e)}")
        finally:
            self.btn_download.disabled = False

if __name__ == '__main__':
    DownloaderApp().run()
