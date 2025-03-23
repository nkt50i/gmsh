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

st.set_page_config(page_title="📑", layout="wide")

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
    "1. Подключение библиотеки геометрии": "",
    "2. Определение геометрических объектов": "",
    "3. Формирование 3D объектов и операций": "",
    "4. Создание и обработка линий, поверхностей и тел":"",
    "5. Параметры для спирали": "",
    "6. Создание сетки": "",
    "7. Генерация сетки": "",
    "8. Пример файла .geo": "",
}

choice = st.sidebar.radio("Выберите раздел", list(sections.keys()))


if choice == "1. Подключение библиотеки геометрии":
    # 1. Установка фабрики геометрии
    st.write("""##### 1. Подключение библиотеки геометрии""")
    st.write("""
     - Команда `SetFactory("OpenCASCADE");` указывает Gmsh использовать библиотеку OpenCASCADE для построения геометрии. 
    Это необходимо для создания сложных геометрических объектов, таких как окружности и экструзии.
    """)

elif choice == "2. Определение геометрических объектов":

    st.write("""##### 2. Определение геометрических объектов""")
    st.write("""
    В этом разделе создаются базовые геометрические элементы.
    """)

    # Circle(x) = {...}
    st.write("""**Создание окружностей (Circle)**""")
    st.write("""
     - Команда `Circle(x) = {...};` используется для создания окружности. 
    В примере задаются окружности с определёнными координатами центра и радиусом.
    - `Circle(1) = {0, 0, 0, 0.5};` создаёт окружность с центром в начале координат и радиусом 0.5.
    """)

    # Curve Loop(x) = {...}
    st.write("""**Создание кривых и замкнутых контуров (Curve Loop)**""")
    st.write("""
     - Команда `Curve Loop(x) = {...};` объединяет несколько кривых в замкнутый контур, 
    который затем будет использоваться для создания поверхностей.
    - `Curve Loop(1) = {1};` создаёт контур на основе первой окружности.
    """)

    # ThruSections(x) = {...}
    st.write("""**Экструзия через сечения (ThruSections)**""")
    st.write("""
     - Команда `ThruSections(x) = {...};` используется для создания 3D-объектов путём экструзии или вращения. 
    В примере используется экструзия нескольких окружностей, чтобы создать цилиндр.
    """)

    # Ruled ThruSections(x) = {...}
    st.write("""**Правила экструзии (Ruled ThruSections)**""")
    st.write("""
     - Команда `Ruled ThruSections(x) = {...};` указывает, что необходимо экструзировать поверхность, используя определённые кривые.
    """)

    # Translate{...} {...}
    st.write("""**Перемещение объектов (Translate)**""")
    st.write("""
     - Команда `Translate{...} {...};` перемещает геометрический объект в новое положение. 
    Например, команда перемещает экструзированный объект.
    """)

    # Fillet{...}
    st.write("""**Закругление объектов (Fillet)**""")
    st.write("""
     - Команда `Fillet{...};` создаёт закругления на соединении объектов, сглаживая углы.
    """)

elif choice == "3. Формирование 3D объектов и операций":
    st.write("""##### 3. Формирование 3D объектов и операций""")

    # Volume
    st.write("""**Создание объемов (Volume)**""")
    st.write("""
     - Команда `Volume{...};` используется для создания объемных объектов, которые могут быть использованы для дальнейшей генерации сетки.
    """)

    # Rotate{...}
    st.write("""**Поворот объектов (Rotate)**""")
    st.write("""
     - Команда `Rotate{...};` осуществляет поворот объекта в пространстве. Например, можно повернуть поверхность или объем.
    """)

    # Extrude
    st.write("""**Экструзия объектов (Extrude)**""")
    st.write("""
     - Команда `Extrude {...};` используется для создания объемных объектов путём экструзии поверхностей.
    """)

elif choice == "4. Создание и обработка линий, поверхностей и тел":

    st.write("""##### 4. Создание и обработка линий, поверхностей и тел""")

    # Abs(Boundary{...})
    st.write("""**Обработка границ (Abs(Boundary))**""")
    st.write("""
     - Команда `Abs(Boundary{ Volume{v(0)}; });` используется для создания абстрактных границ объемов, что необходимо для сетки и дальнейших расчётов.
    """)

    # Unique(Abs(Boundary{ Surface{f()}; }));
    st.write("""**Создание уникальных поверхностей**""")
    st.write("""
     - Команда `Unique(Abs(Boundary{ Surface{f()}; }));` создаёт уникальные поверхности для дальнейшего использования.
    """)

    # Delete
    st.write("""**Удаление объектов (Delete)**""")
    st.write("""
     - Команда `Delete{ Surface{1000}; };` удаляет геометрические объекты, которые больше не нужны, например, временные или промежуточные.
    """)

elif choice == "5. Параметры для спирали":

    st.write("""##### 5. Параметры для спирали""")

    st.write("""
    В этом разделе создаётся спираль. Цикл For генерирует точки вдоль спирали с использованием параметров радиуса r, высоты h и угла theta.
    """)

    # Цикл For и генерация точек
    st.write("""**Цикл For для спирали**""")
    st.write("""
     - Цикл For генерирует точки на спирали. Например:
    - `Point(1000 + i) = {r * Cos(theta), r * Sin(theta), i * h/npts};` создаёт точку на спирали с координатами.
    """)

    # Spline
    st.write("""**Создание сплайна (Spline)**""")
    st.write("""
     - Команда `Spline(x) = {...};` используется для создания кривой (сплайна), которая проходит через сгенерированные точки.
    """)

    # Wire
    st.write("""**Создание проводника (Wire)**""")
    st.write("""
     - Команда `Wire(x) = {...};` используется для создания проводника, который будет использован в последующих операциях.
    """)

    # Disk
    st.write("""**Создание круг (Disk)**""")
    st.write("""
     - Команда `Disk(x) = {...};` создаёт круг с заданным радиусом, который может быть использован в экструзиях.
    """)

elif choice == "6. Создание сетки":

    st.write("""##### 6. Создание сетки""")

    st.write("""
     - После определения геометрии, необходимо настроить параметры сетки. В этом разделе настраиваются параметры сетки для всех объектов.
    """)

    # Geometry.NumSubEdges
    st.write("""**Количество подребер (Geometry.NumSubEdges)**""")
    st.write("""
     - Параметр `Geometry.NumSubEdges` определяет количество подребер в геометрии, что влияет на детальность сетки.
    """)

    # Mesh.Size
    st.write("""**Размер элементов сетки**""")
    st.write("""
    - `Mesh.MeshSizeFromCurvature` указывает размер сетки в зависимости от кривизны геометрии.
    - `Mesh.MeshSizeMin` и `Mesh.MeshSizeMax` задают минимальные и максимальные размеры элементов сетки.
    """)

elif choice == "7. Генерация сетки":

    # Генерация сетки
    st.write("""##### 7. Генерация сетки""")
    st.write("""
     - После настройки геометрии и сетки, команда `Mesh 2;` создаёт сетку на основе описанных объектов.
    """)

    # Пример команды Mesh
    st.write("""**Команда для генерации сетки (Mesh 2)**""")
    st.write("""
     - Команда `Mesh 2;` запускает процесс генерации сетки для всех объектов, описанных в файле .geo.
    """)

elif choice == "8. Пример файла .geo":

    st.write("""##### 8. Пример файла .geo""")
    geo_code = """
    SetFactory("OpenCASCADE");
    Circle(1) = {0,0,0, 0.5}; Curve Loop(1) = 1;
    Circle(2) = {0.1,0.05,1, 0.1}; Curve Loop(2) = 2;
    Circle(3) = {-0.1,-0.1,2, 0.3}; Curve Loop(3) = 3;
    ThruSections(1) = {1:3};
    Circle(11) = {2+0,0,0, 0.5}; Curve Loop(11) = 11;
    Circle(12) = {2+0.1,0.05,1, 0.1}; Curve Loop(12) = 12;
    Circle(13) = {2-0.1,-0.1,2, 0.3}; Curve Loop(13) = 13;
    Ruled ThruSections(11) = {11:13};
    v() = Translate{4, 0, 0} { Duplicata{ Volume{1}; } };
    f() = Abs(Boundary{ Volume{v(0)}; });
    e() = Unique(Abs(Boundary{ Surface{f()}; }));
    Fillet{v(0)}{e()}{0.1}
    nturns = 1;
    npts = 20;
    r = 1;
    h = 1 * nturns;
    For i In {0 : npts - 1}
    theta = i * 2*Pi*nturns/npts;
    Point(1000 + i) = {r * Cos(theta), r * Sin(theta), i * h/npts};
    EndFor
    Spline(1000) = {1000 : 1000 + npts - 1};
    Wire(1000) = {1000};
    Disk(1000) = {1,0,0, 0.2};
    Rotate {{1, 0, 0}, {0, 0, 0}, Pi/2} { Surface{1000}; }
    Extrude { Surface{1000}; } Using Wire {1000}
    Delete{ Surface{1000}; }
    Geometry.NumSubEdges = 1000;
    Mesh.MeshSizeFromCurvature = 20;
    Mesh.MeshSizeMin = 0.001;
    Mesh.MeshSizeMax = 0.3;
    Mesh 2;

    """
    show_code(geo_code, "python")

    # Загрузка файла примера
    def save_example_file():
        example_file_path = './example.geo'
        with open(example_file_path, 'w') as f:
            f.write(geo_code)
        return example_file_path

    # Кнопка для загрузки и запуска примера
    if st.button("Пример"):
        example_file_path = save_example_file()
        run_gmsh(example_file_path)