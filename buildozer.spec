[app]
title = YT Downloader
package.name = ytdownloader
package.domain = org.vladisx
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Вказуємо мову та обов'язкові бібліотеки для додатка
requirements = python3, kivy, yt_dlp

orientation = portrait
fullscreen = 0

# Запитуємо дозволи на інтернет та роботу з файлами на Android
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
