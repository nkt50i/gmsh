import streamlit as st
from PIL import Image
import base64
import subprocess
import os
import math
import gmsh
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
import plotly.graph_objects as go  # Для 3D-визуализации

st.set_page_config(page_title="💻", layout="wide")

# Функция для отображения кода с возможностью копирования
def show_code(code, language="python"):
    st.code(code, language)

def run_gmsh(file_path):
    try:
        env = os.environ.copy()
        env["LIBGL_ALWAYS_SOFTWARE"] = "1"  # Используем программный рендеринг
        subprocess.run(["gmsh", file_path], check=True, env=env)
        st.success("Gmsh успешно запущен в программном режиме!")
    except FileNotFoundError:
        st.error("Gmsh не найден. Убедитесь, что он установлен и доступен в PATH.")
    except subprocess.CalledProcessError as e:
        st.error(f"Ошибка при запуске Gmsh: {e.returncode}")
        st.text(f"Вывод ошибки:\n{e.stderr}")


st.write("""##### Установка""")

with st.container():
    # Загрузка изображения с локального файла
    image = Image.open("gmsh_logo.jpg")
    
    # Отображение изображения внутри контейнера
    st.image(image, caption="", use_container_width=True) 

st.markdown("""
    <style>
    pre, code {
        background-color: #e6e6e6 !important; /* Светло-серый фон */
        color: #008000 !important; /* Зелёный текст */
        font-weight: normal !important; /* Обычный шрифт */
        padding: 8px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.write("""

- **Linux:**
    1. Используйте команду для установки Gmsh через пакетный менеджер:
        - для Ubuntu/Debian:
            ```bash
            sudo apt-get install gmsh
            ```
        - для Fedora:
            ```bash
            sudo dnf install gmsh
            ```

    2. Для установки последней версии Gmsh можно также скомпилировать из исходников с [официального репозитория Gmsh](http://gmsh.info/). """)

def install_gmsh():
    try:
        # Команда для установки GMSH
        subprocess.run(['sudo', 'apt-get', 'install', 'gmsh', '-y'], check=True)
        return "Gmsh успешно установлен!"
    except subprocess.CalledProcessError:
        return "Произошла ошибка при установке GMSH."

if st.button("Установить Gmsh на Linux"):
    output = install_gmsh()
    st.write(output)

st.write("""
- **macOS:**
    1. Используйте Homebrew для установки Gmsh:
        ```bash
        brew install gmsh
        ```

    2. Альтернативно можно скачать установщик с [официального сайта Gmsh](http://gmsh.info/).
    """)

def install_gmsh_macos():
    try:
        # Команда для установки GMSH через Homebrew
        subprocess.run(['brew', 'install', 'gmsh'], check=True)
        return "Gmsh успешно установлен через Homebrew!"
    except subprocess.CalledProcessError:
        return "Произошла ошибка при установке Gmsh через Homebrew."
    
# Кнопка для установки Gmsh через Homebrew на macOS
if st.button("Установить Gmsh на macOS"):
    output = install_gmsh_macos()
    st.write(output)

st.write("""
- **Windows:**
    1. Перейдите на страницу [с загрузками Gmsh для Windows](http://gmsh.info/).
    2. Скачайте и установите `.exe` файл для вашей системы (обычно это файл с расширением `.exe`).
    3. Следуйте инструкциям мастера установки.
    4. После установки Gmsh будет доступен для использования.

""")

# Кнопка для скачивания Gmsh для Windows
if st.button("Скачать Gmsh для Windows"):
    st.write("Вы можете скачать Gmsh для Windows по [ссылке](http://gmsh.info/#Download).")