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

st.set_page_config(page_title="✏️", layout="wide")

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

sections = {
    "Физические группы": "",
    "Пример 1-D": "",
    "Пример 2-D": "",
    "Пример 3-D":"",
}

choice = st.sidebar.radio("Выберите раздел", list(sections.keys()))


if choice == "Физические группы":
    st.write("""##### Физические группы""")
    st.write(
        """
        **Физические группы (Physical groups)** - именованные наборы геометрических объектов (кривых, поверхностей, объёмов), 
        которые позволяют задавать граничные условия, материалы или другие свойства в численном моделировании.

        """
    )
    st.write("""##### Команды выделения физических групп""")
    st.write( 
        """ 
        Для создания физических групп используются команды `Physical Curve`, `Physical Surfacee`, `Physical Volume`

       **`Physical Curve`**
        Помечает линии (кривые) как физические группы. 
        Используется для задания граничных условий (например, фиксированные края, источники тепла) или интерфейсов между областями.

        **`Physical Surface`**
        Помечает поверхности как физические группы. 
        Используется для задания материалов (например, "Воздух", "Металл") или подобластей с разными свойствами.

        **`Physical Volume`** 
        Помечает объёмы как физические группы. Используется в 3D-моделях для задания материалов или подобластей.
        """
        )

elif choice == "Пример 1-D":
    st.write("""##### Пример 1-D""")
    geo_code_7 = """
            SetFactory("OpenCASCADE");

            // Создаем квадрат
            Rectangle(1) = {0, 0, 0, 1, 1};

            // Физические группы (граничные условия)
            Physical Curve("Fixed_Boundary") = {4}; // Левая грань (линия 4)
            Physical Curve("Heat_Flux") = {2};      // Правая грань (линия 2)
            Physical Surface("Domain") = {1};       // Основная область

            // Генерация сетки
            Mesh.CharacteristicLengthMin = 0.1;

            Geometry.PointNumbers = 1;
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {160, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            Mesh 2;
    
            """
    show_code(geo_code_7,"python")

    def save_example_file():
        example_file_path = './example.geo'
        with open(example_file_path, 'w') as f:
            f.write(geo_code_7)
        return example_file_path

    # Кнопка для загрузки и запуска примера
    if st.button("Пример 1-D"):
        example_file_path = save_example_file()
        run_gmsh(example_file_path)

elif choice == "Пример 2-D":
    st.write("""##### Пример 2-D""")
    
    geo_code_8 = """
                SetFactory("OpenCASCADE");
                // Первый прямоугольник (Материал 1)
                Rectangle(1) = {0, 0, 0, 1, 1, 0};

                // Второй прямоугольник (Материал 2)
                Rectangle(2) = {1, 0, 0, 1, 1, 0};

                // Физические поверхности
                Physical Surface("Air") = {1};
                Physical Surface("Metal") = {2};

                // Общая граница между ними
                Physical Curve("Interface") = {2}; // Линия между прямоугольниками
                // Генерация сетки
                Mesh.CharacteristicLengthMin = 0.1;
                Mesh.CharacteristicLengthMax = 0.1;

                Geometry.PointNumbers = 1;
                Geometry.SurfaceNumbers = 2;
                Geometry.VolumeNumbers = 3;
                Geometry.Color.Points = {160, 255, 0};
                General.Color.Text = White;
                Geometry.Color.Surfaces = Geometry.Color.Points;

                Mesh 2; // Для 2D

                """
    show_code(geo_code_8,"python")

    def save_example_file():
        example_file_path = './example.geo'
        with open(example_file_path, 'w') as f:
            f.write(geo_code_8)
        return example_file_path

    if st.button("Пример 2-D"):
        example_file_path = save_example_file()
        run_gmsh(example_file_path)


elif choice == "Пример 3-D":
    st.write("""##### Пример 3-D""")
    
    geo_code_9 = """
                SetFactory("OpenCASCADE");

                // Создаем сферу (основной объект)
                Sphere(1) = {0, 0, 0, 5};  // Центр (0,0,0), радиус 5

                // Создаем куб (объект, который будет вычтен)
                Box(2) = {-3, -3, -3, 6, 6, 6}; // Центр (0,0,0), размеры 6x6x6

                // Вычитаем куб из сферы
                BooleanDifference(3) = {Volume{1}; Delete;} {Volume{2}; Delete;};

                // Физические группы для визуализации
                Physical Volume("Result") = {3};      // Оставшаяся часть сферы
                Physical Surface("CutBoundary") = {2}; // Граница выреза (бывшие грани куба)

                // Настройки сетки
                Mesh.CharacteristicLengthMin = 1.0;
                Mesh.CharacteristicLengthMax = 1.0;

                Geometry.PointNumbers = 1;
                Geometry.SurfaceNumbers = 2;
                Geometry.VolumeNumbers = 3;
                Geometry.Color.Points = {160, 255, 0};
                General.Color.Text = White;
                Geometry.Color.Surfaces = Geometry.Color.Points;

                // Генерация 3D-сетки
                Mesh 3;

                """
    show_code(geo_code_9,"python")

    def save_example_file():
        example_file_path = './example.geo'
        with open(example_file_path, 'w') as f:
            f.write(geo_code_9)
        return example_file_path

    if st.button("Пример 3-D"):
        example_file_path = save_example_file()
        run_gmsh(example_file_path)    