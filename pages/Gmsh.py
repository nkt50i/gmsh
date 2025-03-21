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
    

st.set_page_config(page_title="Руководство по работе с Gmsh", layout="wide")
sections = {
    "Общая характеристика ПО": "",
    "Установка": "",
    "Геометрические элементы": "",
    "Файл геометрии": "",
    "Создание области": "",
    "Интерактивные возможности создания области": "",
    "Составные области": "",
    "Маркирование подобластей и частей границ": "",
    "Генерация сетки": "",
    "Сгущение сетки": "",
    "Подготовка сетки для FEniCS": "",
    "Constructive Solid Geometry технология в Gmsh": "",
    "Библиотеки Python pygmsh и meshio": "",
}

choice = st.sidebar.radio("Выберите раздел", list(sections.keys()))

st.title(choice)
st.write(sections[choice])

if choice == "Общая характеристика ПО":
    
    st.write(
            """
            **Gmsh** — это открытое программное обеспечение для генерации конечных элементов (mesh generation).
            Оно используется в численном моделировании и вычислительной механике, особенно в методе конечных элементов (FEM).
            """
        )
    st.write("""##### Основные возможности Gmsh""")
    st.markdown(
        """
        - Генерация двумерных и трехмерных сеток
        - Поддержка различных типов элементов (треугольники, тетраэдры, гексаэдры и т. д.)
        - Встроенный язык сценариев (Gmsh scripting language)
        - Визуализация и постобработка
        - Импорт и экспорт в различные форматы (STEP, STL, MSH и др.)
        - Поддержка параметризированного моделирования
        """
        )
        
    st.write("""##### Применение Gmsh""")
    st.write(
        """
        Gmsh активно применяется в различных областях инженерии и науки:
        - Аэродинамика
        - Машиностроение
        - Биомеханика
        - Электромагнетизм
        - Геофизика
        """
        )
        
    st.write("""##### Пример кода для создания сетки""")
    code = """
        SetFactory("OpenCASCADE");
        lc = 1e-2;
        Point(1) = {0, 0, 0, lc};
        Point(2) = {.1, 0, 0, lc};
        Point(3) = {.1, .3, 0, lc};
        Point(4) = {0, .3, 0, lc};

        Line(1) = {1, 2};
        Line(2) = {2, 3}; // Обратите внимание на порядок
        Line(3) = {3, 4};
        Line(4) = {4, 1};

        Curve Loop(1) = {4, 1, -2, 3};
        Plane Surface(1) = {1};

        Physical Curve(5) = {1, 2, 4};
        Physical Surface("My surface") = {1};

        
        Rectangle(2) = {0.2, 0.0, 0.0, 0.1, 0.3};
        Geometry.PointNumbers = 1;
        Geometry.Color.Points = {160, 255, 0};
        General.Color.Text = White;
        Geometry.Color.Surfaces = Geometry.Color.Points;


        Mesh 2;
        
    """
    
    st.code(code, language="python")
    
    if st.button("Запустить пример"):
        file_path = "example.geo"
        with open(file_path, "w") as f:
            f.write(code)
        run_gmsh(file_path)
    st.write("""##### Ссылки и ресурсы""")
    st.markdown("[Официальный сайт Gmsh](https://gmsh.info/)")
    st.markdown("[Документация Gmsh](https://gmsh.info/doc/texinfo/gmsh.html)")


elif choice == "Установка":

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
            - Для Ubuntu/Debian:
              ```bash
              sudo apt-get install gmsh
              ```
            - Для Fedora:
              ```bash
              sudo dnf install gmsh
              ```

        2. Для установки последней версии Gmsh можно также скомпилировать из исходников с [официального репозитория Gmsh](http://gmsh.info/).

    - **macOS:**
        1. Используйте Homebrew для установки Gmsh:
            ```bash
            brew install gmsh
            ```

        2. Альтернативно можно скачать установщик с [официального сайта Gmsh](http://gmsh.info/).

    - **Windows:**
        1. Перейдите на страницу [с загрузками Gmsh для Windows](http://gmsh.info/).
        2. Скачайте и установите `.exe` файл для вашей системы (обычно это файл с расширением `.exe`).
        3. Следуйте инструкциям мастера установки.
        4. После установки Gmsh будет доступен для использования.

    """)

    def install_gmsh():
        try:
            # Команда для установки GMSH
            subprocess.run(['sudo', 'apt-get', 'install', 'gmsh', '-y'], check=True)
            return "GMSH успешно установлен!"
        except subprocess.CalledProcessError:
            return "Произошла ошибка при установке GMSH."

    if st.button("Установить GMSH на Linux"):
        output = install_gmsh()
        st.write(output)

    def install_gmsh_macos():
        try:
            # Команда для установки GMSH через Homebrew
            subprocess.run(['brew', 'install', 'gmsh'], check=True)
            return "GMSH успешно установлен через Homebrew!"
        except subprocess.CalledProcessError:
            return "Произошла ошибка при установке GMSH через Homebrew."
    
    # Кнопка для установки Gmsh через Homebrew на macOS
    if st.button("Установить GMSH на macOS"):
        output = install_gmsh_macos()
        st.write(output)

    # Кнопка для скачивания Gmsh для Windows
    if st.button("Скачать Gmsh для Windows"):
        st.write("Вы можете скачать Gmsh для Windows по [ссылке](http://gmsh.info/#Download).")

elif choice == "Геометрические элементы":

    dimensions = st.selectbox("Выберите размерность",["0D", "1D", "2D", "3D"])
    if dimensions == "0D":
        element_0D = st.selectbox("Выберите тип элемента", ["Point", "Physical Point"])
        if element_0D == "Point":
            st.write("""
            ```bash 
            Point ( expression ) = { expression, expression, expression <, expression > }
            ```
            - **Тег точки**
            - **Координаты точки X, Y, Z**
            - **Размер элемента сетки в этой точке (не обязательный параметр)**
            """)
            code = """
                //Point
                lc = 1e-2;
                Point(1) = {0, 0, 0, lc};
                Point(2) = {.1, 0, 0, lc};
                Point(3) = {.1, .3, 0, lc};
                Point(4) = {0, .3, 0, lc};
                Geometry.PointNumbers = 1;
                Geometry.Color.Points = {160, 255, 0};
                General.Color.Text = White;
                Geometry.Color.Surfaces = Geometry.Color.Points;
            """
            st.code(code, language="python")
    
            if st.button("Запустить пример"):
                file_path = "example.geo"
                with open(file_path, "w") as f:
                    f.write(code)
                run_gmsh(file_path)

        elif element_0D == "Physical Point":
            st.write("""

            ```bash 
            Physiacal Point ( expression ) = { expression, expression, expression <, expression > }
            ```
            - **Тег точки**
            - **Теги всех элементарных точек, которые необходимо сгруппировать внутри физической точки**

            Если вместо выражения внутри скобок указано строковое выражение, то с физическим тегом связывается строковая метка, которая может быть указана явно (после запятой) или нет (в этом случае автоматически создается уникальный тег).
            """)
            code = """
                //Physiacal Point
                lc = 1e-2;
                p = newp;
                Point(p) = {0.07, 0.15, 0.025, lc};
                Physical Point("Embedded point") = {p};

                Geometry.PointNumbers = 1;
                Geometry.Color.Points = {160, 255, 0};
                General.Color.Text = White;
                Geometry.Color.Surfaces = Geometry.Color.Points;
            """
            st.code(code, language="python")

            if st.button("Запустить пример"):
                file_path = "example.geo"
                with open(file_path, "w") as f:
                    f.write(code)
                run_gmsh(file_path)

    elif dimensions == "1D":
        element_type = st.selectbox("Выберите тип элемента", ["Line", "Bezier", "Spline", "BSpline", "Circle", "Ellipse", "Curve Loop", "Physical Curve"])

        if element_type == "Line":
            st.write("""

            ```bash 
            Line ( expression ) = { expression, expression };
            ```
            - **Тег отрезка прямой линии**
            - **Теги начальной и конечной точек**

            """)
            col1, col2, col3 = st.columns(3)

            with col1:
                x1 = st.number_input("X1", value=0.0)
                x2 = st.number_input("X2", value=1.0)

            with col2:
                y1 = st.number_input("Y1", value=0.0)
                y2 = st.number_input("Y2", value=0.0)

            with col3:
                z1 = st.number_input("Z1", value=0.0)
                z2 = st.number_input("Z2", value=0.0)
            geo_code = f"""
            //Line
            Point(1) = {{{x1}, {y1}, {z1}, 1.0}};
            Point(2) = {{{x2}, {y2}, {z2}, 1.0}};
            Line(1) = {{1, 2}};
            Geometry.PointNumbers = 1;
            Geometry.Color.Points = {{160, 255, 0}};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;
            """


        elif element_type == "Bezier":
            st.write("""
            ```bash
            Bezier ( expression ) = { expression-list };
            ```
            - **Тег кривой Безье**
            - **Список выражений содержит теги контрольных точек**
            """)
            if "points" not in st.session_state:
                st.session_state.points = [(0, 0, 0), (5, 5, 5), (10, 0, 1)]  # Начальные точки

            new_points = []
            for i, (x, y, z) in enumerate(st.session_state.points):
                col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
                x_val = col1.number_input(f"X{i+1}", value=x, key=f"x_{i}")
                y_val = col2.number_input(f"Y{i+1}", value=y, key=f"y_{i}")
                z_val = col3.number_input(f"Z{i+1}", value=z, key=f"z_{i}")
                if col4.button("❌", key=f"remove_{i}"):
                    st.session_state.points.pop(i)
                    st.rerun()
                new_points.append((x_val, y_val, z_val))
            st.session_state.points = new_points
            if st.button("Добавить точку"):
                st.session_state.points.append((0, 0, 0))
                st.rerun()
            geo_code = """//Bezier\n"""
            for i, (x, y, z) in enumerate(st.session_state.points, start=1):
                geo_code += f"Point({i}) = {{{x}, {y}, {z}, 1.0}};\n"
            geo_code += f"Bezier(1) = {{{', '.join(str(i+1) for i in range(len(st.session_state.points)))}}};\n"
            geo_code += f"Geometry.PointNumbers = 1;\n"
            geo_code += "Geometry.Color.Points = {160, 255, 0};\n"
            geo_code += "General.Color.Text = White;\n"
            geo_code += "Geometry.Color.Surfaces = Geometry.Color.Points;\n"
            geo_code = geo_code.lstrip()

            

        elif element_type == "Spline":

            st.write("""

            ```bash 
            Spline ( expression ) = { expression-list };
            ```
            - **Тег сплайна**
            - **Теги точек сплайна**
            """)
            
            st.write("""
             - С помощью встроенного ядра геометрии создается сплайн Catmull-Rom.
             - С помощью ядра OpenCASCADE создается BSpline.
             - Если первая и последняя точка совпадают, тогда строится периодическая кривая.
            """)

            if "points" not in st.session_state:
                st.session_state.points = [(0, 0, 0), (5, 5, 5), (10, 0, 1)]  # Начальные точки

            new_points = []
            for i, (x, y, z) in enumerate(st.session_state.points):
                col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
                x_val = col1.number_input(f"X{i+1}", value=x, key=f"x_{i}")
                y_val = col2.number_input(f"Y{i+1}", value=y, key=f"y_{i}")
                z_val = col3.number_input(f"Z{i+1}", value=z, key=f"z_{i}")
                if col4.button("❌", key=f"remove_{i}"):
                    st.session_state.points.pop(i)
                    st.rerun()
                new_points.append((x_val, y_val, z_val))
            st.session_state.points = new_points
            if st.button("Добавить точку"):
                st.session_state.points.append((0, 0, 0))
                st.rerun()
            geo_code = """//Spline\n"""
            for i, (x, y, z) in enumerate(st.session_state.points, start=1):
                geo_code += f"Point({i}) = {{{x}, {y}, {z}, 1.0}};\n"
            geo_code += f"Spline(1) = {{{', '.join(str(i+1) for i in range(len(st.session_state.points)))}}};\n"
            geo_code += f"Geometry.PointNumbers = 1;\n"
            geo_code += "Geometry.Color.Points = {160, 255, 0};\n"
            geo_code += "General.Color.Text = White;\n"
            geo_code += "Geometry.Color.Surfaces = Geometry.Color.Points;\n"
            geo_code = geo_code.lstrip()
            

        

        elif element_type == "BSpline":
            st.write("""

            ```bash 
            BSpline ( expression ) = { expression-list };
            ```
            - **Тег сплайна**
            - **Теги контрольных точек сплайна**
            """)
            
            st.write("""
             - Если первая и последняя точка совпадают, тогда строится периодическая кривая.
            """)

            if "points" not in st.session_state:
                st.session_state.points = [(0, 0, 0), (5, 5, 5), (10, 0, 1)]  # Начальные точки

            new_points = []
            for i, (x, y, z) in enumerate(st.session_state.points):
                col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
                x_val = col1.number_input(f"X{i+1}", value=x, key=f"x_{i}")
                y_val = col2.number_input(f"Y{i+1}", value=y, key=f"y_{i}")
                z_val = col3.number_input(f"Z{i+1}", value=z, key=f"z_{i}")
                if col4.button("❌", key=f"remove_{i}"):
                    st.session_state.points.pop(i)
                    st.rerun()
                new_points.append((x_val, y_val, z_val))
            st.session_state.points = new_points
            if st.button("Добавить точку"):
                st.session_state.points.append((0, 0, 0))
                st.rerun()
            geo_code = """//BSpline\n"""
            for i, (x, y, z) in enumerate(st.session_state.points, start=1):
                geo_code += f"Point({i}) = {{{x}, {y}, {z}, 1.0}};\n"
            geo_code += f"BSpline(1) = {{{', '.join(str(i+1) for i in range(len(st.session_state.points)))}}};\n"
            geo_code += f"Geometry.PointNumbers = 1;\n"
            geo_code += "Geometry.Color.Points = {160, 255, 0};\n"
            geo_code += "General.Color.Text = White;\n"
            geo_code += "Geometry.Color.Surfaces = Geometry.Color.Points;\n"
            geo_code = geo_code.lstrip()

        elif element_type == "Circle":

            st.write("""

            ```bash 
            Circle ( expression ) = { expression, expression, expression <, ...> };
            ```
            - **Тег дуги окружности**
            - **Теги точек (начало дуги, центр, конечная точка дуги)**
            """)
            
            st.write("""
             - Со встроенным ядрoм геометрии дуга должна быть строго меньше числа π.
             - С ядром OpenCASCADE, если указано от 4 до 6 точек, первые три определяют координаты центра, следующие определяет радиус, а последние 2 определяют угол.
            """)

            if "center" not in st.session_state:
                st.session_state.center = (0, 0, 0)
            if "radius" not in st.session_state:
                st.session_state.radius = 5.0
        
            col1, col2, col3 = st.columns([3, 3, 3])
            cx = col1.number_input("X (центр)", value=st.session_state.center[0], key="cx")
            cy = col2.number_input("Y (центр)", value=st.session_state.center[1], key="cy")
            cz = col3.number_input("Z (центр)", value=st.session_state.center[2], key="cz")
            radius = st.number_input("Радиус", min_value=0.1, key="radius")

            if "center" in st.session_state:
                st.session_state.center = (cx, cy, cz)
    
            st.session_state.center = (cx, cy, cz)
        
            # Вычисление трёх точек для окружности
            p1 = (cx - radius, cy, cz)
            p2 = (cx, cy + radius, cz)
            p3 = (cx + radius, cy, cz)
    
        
            geo_code = """//Circle\n"""
            geo_code += f"Point(1) = {{{p1[0]}, {p1[1]}, {p1[2]}, 1.0}};\n"
            geo_code += f"Point(2) = {{{cx}, {cy}, {cz}, 1.0}}; // Центр\n"
            geo_code += f"Point(3) = {{{p3[0]}, {p3[1]}, {p3[2]}, 1.0}};\n"
            geo_code += f"Circle(1) = {{1, 2, 3}};\n"
            geo_code += f"Geometry.PointNumbers = 1;\n"
            geo_code += "Geometry.Color.Points = {160, 255, 0};\n"
            geo_code += "General.Color.Text = White;\n"
            geo_code += "Geometry.Color.Surfaces = Geometry.Color.Points;\n"
            geo_code = geo_code.lstrip()

        elif element_type == "Ellipse":

            st.write("""

            ```bash 
            Ellipse ( expression ) = { expression, expression, expression <, ...> };
            ```
            - **Тег дуги эллипса**
            - **Тег начальной точки**
            - **Тег центральной точки**
            - **Тег точки на большей полуоси эллипса**
            - **Тег конечной точки**
            """)
            
            st.write("""
             - Если первая точка является точкой большой оси, третье выражение можно опустить.
             - С ядром OpenCASCADE, если указано от 5 до 7 выражений, первые три определяют координаты центра, следующие два определяют большой (вдоль оси x) и малый радиусы (вдоль оси y), а следующие два — начальный и конечный угол.
             - OpenCASCADE не позволяет создавать дуги эллипса с большим радиусом, меньше малого радиуса.
            """)

            if "center" not in st.session_state:
                st.session_state.center = (0, 0, 0)
            if "semi_major_axis" not in st.session_state:
                st.session_state.semi_major_axis = 5.0
            if "semi_minor_axis" not in st.session_state:
                st.session_state.semi_minor_axis = 3.0
    
            col1, col2, col3 = st.columns([3, 3, 3])
            cx = col1.number_input("X (центр)", value=st.session_state.center[0], key="cx")
            cy = col2.number_input("Y (центр)", value=st.session_state.center[1], key="cy")
            cz = col3.number_input("Z (центр)", value=st.session_state.center[2], key="cz")
    
            # Получаем полуоси эллипса
            semi_major_axis = st.number_input("Полуось по X", min_value=0.1, key="semi_major_axis")
            semi_minor_axis = st.number_input("Полуось по Y", min_value=0.1, key="semi_minor_axis")
    
            # Обновляем состояние сессии только если это необходимо
            if "center" in st.session_state:
                st.session_state.center = (cx, cy, cz)

            # Вычисление четырёх точек для эллипса
            p1 = (cx - semi_major_axis, cy, cz)
            p2 = (cx, cy + semi_minor_axis, cz)
            p3 = (cx + semi_major_axis, cy, cz)
            p4 = (cx, cy - semi_minor_axis, cz)
    
        
            geo_code = """//Ellipse\n"""
            geo_code += f"Point(1) = {{{p1[0]}, {p1[1]}, {p1[2]}, 1.0}};\n"
            geo_code += f"Point(2) = {{{cx}, {cy}, {cz}, 1.0}}; // Центр эллипса\n"
            geo_code += f"Point(3) = {{{p3[0]}, {p3[1]}, {p3[2]}, 1.0}};\n"
            geo_code += f"Point(4) = {{{p4[0]}, {p4[1]}, {p4[2]}, 1.0}};\n"
            geo_code += f"Ellipse(1) = {{1, 2, 3, 4}};\n"
            geo_code += f"Geometry.PointNumbers = 1;\n"
            geo_code += "Geometry.Color.Points = {160, 255, 0};\n"
            geo_code += "General.Color.Text = White;\n"
            geo_code += "Geometry.Color.Surfaces = Geometry.Color.Points;\n"
            geo_code = geo_code.lstrip()

        elif element_type == "Curve Loop":
            st.write("""

                ```bash 
                Curve Loop ( expression ) = { expression-list };
                ```
                - **Тег замкнутого конутра**
                - **Выражение в скобках является тегом цикла кривой**
                - **Список выражений справа должен содержать теги всех кривых, составляющих цикл кривой**
                """)
            
            st.write("""
                 - С помощью встроенного геометрического ядра кривые должны быть упорядочены и ориентированы, используя отрицательные теги для указания обратной ориентации.
                """)

            geo_code = """
            // Curve Loop
            Point(1) = {0, 0, 0, 1.0};
            Point(2) = {0.5, -0.3, 0, 1.0};  
            Point(3) = {1, -0.2, 0, 1.0};

            Point(4) = {1.2, 0.5, 0, 1.0};  
            Point(5) = {1.5, 1, 0, 1.0};

            Point(6) = {1.1, 1.5, 0, 1.0};  
            Point(7) = {0.5, 1.7, 0, 1.0};

            Point(8) = {-0.2, 1.6, 0, 1.0};  
            Point(9) = {-0.7, 1, 0, 1.0};

            Point(10) = {-0.6, 0.5, 0, 1.0};  
            Point(11) = {0, 0, 0};  

            Spline(1) = {1, 2, 3};
            Spline(2) = {3, 4, 5};
            Spline(3) = {5, 6, 7};
            Spline(4) = {7, 8, 9};
            Spline(5) = {9, 10, 11};

            Curve Loop(1) = {1, 2, 3, 4, 5};

            Geometry.PointNumbers = 1;
            Geometry.Color.Points = {160, 255, 0}; 
            General.Color.Text = White;
            Geometry.Color.Surfaces = {200, 200, 200}; 
            """

        elif element_type == "Physical Curve":

            st.write("""

                ```bash 
                Physical Curve ( expression | string-expression <, expression> ) <+|->= {expression-list };
                ```
                - **Тег физической кривой**
                - **Список выражений справа должен содержать теги всех элементарных кривых, которые необходимо сгруппировать внутри физической кривой**
                """)
            
            st.write("""
                 - С помощью встроенного геометрического ядра кривые должны быть упорядочены и ориентированы, используя отрицательные теги для указания обратной ориентации.
                 - Если вместо выражения внутри скобок указано строковое выражение, то с физическим тегом связывается строковая метка, которая может быть указана явно (после запяой) или нет (в этом случае автоматически создается уникальный тег).
                 - В некоторых форматах файлов сетки (например, MSH2) указание отрицательных тегов в списке выражений изменит ориентацию элементов сетки, принадлежащих соответствующим элементарным кривым в сохраненном файле сетки.
                """)

            geo_code = """
            //Physical Curve
            Point(1) = {0, 0, 0};
            Point(2) = {1, 0, 0};
            Point(3) = {1, 1, 0};
            Point(4) = {0, 1, 0};

            Line(1) = {1, 2};
            Line(2) = {2, 3};
            Line(3) = {3, 4};
            Line(4) = {4, 1};

            Physical Curve("Boundary", 100) = {1, 2, 3, 4};
            Geometry.PointNumbers = 1;
            Geometry.Color.Points = {160, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;
            """

        st.code(geo_code, language="python")
    
        def save_example_file():
            example_file_path = "./example.geo"
            with open(example_file_path, "w") as f:
                f.write(geo_code)
            return example_file_path
    
        if st.button("Перестроить геометрию"):
            example_file_path = save_example_file()
            run_gmsh(example_file_path)
        
    elif dimensions == "2D":
        element_type_2D = st.selectbox("Выберите тип элемента", ["Plane Surface", "Bezier(BSpline) Surface", "Surface Loop", "Physical Surface"])

        if element_type_2D == "Plane Surface":
            st.write("""
                ```bash
                Plane Surface ( expression ) = { expression-list };
                ```

                - **Тег плоской поверхности**
                - **Список выражений справа должен содержать теги всех контуров кривых, определяющих поверхность**
            """)
            
            st.write("""
                 - Первый контур кривых определяет внешнюю границу поверхности.    
                 - Все остальные контуры кривых определяют отверстия в поверхности.
                 - Контур кривых, определяющий отверстие, не должен иметь общих кривых с внешним контуром кривых (в этом случае он не является отверстием, и две поверхности должны быть определены отдельно).
                 - Аналогично, контур кривых, определяющий отверстие, не должен иметь общих кривых с другим контуром кривых, определяющим отверстие в той же поверхности (в этом случае два контура кривых должны быть объединены).
                """)

            geo_code = """
            //Plane Surface
            Point(1) = {0, 0, 0};
            Point(2) = {5, 0, 0};
            Point(3) = {5, 5, 0};
            Point(4) = {0, 5, 0};

            
            Point(5) = {2.5, 2.5, 0}; // Центр круга
            Point(6) = {3.5, 2.5, 0}; // Правая точка
            Point(7) = {2.5, 3.5, 0}; // Верхняя точка
            Point(8) = {1.5, 2.5, 0}; // Левая точка
            Point(9) = {2.5, 1.5, 0}; // Нижняя точка

            Line(1) = {1, 2};
            Line(2) = {2, 3};
            Line(3) = {3, 4};
            Line(4) = {4, 1};

            Circle(5) = {8, 5, 7};
            Circle(6) = {7, 5, 6};
            Circle(7) = {6, 5, 9};
            Circle(8) = {9, 5, 8};  

            Curve Loop(1) = {1, 2, 3, 4}; // Внешний квадрат
            Curve Loop(2) = {5, 6, 7, 8}; // Внутренний круг (отверстие)

            // Создание плоской поверхности с отверстием
            Plane Surface(1) = {1, 2};
            Geometry.PointNumbers = 1;

            // Настройки цветов
            Geometry.Color.Points = {160, 255, 0};   
            Geometry.Color.Lines = {0, 0, 200};    
            Geometry.Color.Surfaces = {200, 200, 200}; 

            //Генерация 2D-сетки
            Mesh 2;

            """

        
        elif element_type_2D == "Bezier(BSpline) Surface":
            st.write("""
                ```bash
                Bezier Surface ( expression ) = { expression-list };
                ```

                - **Тег поверхности, построенной на кривых Безье**
                - **Тег контура, построенного на 2, 3, 4 кривых Безье**
            """)
            st.write("""
                ```bash
                BSpline Surface ( expression ) = { expression-list };
                ```
                - **Тег поверхности, построенной на сплайнах**
                - **Теги контура, построенного на 2, 3, 4 сплайнах**
                
            """)
            
            st.write("""
             - Поверхность Безье доступна только с ядром OpenCASCADE.
             - Поверхность Сплайнов доступна только с ядром OpenCASCADE.
            """)
            geo_code = """
            //Bezier Surface
            SetFactory("OpenCASCADE");
            Point(1) = {0, 0, 0};
            Point(2) = {1, 0.5, 0};
            Point(3) = {2, 0, 0};

            Point(4) = {0, 1, 1};
            Point(5) = {2, 1, 1};

            Point(6) = {0, 2, 0};
            Point(7) = {1, 2.5, 0};
            Point(8) = {2, 2, 0};

            Bezier(1) = {1, 2, 3};  // Нижняя граница
            Bezier(3) = {6, 7, 8};  // Верхняя граница
            Bezier(4) = {1, 4, 6};  // Левая боковая кривая
            Bezier(5) = {3, 5, 8};  // Правая боковая кривая

            Curve Loop(1) = {1, 5, -3, -4};

            Bezier Surface(1) = {1};
            Geometry.PointNumbers = 1;
            // Настройки цветов
            Geometry.Color.Points = {160, 255, 0};
            Geometry.Color.Lines = {0, 0, 200};
            Geometry.Color.Surfaces = {200, 200, 200};

            //Генерация 2D-сетки
            Mesh 2;

            """
        
        elif element_type_2D == "Surface Loop":
            st.write("""
                ```bash
                Surface Loop ( expression ) = { expression-list } < Using Sewing >;
                ```

                - **Тег поверхности цикла**
                - **Список выражений справа должен содержать теги всех поверхностей, составляющих цикл поверхности**
            """)
            
            st.write("""
             - Цикл поверхности всегда должен представлять собой замкнутую оболочку, а поверхности должны быть ориентированы последовательно (используя отрицательные теги для указания обратной ориентации).
            """)
            geo_code = """
            //Surface Loop
            lc = 1e-2;
            Point(1) = {0, 0, 0, lc};
            Point(2) = {.1, 0, 0, lc};
            Point(3) = {.1, .3, 0, lc};
            Point(4) = {0, .3, 0, lc};
            Line(1) = {1, 2};
            Line(2) = {3, 2};
            Line(3) = {3, 4};
            Line(4) = {4, 1};
            Curve Loop(1) = {4, 1, -2, 3};
            Plane Surface(1) = {1};
            Point(5) = {0, .4, 0, lc};
            Line(5) = {4, 5};
            Translate {-0.02, 0, 0} { Point{5}; }
            Rotate {{0,0,1}, {0,0.3,0}, -Pi/4} { Point{5}; }
            Translate {0, 0.05, 0} { Duplicata{ Point{3}; } }
            Line(7) = {3, 6};
            Line(8) = {6, 5};
            Curve Loop(10) = {5,-8,-7,3};
            Plane Surface(11) = {10};
            
            Point(100) = {0., 0.3, 0.12, lc}; Point(101) = {0.1, 0.3, 0.12, lc};
            Point(102) = {0.1, 0.35, 0.12, lc};
            xyz[] = Point{5}; // Get coordinates of point 5
            Point(103) = {xyz[0], xyz[1], 0.12, lc};
            Line(110) = {4, 100}; Line(111) = {3, 101};
            Line(112) = {6, 102}; Line(113) = {5, 103};
            Line(114) = {103, 100}; Line(115) = {100, 101};
            Line(116) = {101, 102}; Line(117) = {102, 103};
            Surface Loop(128) = {127, 119, 121, 123, 125, 11};
            Geometry.PointNumbers = 1;
            // Настройки цветов
            Geometry.Color.Points = {160, 255, 0};
            Geometry.Color.Lines = {0, 0, 200};
            Geometry.Color.Surfaces = {200, 200, 200};

            //Генерация 2D-сетки
            Mesh 2;

            """

        elif element_type_2D == "Physical Surface":
            st.write("""
                ```bash
                Physical Surface ( expression | string-expression <, expression> ) <+|->= { expression-list };
                ```

                - **Тег физической поверхности**
                - **Список выражений справа должен содержать теги всех поверхностей, составляющих цикл поверхности**
            """)
            
            st.write("""
             - Список выражений справа должен содержать теги всех элементарных поверхностей, которые необходимо сгруппировать внутри физической поверхности.
            """)
            geo_code = """
            //Physiacal Surface
            SetFactory("OpenCASCADE");
            lc = 1e-2;
            Point(1) = {0, 0, 0, lc};
            Point(2) = {.1, 0, 0, lc};
            Point(3) = {.1, .3, 0, lc};
            Point(4) = {0, .3, 0, lc};

            Line(1) = {1, 2};
            Line(2) = {2, 3}; // Обратите внимание на порядок
            Line(3) = {3, 4};
            Line(4) = {4, 1};

            Curve Loop(1) = {4, 1, -2, 3};
            Plane Surface(1) = {1};

            Physical Curve(5) = {1, 2, 4};
            Physical Surface("My surface") = {1};

            
            Rectangle(2) = {0.2, 0.0, 0.0, 0.1, 0.3};
            Geometry.PointNumbers = 1;
            Geometry.Color.Points = {160, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            //Генерация 2D-сетки
            Mesh 2;
            """

        st.code(geo_code, language="python")
    
        def save_example_file():
            example_file_path = "./example.geo"
            with open(example_file_path, "w") as f:
                f.write(geo_code)
            return example_file_path
    
        if st.button("Перестроить геометрию"):
            example_file_path = save_example_file()
            run_gmsh(example_file_path)
    
    elif dimensions == "3D":
        element_type_3D = st.selectbox("Выберите тип элемента", ["Volume", "Sphere", "Box", "Cylinder", "Torus", "Cone", "Wedge", "Physical Volume"])

        if element_type_3D == "Volume":
            st.write("""
                ```bash
                Volume ( expression ) = { expression-list };
                ```

                - **Тег объема**
                - **Список выражений справа должен содержать теги всех контуров поверхности, определяющих объем**
                - **Первый контур поверхности определяет внешнюю границу объема** 
                - **Все остальные контуры поверхности определяют отверстия в объеме**
            """)
            
            st.write("""
             - Контур поверхности, определяющий отверстие, не должен иметь общих поверхностей с контуром внешней поверхности (в этом случае это не отверстие, и два объема должны быть определены отдельно).
             - Точно так же контур поверхности, определяющий отверстие, не должен иметь общих поверхностей с другим контуром поверхности, определяющим отверстие в том же объеме (в этом случае два контура поверхности должны быть объединены).
            """)
            geo_code = """
            //Volume
            SetFactory("OpenCASCADE");
            Box(1) = {0, 0, 0, 1, 1, 1}; // Куб 1x1x1
            Sphere(2) = {0.5, 0.5, 0.5, 0.3}; // Сфера внутри куба
            Surface Loop(3) = {1, 2, 3, 4, 5, 6}; 
            Surface Loop(4) = {7};
            Volume(5) = {3, 4}; // Куб с вырезанной сферической областью
            Geometry.PointNumbers = 1;
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {160, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            
            """

        elif element_type_3D == "Sphere":
            st.write("""
                ```bash
                Sphere ( expression ) = { expression-list };
                ```

                - **Тег сферы, заданной тремя координатами ее центра и радиусом**
                - **Дополнительные выражения определяют три предела угла**
                - **Первые два необязательных аргумента определяют полярный угол раскрытия** 
                - **Все остальные контуры поверхности определяют отверстия в объеме**
            """)
            
            st.write("""
             - Необязательный аргумент «angle3» определяет азимут раскрытия.
             - Сфера доступна только с ядром OpenCASCADE.
            """)

            geo_code = """
            //Shere
            SetFactory("OpenCASCADE");

            Sphere(1) = {0, 0, 0, 1, -Pi/2, Pi/2}; // Полусфера радиусом 1
            Geometry.PointNumbers = 1;
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {160, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            // Генерация 3D-сетки
            Mesh 3;

            """

        elif element_type_3D == "Box":
            st.write("""
                ```bash
                Box ( expression ) = { expression-list };
                ```

                - **Тег параллелипипеда, заданного диагональю**
            """)
            
            st.write("""
             - Доступен только с ядром OpenCASCADE.
            """)
            geo_code = """
            //Box
            SetFactory("OpenCASCADE");

            Box(1) = {0, 0, 0, 2, 1, 3}; // Параллелепипед
            Geometry.PointNumbers = 1;
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {160, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            // Генерация 3D-сетки
            Mesh 3;

            """

        elif element_type_3D == "Cylinder":
            st.write("""
                ```bash
                Cylinder ( expression ) = { expression-list };
                ```

                - **Тег цилиндра, определяемого тремя координатами центра первой боковой поверхности, тремя компонентами вектора, определяющими его ось и радиус**
                - **Дополнительное выражение определяет угол основания**
            """)
            
            st.write("""
             - Доступен только с ядром OpenCASCADE.
            """)
            geo_code = """
            //Cylinder
            SetFactory("OpenCASCADE");

            Cylinder(1) = {0, 0, 0, 0, 3, 0, 0.5}; // Цилиндр вдоль оси Y
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {160, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            // Генерация 3D-сетки
            Mesh 3;

            """

        elif element_type_3D == "Torus":
            st.write("""
                ```bash
                Torus ( expression ) = { expression-list };
                ```

                - **Тег тора, определяемого тремя координатами его центра и двумя радиусами**
                - **Дополнительное выражение определяет угловое раскрытие**
            """)
            
            st.write("""
             - Доступен только с ядром OpenCASCADE.
            """)
            geo_code = """
            //Torus
            SetFactory("OpenCASCADE");

            Torus(1) = {0, 0, 0, 2, 0.5}; // Тор
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {160, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            // Генерация 3D-сетки
            Mesh 3;

            """

        elif element_type_3D == "Cone":
            st.write("""
                ```bash
                Cone ( expression ) = { expression-list };
                ```

                - **Создайте конус, определяемый тремя координатами центра основания, тремя компонентами вектора, определяющего его ось, и двумя радиусами средней линии и верхнего основания (эти радиусы могут быть нулевыми)**
                - **Дополнительное выражение определяет угловое раскрытие**
            """)
            
            st.write("""
             - Доступен только с ядром OpenCASCADE.
            """)
            geo_code = """
            //Cone
            SetFactory("OpenCASCADE");

            Cone(1) = {0, 0, 0, 0, 0, 2, 1, 0.3}; // Конус высотой 2
            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {160, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            // Генерация 3D-сетки
            Mesh 3;

            """

        elif element_type_3D == "Wedge":
            st.write("""
                ```bash
                Wedge ( expression ) = { expression-list };
                ```

                - **Тег прямого углового клина, определяемый тремя координатами точки прямого угла и тремя размерами**
                - **Дополнительный параметр определяет верхнюю протяженность (по умолчанию ноль)**
            """)
            
            st.write("""
             - Доступен только с ядром OpenCASCADE.
            """)
            geo_code = """
            //Wedge
            SetFactory("OpenCASCADE");

            Wedge(1) = {0, 0, 0, 2, 2, 1, 1}; // Клин

            Geometry.SurfaceNumbers = 2;
            Geometry.VolumeNumbers = 3;
            Geometry.Color.Points = {160, 255, 0};
            General.Color.Text = White;
            Geometry.Color.Surfaces = Geometry.Color.Points;

            // Генерация 3D-сетки
            Mesh 3;

            """
        

        elif element_type_3D == "Physical Volume":
            st.write("""
                ```bash
                Physical Volume ( expression | string-expression <, expression> ) <+|->= { expression-list };

                ```

                - **Тег физического объема**
                - **Список выражений справа должен содержать теги всех элементарных томов, которые необходимо сгруппировать внутри физического объема**
            """)
            geo_code = """
            //Physical Volume
            SetFactory("OpenCASCADE");
            Box(1) = {0, 0, 0, 1, 1, 1};
            Sphere(2) = {0.5, 0.5, 0.5, 0.5};
            BooleanDifference(3) = {Volume{1}; Delete; }{ Volume{2}; Delete; };

            Physical Volume("Hollow Cube") = {3};

            // Генерация 3D-сетки
            Mesh 3;

            """

        st.code(geo_code, language="python")
    
        def save_example_file():
            example_file_path = "./example.geo"
            with open(example_file_path, "w") as f:
                f.write(geo_code)
            return example_file_path
    
        if st.button("Перестроить геометрию"):
            example_file_path = save_example_file()
            run_gmsh(example_file_path)


    
elif choice == "Файл геометрии":
    # 1. Установка фабрики геометрии
    st.write("""##### 1. Установка фабрики геометрии""")
    st.write("""
     - Команда `SetFactory("OpenCASCADE");` указывает GMSH использовать библиотеку OpenCASCADE для построения геометрии. 
    Это необходимо для создания сложных геометрических объектов, таких как окружности и экструзии.
    """)

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

    st.write("""##### 8. Пример простого файла .geo""")
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

    # Возможность загрузки файла для Gmsh только в этом разделе
    uploaded_file = st.file_uploader("Загрузите файл для Gmsh", type=["geo", "msh", "step", "stl"])

    if uploaded_file is not None:
        file_path = os.path.join("./", uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Файл {uploaded_file.name} успешно загружен!")
        
        if st.button("Запустить Gmsh"):
            run_gmsh(file_path)

elif choice == "Создание области":
    st.write("""##### 1. Явное задание через точки, линии и поверхности""")
    st.write("""
    Этот метод использует базовые геометрические элементы Gmsh: точки, линии, поверхностные петли и объемы.
     - **0D -> 1D -> 2D -> 3D**
    """)
    st.subheader("Шаг 1: Определение точек")
    st.write("""###### Шаг 1: Определение точек""")

    geo_code1 = """
    // Создаем точки
    L = 1.0; // Длина ребра куба
    Nx = 10; // Число элементов по X
    Ny = 10; // Число элементов по Y
    Nz = 10; // Число элементов по Z

    Point(1) = {0, 0, 0, L/Nx};
    Point(2) = {L, 0, 0, L/Nx};
    Point(3) = {L, L, 0, L/Nx};
    Point(4) = {0, L, 0, L/Nx};
    Point(5) = {0, 0, L, L/Nx};
    Point(6) = {L, 0, L, L/Nx};
    Point(7) = {L, L, L, L/Nx};
    Point(8) = {0, L, L, L/Nx};
    """
    show_code(geo_code1, "python")

    st.write("""###### Шаг 2: Построение ребер куба""")

    geo_code2 = """
    Line(1) = {1, 2};
    Line(2) = {2, 3};
    Line(3) = {3, 4};
    Line(4) = {4, 1};
    Line(5) = {5, 6};
    Line(6) = {6, 7};
    Line(7) = {7, 8};
    Line(8) = {8, 5};
    Line(9) = {1, 5};
    Line(10) = {2, 6};
    Line(11) = {3, 7};
    Line(12) = {4, 8};
    
    """
    show_code(geo_code2, "python")

    st.write("""###### Шаг 3: Построение поверхности куба""")

    geo_code3 = """
    // Создаём поверхности
    Line Loop(13) = {1, 2, 3, 4};
    Plane Surface(14) = {13};
    Line Loop(15) = {5, 6, 7, 8};
    Plane Surface(16) = {15};
    Line Loop(17) = {1, 10, -5, -9};
    Plane Surface(18) = {17};
    Line Loop(19) = {2, 11, -6, -10};
    Plane Surface(20) = {19};
    Line Loop(21) = {3, 12, -7, -11};
    Plane Surface(22) = {21};
    Line Loop(23) = {4, 9, -8, -12};
    Plane Surface(24) = {23};

    """
    show_code(geo_code3, "python")

    st.write("""###### Шаг 4: Построение объема""")

    geo_code4 = """
    // Создаём объем
    Surface Loop(25) = {14, 16, 18, 20, 22, 24};
    Volume(26) = {25};

    // Определяем сетку
    Transfinite Line {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12} = Nx+1 Using Progression 1;
    Transfinite Surface {14, 16, 18, 20, 22, 24};
    Transfinite Volume {26};
    Recombine Surface {14, 16, 18, 20, 22, 24};
    Physical Volume("Cube1") = {26};
    Color Red {Volume{26};}
    Mesh 3;
    """
    show_code(geo_code4, "python")

    geo_full_code = geo_code1 + geo_code2 + geo_code3 + geo_code4

    # Загрузка файла примера
    def save_example_file():
        example_file_path = './example.geo'
        with open(example_file_path, 'w') as f:
            f.write(geo_full_code)
        return example_file_path

    # Кнопка для загрузки и запуска примера
    if st.button("Пример 1"):
        example_file_path = save_example_file()
        run_gmsh(example_file_path)

    st.write("""
     - Недостатки: Трудно задавать сложную геометрию.
     - Преимущества: Полный контроль над топологией.
    """)

    st.write("""##### 2. OpenCASCADE""")
    
    st.write("""
    Этот метод упрощает построение сложных геометрий за счет использования встроенных примитивов.
    """)
    geo_code5 = """
    // Определяем размеры кубов
    L = 1.0; // Длина ребра куба
    Nx = 10; // Число элементов по X
    Ny = 10; // Число элементов по Y
    Nz = 10; // Число элементов по Z

    // Первый куб (классический способ)
    Point(1) = {0, 0, 0, L/Nx};
    Point(2) = {L, 0, 0, L/Nx};
    Point(3) = {L, L, 0, L/Nx};
    Point(4) = {0, L, 0, L/Nx};
    Point(5) = {0, 0, L, L/Nx};
    Point(6) = {L, 0, L, L/Nx};
    Point(7) = {L, L, L, L/Nx};
    Point(8) = {0, L, L, L/Nx};

    Line(1) = {1, 2};
    Line(2) = {2, 3};
    Line(3) = {3, 4};
    Line(4) = {4, 1};
    Line(5) = {5, 6};
    Line(6) = {6, 7};
    Line(7) = {7, 8};
    Line(8) = {8, 5};
    Line(9) = {1, 5};
    Line(10) = {2, 6};
    Line(11) = {3, 7};
    Line(12) = {4, 8};

    Line Loop(13) = {1, 2, 3, 4};
    Plane Surface(14) = {13};
    Line Loop(15) = {5, 6, 7, 8};
    Plane Surface(16) = {15};
    Line Loop(17) = {1, 10, -5, -9};
    Plane Surface(18) = {17};
    Line Loop(19) = {2, 11, -6, -10};
    Plane Surface(20) = {19};
    Line Loop(21) = {3, 12, -7, -11};
    Plane Surface(22) = {21};
    Line Loop(23) = {4, 9, -8, -12};
    Plane Surface(24) = {23};

    Surface Loop(25) = {14, 16, 18, 20, 22, 24};
    Volume(26) = {25};

    Physical Volume("Cube1") = {26};
    Color Red {Volume{26};}

    // Второй куб (через OpenCASCADE)
    SetFactory("OpenCASCADE");
    Box(27) = {L + 0.5, 0, 0, L, L, L};
    Physical Volume("Cube2") = {27};
    Color Blue {Volume{27};}

    // Определяем сетку
    Transfinite Line {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12} = Nx+1 Using Progression 1;
    Transfinite Surface {14, 16, 18, 20, 22, 24};
    Transfinite Volume {26};
    Recombine Surface {14, 16, 18, 20, 22, 24};
    Mesh 3;
    """
    show_code(geo_code5, "python")

    # Загрузка файла примера
    def save_example_file():
        example_file_path = './example.geo'
        with open(example_file_path, 'w') as f:
            f.write(geo_code5)
        return example_file_path

    # Кнопка для загрузки и запуска примера
    if st.button("Пример 2"):
        example_file_path = save_example_file()
        run_gmsh(example_file_path)

    st.write("""
     - Преимущества: Меньше кода, удобное управление геометрией.
     - Недостатки: Меньше контроля над отдельными гранями.
    """)

    st.write("""##### 3. Импорт CAD-модели""")
    st.write("""
    Если у вас есть готовая CAD-модель цилиндра, например, в формате STEP, можно просто импортировать и создать сетку.
    """)

    geo_code6 = """
    // Импортируем CAD-модель
    Merge "cylinder.step";

    // Устанавливаем размер сетки
    MeshSize {1} = 0.2;

    // Генерируем объемную сетку
    Mesh 3;
    """
    show_code(geo_code6, "python")

    st.write("""
     - Преимущества: Можно использовать сложные геометрии из других программ (SolidWorks, FreeCAD).
     - Недостатки: Нельзя редактировать геометрию в Gmsh.
    """)

    st.write("""##### Вывод""")

    st.write("""
     - Классический метод полезен для учебных целей и тонкого контроля.
     - OpenCASCADE — оптимальный вариант для большинства задач.
     - Импорт CAD хорош, если у вас уже есть модель.
    """)

elif choice == "Интерактивные возможности создания области":

    def run_gmsh_view():
        try:
            # Попытка запустить GMSH
            subprocess.run(["gmsh"], check=True)
        except subprocess.CalledProcessError as e:
            st.error(f"Ошибка при запуске GMSH: {e}")
        except FileNotFoundError:
            st.error("GMSH не найден. Убедитесь, что GMSH установлен и доступен в пути.")

    if st.button("Запустить GMSH"):
        run_gmsh_view()

    # Шаг 1: Создание новой геометрии
    st.write("""##### Шаг 1: Создание новой геометрии""")
    st.write("""
    1. Откройте GMSH: 
    ``` bash 
            gmsh
    ```
    2. Перейдите в меню "File" и выберите "New" для создания нового файла.
    """)
    # Место для картинки (шаг 1)
    st.image("step1_create_geometry.png", caption="Шаг 1: Создание новой геометрии",use_container_width=True)

    # Шаг 2: Определение точек
    st.write("""##### Шаг 2: Определение точек""")
    st.write("""
    Для создания прямоугольника начнем с определения 4 точек.
    В верхнем меню выберите "Geometry" -> "Elementary entitie" -> "Add" -> "Point"  и щелкните на рабочей области, чтобы разместить точки.
    - Точка 1: [0,0,0]
    - Точка 2: [L, 0, 0] — где L — длина области.
    - Точка 3: [L, W, 0] — где W — ширина области.
    - Точка 4: [0, W, 0]
    """)
    # Место для картинки (шаг 2)
    st.image("step2_define_points.png", caption="Шаг 2: Определение точек", use_container_width=True)

    # Шаг 3: Соединение точек
    st.write("""##### Шаг 3: Соединение точек""")
    st.write("""
    После того как точки размещены, их нужно соединить.
    1. В верхнем меню выберите "Geometry" -> "Elementary entitie" -> "Add" -> "Line".
    2. Соедините точки с помощью линий:
    - Линия 1: соединяет точку 1 и точку 2.
    - Линия 2: соединяет точку 2 и точку 3.
    - Линия 3: соединяет точку 3 и точку 4.
    - Линия 4: соединяет точку 4 и точку 1.
    """)
    # Место для картинки (шаг 3)
    st.image("step3_connect_points.png", caption="Шаг 3: Соединение точек", use_container_width=True)

    # Шаг 4: Создание поверхности
    st.write("""##### Шаг 4: Создание поверхности""")
    st.write("""
    Теперь, когда у нас есть все линии, можно создать поверхность, заключенную в этих линиях.
    1. Перейдите в меню "Geometry" -> "Elementary entitie" -> "Add" -> "Plane surface".
    2. Выберите линии для создания поверхности.
    """)
    # Место для картинки (шаг 4)
    st.image("step4_create_surface.png", caption="Шаг 4: Создание поверхности", use_container_width=True)

    # Шаг 5: Генерация сетки
    st.write("""##### Шаг 5: Генерация сетки""")
    st.write("""
    После создания геометрии можно генерировать сетку.
    1. Перейдите в меню "Mesh" и выберите "2D" для генерации двумерной сетки для поверхности.
    2. GMSH автоматически сгенерирует сетку для вашего прямоугольника.
    """)
    # Место для картинки (шаг 5)
    st.image("step5_generate_mesh.png", caption="Шаг 5: Генерация сетки", use_container_width=True)

    # Шаг 6: Визуализация
    st.write("""##### Шаг 6: Визуализация""")
    st.write("""
    После генерации сетки вы можете переключиться на вкладку "View" и включить отображение сетки.
    Вы также можете управлять цветами, отображением и другими параметрами визуализации.
    """)
    # Место для картинки (шаг 6)
    st.image("step6_visualize.png", caption="Шаг 6: Визуализация сетки", use_container_width=True)

    # Шаг 7: Сохранение файла
    st.write("""##### Шаг 7: Сохранение файла""")
    st.write("""
    Вы можете сохранить файл, выбрав "File" -> "Save Mesh".
    """)
    # Место для картинки (шаг 7)
    st.image("step7_save_file.png", caption="Шаг 7: Сохранение файла", use_container_width=True)

    # Пример команды GMSH
    st.write("""##### Пример файла GMSH""")
    st.write("""
    Вы также можете использовать GMSH для создания геометрии и сетки через текстовый файл. Вот пример скрипта для создания прямоугольной области:

    ```bash
    // Прямоугольная область с размерами LxW

    L = 10;  // длина
    W = 5;   // ширина

    // Определение точек
    Point(1) = {0, 0, 0, 1};
    Point(2) = {L, 0, 0, 1};
    Point(3) = {L, W, 0, 1};
    Point(4) = {0, W, 0, 1};

    // Определение линий
    Line(1) = {1, 2};
    Line(2) = {2, 3};
    Line(3) = {3, 4};
    Line(4) = {4, 1};

    // Создание поверхности
    Line Loop(1) = {1, 2, 3, 4};
    Plane Surface(1) = {1};

    // Генерация сетки
    Mesh 2;
    """)

    st.write("""##### Заключение""")
    st.write(""" GMSH предоставляет множество инструментов для создания и визуализации геометрий с помощью графического интерфейса. Мы можем использовать GMSH для построения простых геометрических областей, генерации сеток и их визуализации. Визуализация и настройка сетки возможна через интерфейс, что упрощает процесс проектирования. """)

elif choice == "Составные области":

    st.write("""##### Команды организации составных областей""")
    st.write(
            """
            Составные области в Gmsh — это способ объединения нескольких геометрических объектов (линий, поверхностей или объемов) в единый составной объект. 
            Это позволяет упростить работу с сложными геометриями и улучшить качество сетки. 
            
            Основным способом логического объединения объектов для назначения материальных свойств, граничных условий и экспорта меток в решатели являются команды объединения в физические группы(Physical groups). 
            Для управления генерацией стеки используются команды `Compound Curve`, `Compound Surface`, `Compound Volume`. 
            Они указывают Gmsh рассматривать группу объектов как единое целое при построении сетки.

            Команда `Compound Curve` объединяет линии (отрезки, дуги, сплайны) в единую логическую кривую.
            Команда `Compound Surface` объединяет поверхности в группу.
            Команда `Compound Volume` объединяет объемы в логическую группу.
            Таким образом, операции `Compound` осуществляют логическое объединение для управления сеткой, при этом не сохраняются в файле `.msh` как отдельные сущности.



            Для объединения геометрических объектов используются Булевы операции (Boolean Operations ), например, такие как: `BooleanUnion`, `BooleanDifference`

            `BooleanUnion` - создает объект, объединяющий два или более исходных объекта.
            `BooleanDifference` - удаляет из первого объекта все части, пересекающиеся со вторым объектом.
            `BooleanIntersection` - оставляет только область пересечения объектов.
            `BooleanFragments` - разбивает объекты на общие и уникальные части.
            """
            )
    geo_code_07 = """
                SetFactory("OpenCASCADE");

                // Создаем два куба
                Box(1) = {0, 0, 0, 1, 1, 1};
                Box(2) = {1, 0, 0, 1, 1, 1};

                // Объединяем их через BooleanUnion
                BooleanUnion(3) = {Volume{1}; Delete;} {Volume{2}; Delete;};

                // Назначаем физическую группу на результат
                Physical Volume("Merged_Volumes") = {3};

                // Объединяем границы для сетки
                Compound Surface(200) = {1, 2, 5, 6}; // Внешние грани
                Physical Surface("External_Walls") = {Surface{:}};
                
                Mesh.CharacteristicLengthMin = 0.2;
                Mesh 3;
                """
    show_code(geo_code_07,"python")

    def save_example_file():
        example_file_path = './example.geo'
        with open(example_file_path, 'w') as f:
            f.write(geo_code_07)
        return example_file_path

    # Кнопка для загрузки и запуска примера
    if st.button("Пример "):
        example_file_path = save_example_file()
        run_gmsh(example_file_path)


elif choice == "Маркирование подобластей и частей границ":
    
    st.write(
        """
        Физические группы (Physical groups) - именованные наборы геометрических объектов (кривых, поверхностей, объёмов), 
        которые позволяют задавать граничные условия, материалы или другие свойства в численном моделировании.

        """
    )
    st.write("""##### ККоманды выделения физических групп""")
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
    geo_code_7 = """
            SetFactory("OpenCASCADE");

            // Создаем квадрат
            Rectangle(1) = {0, 0, 0, 1, 1};

            // Физические группы (граничные условия)
            Physical Curve("Fixed_Boundary") = {4}; // Левая грань (линия 4)
            Physical Curve("Heat_Flux") = {2};      // Правая грань (линия 2)
            Physical Surface("Domain") = {1};       // Основная область

            // Цвета для граничных условий
            Color Red { Curve{4} };       // Фиксированная грань — красный
            Color Blue { Curve{2} };      // Тепловой поток — синий
            Color LightGray { Surface{1} }; // Область — серый

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

                Color Red { Volume{3} }; 
                Color Blue { Surface{2} };

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

elif choice == "Генерация сетки":
    # Заголовок
    st.markdown("##### Алгоритмы построения 2D сеток")

    # Введение
    st.write("""
    Для генерации поверхностной сетки в Gmsh предлагаются три основных алгоритма: **MeshAdapt**, **Delaunay** и **Frontal**.
    """)

    # Выбор подтемы
    subtopic = st.selectbox(
        "Выберите алгоритм:",  # Текст подсказки
        ["1. MeshAdapt", "2. Delaunay", "3. Frontal"]  # Список опций
    )

    # Содержание подтем
    if subtopic == "1. MeshAdapt":
        st.markdown("###### 1. MeshAdapt")
        st.write("""
        Этот алгоритм предназначен для адаптивного уточнения сетки. Он позволяет локально изменять размер и плотность элементов сетки для обеспечения высокой точности и гибкости.
        """)

        st.markdown("**Основные особенности:**")
        st.write("""
        - **Локальная модификация сетки**: Алгоритм позволяет локально изменять размер и плотность элементов сетки, что важно для сложных геометрий.
        - **Адаптивность**: MeshAdapt хорошо подходит для создания сеток на сложных поверхностях, где требуется высокая точность и гибкость.
        - **Ограничения**: Используется только для двумерных сеток.
        """)

        st.markdown("**Методы адаптации сетки:**")
        st.write("""
        - **Разделение длинных рёбер**: Выбор рёбер, которые превышают максимально допустимую длину или имеют высокий градиент по критериям адаптации, и их разделение для повышения разрешения сетки.
        - **Объединение коротких рёбер**: Выбор рёбер, которые короче минимально допустимой длины, и их объединение для уменьшения количества элементов и снижения вычислительной сложности.
        - **Перестановка рёбер (edge swaps)**: Анализ качества элементов сетки и выполнение перестановок рёбер для улучшения качества элементов.
        """)

    elif subtopic == "2. Delaunay":
        st.markdown("###### 2. Delaunay")
        st.write("""
        Этот алгоритм используется для создания сеток с равномерным размером элементов. Он основан на принципе максимизации углов между ребрами элементов, что приводит к более равномерной сетке.
        """)

        st.markdown("**Основная идея метода:**")
        st.write("""
        Метод Делоне основан на принципе, что для каждого треугольника сетки окружность, описанная вокруг него (вписанная в треугольник окружность), не должна содержать внутри себя других точек сетки. Это гарантирует, что треугольники имеют относительно равностороннюю форму, что важно для качества сетки.
        """)

        st.markdown("**Характеристики метода:**")
        st.write("""
        - **Скорость генерации**: Алгоритм Delaunay в Gmsh считается одним из самых быстрых для построения поверхностных сеток. Это связано с оптимизированной реализацией триангуляции, минимизирующей вычислительные затраты.
        - **Надежность**: Метод демонстрирует высокую устойчивость при работе с объектами сложной геометрии, включая поверхности с резкими перепадами кривизны или встроенными элементами.
        - **Адаптивность**: Позволяет управлять размером элементов через задание локальных параметров (например, минимального/максимального размера рёбер).
        """)

    elif subtopic == "3. Frontal":
        st.markdown("###### 3. Frontal")
        st.write("""
        Этот алгоритм также называют методом продвигаемого фронта. Он используется для генерации двумерных сеток и может обеспечивать высокое качество сетки, особенно для сложных геометрий.
        """)

        st.markdown("**Этапы работы алгоритма:**")
        st.write("""
        - **Инициализация фронта**: Начинается с граничных элементов, которые формируют "фронт" для последующего роста сетки.
        - **Постепенное добавление точек**: Новые точки размещаются вдоль фронта, обеспечивая плавное увеличение размера элементов.
        - **Триангуляция Делоне**: Каждый добавленный элемент проверяется на соответствие условию Делоне (отсутствие точек внутри описанной окружности).
        - **Оптимизация**: Перестановка рёбер (edge swaps) и сглаживание вершин для улучшения качества элементов.
        """)

    st.markdown("""
    ##### Типы сеток в Gmsh:
                
    - Gmsh позволяет строить как структурированные, так и неструктурированные сетки:  
        - **Структурированная (регулярная) сетка** — совокупность сеточных узлов, заданных упорядоченно;
        - **Неструктурированная (нерегулярная) сетка** — совокупность сеточных узлов, заданных неравномерно или неупорядоченно.
        - **Адаптивные сетки**: Gmsh также поддерживает адаптивные методы генерации сеток, которые позволяют изменять размер элементов в зависимости от требований к точности в различных областях модели.
        - **Элементы первого и второго порядка**: Gmsh может генерировать как элементы первого порядка (линейные), так и второго порядка (квадратные), что позволяет улучшить точность расчетов.

    - **Двумерные сетки**:
        Могут быть как структурированными, так и неструктурированными.
      - **Треугольные сетки**: Основной тип сеток для двумерных областей.
      - **Четырехугольные сетки**: Можно преобразовать треугольные сетки в четырехугольные элементы.
    """)


    def generate_mesh(mesh_type, element_type, width, height, nx, ny):
        """Генерация 2D-сетки для прямоугольника"""
        gmsh.initialize()
        gmsh.model.add("rectangle")
        
        # Создание точек
        p1 = gmsh.model.geo.addPoint(0, 0, 0)
        p2 = gmsh.model.geo.addPoint(width, 0, 0)
        p3 = gmsh.model.geo.addPoint(width, height, 0)
        p4 = gmsh.model.geo.addPoint(0, height, 0)
        
        # Создание линий
        l1 = gmsh.model.geo.addLine(p1, p2)
        l2 = gmsh.model.geo.addLine(p2, p3)
        l3 = gmsh.model.geo.addLine(p3, p4)
        l4 = gmsh.model.geo.addLine(p4, p1)
        
        # Создание области
        cl = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
        s = gmsh.model.geo.addPlaneSurface([cl])
        
        gmsh.model.geo.synchronize()
        
        gmsh.model.mesh.setTransfiniteCurve(l1, nx + 1)
        gmsh.model.mesh.setTransfiniteCurve(l2, ny + 1)
        gmsh.model.mesh.setTransfiniteCurve(l3, nx + 1)
        gmsh.model.mesh.setTransfiniteCurve(l4, ny + 1)
        
        if mesh_type == "Структурированная":
            if element_type == "Треугольные":
                gmsh.model.mesh.setTransfiniteSurface(s, "Left")
            elif element_type == "Четырехугольные":
                gmsh.model.mesh.setTransfiniteSurface(s)
        
        gmsh.model.mesh.generate(2)

        if element_type == "Четырехугольные":
            gmsh.model.mesh.recombine()
        
        node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
        element_types, element_tags, element_nodes = gmsh.model.mesh.getElements(2)
        
        gmsh.finalize()
        
        nodes = np.array(node_coords).reshape(-1, 3)[:, :2]
        elements = [np.array(e).reshape(-1, 4 if element_type == "Четырехугольные" else 3) - 1 for e in element_nodes]
        
        return nodes, np.vstack(elements)

    def mesh_worker(mesh_type, element_type, width, height, nx, ny, result_queue):
        nodes, elements = generate_mesh(mesh_type, element_type, width, height, nx, ny)
        result_queue.put((nodes, elements))


    # Основной код Streamlit
    st.write("""##### Генерация 2D-сеток на прямоугольнике с использованием Gmsh""")


    # Выбор типа сетки
    mesh_type = st.selectbox("Тип сетки", ["Структурированная", "Неструктурированная"])

    # Выбор типа элементов
    element_type = st.selectbox("Тип элементов", ["Треугольные", "Четырехугольные"])


    width = st.number_input("Ширина прямоугольника", min_value=1, max_value=100, value=10)
    height = st.number_input("Высота прямоугольника", min_value=1, max_value=100, value=10)
    nx = st.number_input("Число узлов по X", min_value=2, max_value=100, value=10)
    ny = st.number_input("Число узлов по Y", min_value=2, max_value=100, value=10)

    if st.button("Сгенерировать сетку"):
        with multiprocessing.Manager() as manager:
            result_queue = manager.Queue()
            process = multiprocessing.Process(target=mesh_worker, args=(mesh_type, element_type, width, height, nx, ny, result_queue))
            process.start()
            process.join()
            nodes, elements = result_queue.get()
        
        fig, ax = plt.subplots()
        ax.scatter(nodes[:, 0], nodes[:, 1], s=15, color='blue')
        
        for element in elements:
            if np.all(element < len(nodes)):
                polygon = nodes[element]
                polygon = np.vstack([polygon, polygon[0]])  # Замыкаем элемент
                ax.plot(polygon[:, 0], polygon[:, 1], color='black')
        
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.set_aspect('equal')
        st.pyplot(fig)

    # Заголовок страницы
    st.write("""##### Различия между методом Delaunay и методом Frontal""")

    # Введение
    st.write("""
    Методы **Delaunay** и **Frontal** широко используются для генерации сеток. Они отличаются принципами работы, скоростью, качеством элементов и областью применения.
    Выберите интересующий аспект, чтобы узнать подробнее:
    """)

    # Выбор аспекта для сравнения
    aspect = st.selectbox(
        "Выберите аспект сравнения:",
        [
            "Принцип работы",
            "Скорость генерации",
            "Качество элементов",
            "Надёжность",
            "Применение"
        ]
    )

    # Принцип работы
    if aspect == "Принцип работы":
        st.markdown("##### 1. Принцип работы")
        st.write("""
        - **Метод Delaunay**:  
        Основан на триангуляции Delaunay, где каждый треугольник удовлетворяет условию: внутри описанной окружности нет других точек сетки. Это обеспечивает равномерность и высокое качество элементов.
        
        - **Метод Frontal**:  
        Комбинирует фронтальный метод с триангуляцией Delaunay. Начинается с границ объекта и постепенно добавляет новые точки, поддерживая условие Delaunay для каждого нового элемента.
        """)

    # Скорость генерации
    elif aspect == "Скорость генерации":
        st.markdown("##### 2. Скорость генерации")
        st.write("""
        - **Метод Delaunay**:  
        Быстрее, так как использует оптимизированные алгоритмы триангуляции.  
        
        - **Метод Frontal**:  
        Медленнее, так как фронтальный метод требует более сложных вычислений  
        для поддержания качества элементов.
        """)

    # Качество элементов
    elif aspect == "Качество элементов":
        st.markdown("##### 3. Качество элементов")
        st.write("""
        - **Метод Delaunay**:  
        Обеспечивает хорошие, но не всегда оптимальные треугольники.  
        
        - **Метод Frontal**:  
        Генерирует почти равносторонние треугольники, минимизируя искажения. Это особенно важно в задачах с высокими требованиями к точности.
        """)

    # Надёжность
    elif aspect == "Надёжность":
        st.markdown("##### 4. Надёжность")
        st.write("""
        - **Метод Delaunay**:  
        Высокая устойчивость к сложной геометрии.  
        
        - **Метод Frontal**:  
        Средняя устойчивость, возможны трудности с очень сложными геометриями.
        """)

    # Применение
    elif aspect == "Применение":
        st.markdown("##### 5. Применение")
        st.write("""
        - **Метод Delaunay**:  
        Подходит для стандартных задач с умеренными требованиями к качеству сетки.  
        
        - **Метод Frontal**:  
        Используется в задачах, где критично высокое качество элементов:  
            - Аэродинамика  
            - Механика деформируемого тела
            - и т.д.
        """)

    # Итоговое сравнение
    st.markdown("---")
    st.markdown("###### Итоговое сравнение")
    st.write("""
    В целом, метод Delaunay быстрее и более устойчив, но может уступать Frontal по качеству элементов. Выбор метода зависит от требований к точности и сложности геометрии.  
    """)

    # Заголовок страницы
    st.markdown("#### Алгоритмы для построения 3D сеток")

    # Описание
    st.write("""
    Для генерации трехмерных сеток также используются три алгоритма: **Delaunay**, **Frontal** и **HXT**.
    """)

    # Выбор алгоритма
    algorithm = st.selectbox(
        "Выберите алгоритм:",
        ["Алгоритм Делоне", "Алгоритм Frontal", "Алгоритм HXT"]
    )

    # Алгоритм Делоне
    if algorithm == "Алгоритм Делоне":
        st.markdown("##### 1. Алгоритм Делоне для 3D сеток")
        st.write("""
        Алгоритм Делоне, используемый для генерации 3D сеток, является трехмерной версией классического алгоритма Делоне. 
        Он основан на построении **тетраэдральной сетки**, где каждый тетраэдр удовлетворяет **условию Делоне**: внутри сферы, 
        описанной вокруг каждого тетраэдра, не должно быть других точек сетки.
        """)

        st.markdown("###### Этапы работы алгоритма:")
        st.markdown("""
        - **Инициализация**  
        Начинается с создания начальной сетки на основе заданной геометрии, включая определение точек, линий и поверхностей объекта.
        
        - **Триангуляция Делоне для поверхностей**  
        Сначала генерируется двумерная сетка на поверхностях объекта с использованием алгоритма Делоне для обеспечения равномерности и качества элементов.

        - **Тетраэдризация объёма**  
        Затем выполняется тетраэдризация объёма, где алгоритм Делоне используется для построения тетраэдральной сетки внутри объекта. 
        Это включает в себя добавление новых точек и перестроение сетки для удовлетворения условию Делоне.

        - **Оптимизация сетки**  
        После генерации сетки могут быть применены оптимизационные методы, такие как перестановка рёбер и граней, 
        а также сглаживание вершин, для улучшения качества элементов.
        """)

    # Алгоритм Frontal
    elif algorithm == "Алгоритм Frontal":
        st.markdown("##### 2. Алгоритм Frontal для 3D сеток")

        st.markdown("###### Принцип работы:")
        st.write("""
        - Начинается с границ объекта, где создается двумерная сетка.  
        - Затем постепенно добавляются новые точки внутри объёма, поддерживая **условие Делоне** для каждого нового тетраэдра.
        """)

        st.markdown("###### Качество элементов:")
        st.write("""
        - Обеспечивает высокое качество тетраэдральных элементов, близких к равносторонним, что важно для численных методов.
        - Позволяет создавать **смешанные структурированные/неструктурированные сетки**, что полезно для сложных геометрий.
        """)

        st.markdown("###### Скорость и устойчивость:")
        st.write("""
        - Медленнее алгоритма Делоне из-за сложности фронтального подхода.
        - Средняя устойчивость к сложной геометрии, может испытывать трудности с очень сложными объектами.
        """)

        st.markdown("###### Оптимизация:")
        st.write("""
        После генерации сетки могут быть применены **оптимизационные методы**, такие как перестановка рёбер и граней, 
        а также **сглаживание вершин**, для улучшения качества элементов.
        """)

    # Алгоритм HXT
    elif algorithm == "Алгоритм HXT":
        st.markdown("##### 3. Алгоритм HXT")

        st.write("""
        **Алгоритм HXT** — это высокоэффективный метод генерации 3D тетраэдральных сеток. 
        Он был разработан как **параллельная реализация алгоритма Делоне** при помощи OpenMP.
        """)

        st.markdown("###### Характеристики алгоритма HXT:")
        
        st.markdown("""
        - **Параллельная обработка**  
        HXT использует **параллельную обработку** с помощью OpenMP, что позволяет существенно ускорить процесс генерации сеток. 
        Это особенно важно для больших моделей, где традиционные методы могут быть слишком медленными.

        - **Оптимизация сетки**  
        Включает встроенную **оптимизацию сетки**, которая улучшает качество элементов без значительного увеличения времени генерации.  
        Эта оптимизация позволяет получить сетки с высоким качеством, сравнимым с другими алгоритмами.

        - **Скорость генерации**  
        HXT **существенно опережает** другие алгоритмы, такие как Delaunay и Frontal, по скорости генерации сеток.
        """)

    def generate_mesh(mesh_type, element_type, width, height, length, nx, ny, nz):
        """Генерация 3D-сетки"""
        gmsh.initialize()
        gmsh.model.add("mesh")

        # Создание точек
        p1 = gmsh.model.geo.addPoint(0, 0, 0)
        p2 = gmsh.model.geo.addPoint(width, 0, 0)
        p3 = gmsh.model.geo.addPoint(width, height, 0)
        p4 = gmsh.model.geo.addPoint(0, height, 0)
        p5 = gmsh.model.geo.addPoint(0, 0, length)
        p6 = gmsh.model.geo.addPoint(width, 0, length)
        p7 = gmsh.model.geo.addPoint(width, height, length)
        p8 = gmsh.model.geo.addPoint(0, height, length)

        # Создание линий
        lines = [
            gmsh.model.geo.addLine(p1, p2),  # l1
            gmsh.model.geo.addLine(p2, p3),  # l2
            gmsh.model.geo.addLine(p3, p4),  # l3
            gmsh.model.geo.addLine(p4, p1),  # l4
            gmsh.model.geo.addLine(p5, p6),  # l5
            gmsh.model.geo.addLine(p6, p7),  # l6
            gmsh.model.geo.addLine(p7, p8),  # l7
            gmsh.model.geo.addLine(p8, p5),  # l8
            gmsh.model.geo.addLine(p1, p5),  # l9
            gmsh.model.geo.addLine(p2, p6),  # l10
            gmsh.model.geo.addLine(p3, p7),  # l11
            gmsh.model.geo.addLine(p4, p8),  # l12
        ]

        # Создание поверхностей
        curve_loops = [
            gmsh.model.geo.addCurveLoop([lines[0], lines[1], lines[2], lines[3]]),  # cl1
            gmsh.model.geo.addCurveLoop([lines[4], lines[5], lines[6], lines[7]]),  # cl2
            gmsh.model.geo.addCurveLoop([lines[0], lines[9], -lines[4], -lines[8]]),  # cl3
            gmsh.model.geo.addCurveLoop([lines[1], lines[10], -lines[5], -lines[9]]),  # cl4
            gmsh.model.geo.addCurveLoop([lines[2], lines[11], -lines[6], -lines[10]]),  # cl5
            gmsh.model.geo.addCurveLoop([lines[3], lines[8], -lines[7], -lines[11]]),  # cl6
        ]

        surfaces = [gmsh.model.geo.addPlaneSurface([cl]) for cl in curve_loops]

        # Создание объема
        surface_loop = gmsh.model.geo.addSurfaceLoop(surfaces)
        volume = gmsh.model.geo.addVolume([surface_loop])

        gmsh.model.geo.synchronize()

        gmsh.model.mesh.setTransfiniteCurve(lines[0], nx + 1)
        gmsh.model.mesh.setTransfiniteCurve(lines[2], nx + 1)
        gmsh.model.mesh.setTransfiniteCurve(lines[4], nx + 1)
        gmsh.model.mesh.setTransfiniteCurve(lines[6], nx + 1)
        gmsh.model.mesh.setTransfiniteCurve(lines[1], ny + 1)
        gmsh.model.mesh.setTransfiniteCurve(lines[3], ny + 1)
        gmsh.model.mesh.setTransfiniteCurve(lines[5], ny + 1)
        gmsh.model.mesh.setTransfiniteCurve(lines[7], ny + 1)
        gmsh.model.mesh.setTransfiniteCurve(lines[8], nz + 1)
        gmsh.model.mesh.setTransfiniteCurve(lines[9], nz + 1)
        gmsh.model.mesh.setTransfiniteCurve(lines[10], nz + 1)
        gmsh.model.mesh.setTransfiniteCurve(lines[11], nz + 1)
            
        # Настройка сетки
        if mesh_type == "Структурированная":
            gmsh.model.mesh.setTransfiniteSurface(surfaces[0])
            gmsh.model.mesh.setTransfiniteVolume(volume)

        # Генерация сетки
        if element_type == "Тетраэдальные":
            gmsh.model.mesh.generate(3)
        else:
            if mesh_type == "Структурированная":
                if element_type == "Треугольные":
                    for s in surfaces:
                        gmsh.model.mesh.setTransfiniteSurface(s, "Left")
                elif element_type == "Четырехугольные":
                    for s in surfaces:
                        gmsh.model.mesh.setTransfiniteSurface(s)
            
            gmsh.model.mesh.generate(2)

            if element_type == "Четырехугольные":
                gmsh.model.mesh.recombine()
            
        node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
        element_types, element_tags, element_nodes = gmsh.model.mesh.getElements()
            
        nodes = np.array(node_coords).reshape(-1, 3)
        elements = [np.array(e).reshape(-1, 4) - 1 for e in element_nodes]  # Только тетраэдальные элементы
            
        gmsh.finalize()
        
        return nodes, np.vstack(elements)

    def mesh_worker(mesh_type, element_type, width, height, length, nx, ny, nz, result_queue):
        nodes, elements = generate_mesh(mesh_type, element_type, width, height, length, nx, ny, nz)
        result_queue.put((nodes, elements))

    # Основной код Streamlit
    st.markdown("#### Генерация 3D-сеток")
    st.markdown("""
    **Трехмерные сетки**  
    Могут быть как структурированными, так и неструктурированными.  
    Также 3D сетки используются для объемных моделей и являются наиболее распространенными для сложных геометрий.  

    - **Тетраэдральные сетки**: Gmsh поддерживает автоматическую генерацию неструктурированных тетраэдральных сеток.  
    - **Призматические элементы**: Эти элементы могут быть созданы на основе двухмерных четырехугольных сеток, что позволяет создавать более сложные трехмерные структуры.  
    """)

    # Выбор типа сетки
    mesh_type = st.selectbox("Тип сетки", ["Структурированная", "Неструктурированная"], key="mesh_type_select")

    # Выбор типа элементов
    element_type = st.selectbox("Тип элементов", ["Треугольные", "Четырехугольные", "Тетраэдальные"], key="element_type_select")

    # Параметры геометрии
    width = st.number_input("Ширина", min_value=1, max_value=100, value=10)
    height = st.number_input("Высота", min_value=1, max_value=100, value=10)
    length = st.number_input("Длина", min_value=1, max_value=100, value=10)

    # Параметры разбиения
    nx = st.number_input("Число узлов по X", min_value=2, max_value=100, value=10, key="nx_input")
    ny = st.number_input("Число узлов по Y", min_value=2, max_value=100, value=10, key="ny_input")
    nz = st.number_input("Число узлов по Z", min_value=2, max_value=100, value=10, key="nz_input")


    if st.button("Сгенерировать сетку", key="generate_mesh_button"):
        # Проверка: если выбрана структурированная тетраэдальная сетка
        if mesh_type == "Структурированная" and element_type == "Тетраэдальные":
            st.warning("В 3D Gmsh позволяет строить только неструктурированные тетраэдальные сетки. Пожалуйста, не пытайтесь построить структурированные тетраэдальные сетки, оно не будет работать...")
        else:
            with multiprocessing.Manager() as manager:
                result_queue = manager.Queue()
                process = multiprocessing.Process(target=mesh_worker, args=(mesh_type, element_type, width, height, length, nx, ny, nz, result_queue))
                process.start()
                process.join()
                nodes, elements = result_queue.get()
            
            fig = go.Figure()
            
            if element_type in ["Треугольные", "Четырехугольные"]:
                # Визуализация каркасной сетки по граням
                for element in elements:
                    element_closed = np.append(element, element[0])  # Замыкаем элемент
                    fig.add_trace(go.Scatter3d(
                        x=nodes[element_closed, 0],
                        y=nodes[element_closed, 1],
                        z=nodes[element_closed, 2],
                        mode='lines',
                        line=dict(color='red', width=2),
                        showlegend=False  # Убираем из легенды
                    ))
            else:
                # Визуализация объемной сетки
                fig.add_trace(go.Mesh3d(
                    x=nodes[:, 0],
                    y=nodes[:, 1],
                    z=nodes[:, 2],
                    i=elements[:, 0],
                    j=elements[:, 1],
                    k=elements[:, 2],
                    opacity=0.5,
                    color='lightblue',
                    showlegend=False  # Убираем из легенды
                ))

            # Полностью отключаем легенду
            fig.update_layout(showlegend=False)

            # Отображение в Streamlit
            st.plotly_chart(fig)

                


elif choice == "Сгущение сетки":
    # Заголовок
    st.markdown("##### Сгущение сетки")

    # Основной текст
    st.write("""
    **Сгущение сетки** — это процесс, который позволяет увеличить плотность элементов сетки в определенных областях модели, 
    что особенно важно для задач, где требуется высокая точность или присутствуют критические особенности.
    """)

    # Раздел 1: Параметры сгущения
    st.markdown("**1. Параметры сгущения**")
    st.write("""
    **Characteristic Length**: Используется для управления размером элементов. Это делается через скрипты .geo или в графическом интерфейсе Gmsh.
    Скрипты позволяют автоматизировать процесс создания и настройки сетки, что особенно полезно для сложных моделей или при необходимости многократного 
    использования одних и тех же параметров.
    - `Mesh.CharacteristicLengthMin`- используется для сгущения сетки в областях, где требуется высокая точность.
    - `Mesh.CharacteristicLengthMax`- Используется для уменьшения плотности сетки в областях, где высокая точность не требуется. 
    Это помогает сократить количество элементов и, следовательно, вычислительные ресурсы.
    """)

    # Раздел 2: Разбиение элементов
    st.markdown("**2. Разбиение элементов (Refine by splitting):**")
    st.write("""
    Этот метод позволяет разбить существующие элементы сетки на более мелкие внутри себя. Однако он не всегда приводит 
    к качественному разбиению и требует осторожности при использовании.
    """)

    # Раздел 3: Адаптивное сгущение
    st.markdown("**3. Адаптивное сгущение:**")
    st.write("""
    Gmsh поддерживает адаптивное сгущение сетки, когда алгоритмы автоматически увеличивают плотность элементов 
    в областях с высокими градиентами или критическими особенностями.
    """)

    # Раздел 4: Локальное сгущение
    st.markdown("**4. Локальное сгущение:**")
    st.write("""
    Позволяет задавать меньшую характеристическую длину для конкретных точек или линий, что приводит к сгущению сетки 
    в этих областях.
    """)

    # Раздел 5: Применение
    st.markdown("**5. Применение:**")
    st.write("""
    - **Аэродинамика и гидродинамика**: Сгущение сетки используется для моделирования обтекания объектов, где важно 
    точно рассчитать поток в зонах высоких скоростей или давлений;
    - **Механика деформируемого тела**: Сгущение сетки в зонах высоких напряжений или деформаций позволяет улучшить 
    точность моделирования;
    - и т.д.
    """)

    def generate_mesh(mesh_type, element_type, nx, ny):
        """Генерация 2D-сетки для прямоугольника"""
        gmsh.initialize()
        gmsh.model.add("rectangle")
        
        # Фиксированные размеры прямоугольника
        width = 10
        height = 10
        
        # Создание точек
        p1 = gmsh.model.geo.addPoint(0, 0, 0)
        p2 = gmsh.model.geo.addPoint(width, 0, 0)
        p3 = gmsh.model.geo.addPoint(width, height, 0)
        p4 = gmsh.model.geo.addPoint(0, height, 0)
        
        # Создание линий
        l1 = gmsh.model.geo.addLine(p1, p2)
        l2 = gmsh.model.geo.addLine(p2, p3)
        l3 = gmsh.model.geo.addLine(p3, p4)
        l4 = gmsh.model.geo.addLine(p4, p1)
        
        # Создание области
        cl = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
        s = gmsh.model.geo.addPlaneSurface([cl])
        
        gmsh.model.geo.synchronize()
        
        gmsh.model.mesh.setTransfiniteCurve(l1, nx + 1)
        gmsh.model.mesh.setTransfiniteCurve(l2, ny + 1)
        gmsh.model.mesh.setTransfiniteCurve(l3, nx + 1)
        gmsh.model.mesh.setTransfiniteCurve(l4, ny + 1)
        
        if mesh_type == "Структурированная":
            if element_type == "Треугольные":
                gmsh.model.mesh.setTransfiniteSurface(s, "Left")
            elif element_type == "Четырехугольные":
                gmsh.model.mesh.setTransfiniteSurface(s)
        
        gmsh.model.mesh.generate(2)

        if element_type == "Четырехугольные":
            gmsh.model.mesh.recombine()
        
        node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
        element_types, element_tags, element_nodes = gmsh.model.mesh.getElements(2)
        
        gmsh.finalize()
        
        nodes = np.array(node_coords).reshape(-1, 3)[:, :2]
        elements = [np.array(e).reshape(-1, 4 if element_type == "Четырехугольные" else 3) - 1 for e in element_nodes]
        
        return nodes, np.vstack(elements)

    def mesh_worker(mesh_type, element_type, nx, ny, result_queue):
        nodes, elements = generate_mesh(mesh_type, element_type, nx, ny)
        result_queue.put((nodes, elements))


    # Основной код Streamlit
    st.markdown("##### Пример сгущения 2D-сеток на границе")

    # Выбор типа сетки
    mesh_type = st.selectbox("Тип сетки", ["Структурированная", "Неструктурированная"])

    # Выбор типа элементов
    element_type = st.selectbox("Тип элементов", ["Треугольные", "Четырехугольные"])

    # Количество узлов по осям X и Y
    nx = st.number_input("Число узлов по X", min_value=2, max_value=100, value=10)
    ny = st.number_input("Число узлов по Y", min_value=2, max_value=100, value=10)

    if st.button("Сгенерировать сетку"):
        with multiprocessing.Manager() as manager:
            result_queue = manager.Queue()
            process = multiprocessing.Process(target=mesh_worker, args=(mesh_type, element_type, nx, ny, result_queue))
            process.start()
            process.join()
            nodes, elements = result_queue.get()
            
        fig, ax = plt.subplots()
        ax.scatter(nodes[:, 0], nodes[:, 1], s=15, color='blue')
            
        for element in elements:
            if np.all(element < len(nodes)):
                polygon = nodes[element]
                polygon = np.vstack([polygon, polygon[0]])  # Замыкаем элемент
                ax.plot(polygon[:, 0], polygon[:, 1], color='black')
            
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        st.pyplot(fig)


elif choice == "Подготовка сетки для FEniCS":
    st.markdown("##### Поддерживаемые сеточные форматы:")
    st.markdown("###### 1. Собственный формат FEniCS (XML):")
    st.write("""
    
    - FEniCS изначально использует XML-формат для хранения сеток и данных.
    - Примеры файлов:
        - `mesh.xml` — файл сетки.
        - `mesh_facet_region.xml` — файл с метками граничных элементов.
        - `mesh_physical_region.xml` — файл с метками физических областей.
    - Эти файлы создаются с помощью утилиты `dolfin-convert` или вручную.
    """)
    st.markdown("###### 2. Форматы, поддерживаемые через `dolfin-convert`:")
    st.write("""
    
    Утилита dolfin-convert позволяет конвертировать сетки из других форматов в формат, понятный FEniCS. 
    - Поддерживаемые форматы:
        - **Gmsh (.msh):** Популярный формат для генерации сеток.
        - **MEDIT (.mesh):** Формат, используемый в программе MEDIT.
        - **Triangle (.node, .ele):** Формат, используемый в программе Triangle для 2D-сеток.
        - **TetGen (.node, .ele):** Формат, используемый в программе TetGen для 3D-сеток.
    Пример использования `dolfin-convert`:
    ```bash
              dolfin-convert input_mesh.msh output_mesh.xml
              
              """)
    st.markdown("###### 3. Форматы, поддерживаемые через `meshio`:")
    st.write("""
    
    Библиотека `meshio` предоставляет более широкую поддержку форматов и может использоваться для конвертации сеток в формат, совместимый с FEniCS. Поддерживаемые форматы:
    - Поддерживаемые форматы:
        - **Gmsh (.msh):**
        - **VTK (.vtk, .vtu)**
        - **XDMF (.xdmf)**
        - **ABAQUS (.inp)**
        - **COMSOL (.mphtxt)**
        - **STL (.stl)**
        - **MED (.med)**
        - и многие другие.
        
    Пример использования `meshio` для конвертации в формат XML:
    ```bash
            import meshio
            # Чтение сетки из формата Gmsh
            mesh = meshio.read("input_mesh.msh")
            # Запись сетки в формат FEniCS (XML)
            meshio.write("output_mesh.xml", mesh)
    """)
    st.write("""
    Пример импортирования сетки в FEniCS:
    ```bash
            from fenics import *
            # Загрузка сетки
            mesh = Mesh("mesh.xml")
            # Визуализация сетки
            plot(mesh)
            plt.title("Imported Mesh from Gmsh")
            plt.show()
    """)

    st.markdown("###### 4. Формат XDMF:")
    st.write("""
    
    - XDMF (eXtensible Data Model and Format) — это современный формат, который поддерживает хранение сеток и данных (например, результатов вычислений).
    - FEniCS может читать и записывать XDMF-файлы, что особенно полезно для больших сеток и параллельных вычислений.
    - Пример использования:
    ```bash
            from dolfin import *
            # Чтение сетки из XDMF
            mesh = Mesh()
            with XDMFFile("mesh.xdmf") as infile:
                infile.read(mesh)
            # Запись сетки в XDMF
            with XDMFFile("output_mesh.xdmf") as outfile:
                outfile.write(mesh)
              """)

    st.markdown("###### 5. Формат VTK:")
    st.write("""
    
    - VTK (Visualization Toolkit) — это формат, используемый для визуализации данных. 
    - FEniCS может экспортировать результаты в VTK для визуализации в программах, таких как Paraview.
    - Пример использования:
    ```bash
            from dolfin import *

            # Создание функции и экспорт в VTK
            mesh = UnitSquareMesh(10, 10)
            V = FunctionSpace(mesh, 'P', 1)
            u = Function(V)
            File("output.pvd") << u
              """)
              
    st.markdown("###### 6. Другие форматы:")
    st.write("""
    
    - **HDF5**: Используется для хранения больших данных и сеток в параллельных вычислениях. 
    - **DOLFIN HDF5**: Специальный формат для хранения сеток и данных в FEniCS.
    - **NETCDF:** Поддерживается для работы с данными.
              """)
    st.markdown("###### Некоторые рекомендации:")
    st.write("""
    
    - Для простых задач использовать XML-формат. 
    - Для больших сеток и параллельных вычислений лучше подходят XDMF или HDF5.
    - Для конвертации сеток из других форматов использовать `meshio`, так как оно поддерживает больше форматов, чем `dolfin-convert`.
              """)
    st.markdown("###### Пример подготовки сетки с граничными условиями:")
    st.write("""
    ```bash
    import meshio

    # Чтение .msh файла
    mesh = meshio.read("mesh_with_bc.msh")
    # Запись в .xdmf формат
    meshio.write("mesh_with_bc.xdmf", mesh)
    from fenics import *

    # Загрузка сетки
    mesh = Mesh()
    with XDMFFile("mesh_with_bc.xdmf") as infile:
        infile.read(mesh)

    # Загрузка граничных меток
    boundaries = MeshFunction("size_t", mesh, mesh.topology().dim() - 1)
    with XDMFFile("mesh_with_bc_boundaries.xdmf") as infile:
        infile.read(boundaries)

    # Определение граничных условий
    u_D = Constant(0.0)
    bc = DirichletBC(V, u_D, boundaries, 1)  # 1 — идентификатор границы

    # Визуализация граничных меток
    plot(boundaries)
    plt.title("Boundary Markers")
    plt.show()
              """)
    
    st.markdown("###### Итоги:")
    st.write("""

    - Для подготовки сетки в FEniCS нужно использовать Gmsh, `mshr` или другие инструменты. 
    - Конвертировать сетку в формат `.xml` или `.xdmf` с помощью `meshio` или `dolfin-convert`.
    - Загрузить сетку в FEniCS и определить граничные условия с помощью физических групп.
              """)

elif choice == "Constructive Solid Geometry технология в Gmsh":

    st.write("""**Constructive Solid Geometry (CSG)** — это технология, используемая для создания сложных геометрических моделей путём комбинирования простых фигур (примитивов) с помощью **булевых операций**: **объединение (union)**, **вычитание (difference)** и **пересечение (intersection)**. В Gmsh эта технология активно применяется для построения геометрии.""")
    st.markdown("###### Пример использования CSG в Gmsh")
    st.write("""Создадим геометрию состоящую из прямоугольников с круглым отверстием внутри, используя CSG.""")
    st.write("""
    1. **Создание примитивов:**
        - Прямоугольник (Rectangle).
        - Круг (Disk)
    2. **Применение булевых операций:**
        - Используем операцию **вычитания (Difference)**, чтобы удалить круг из прямоугольника.""")
        
    st.write("""
        Пример кода в Gmsh:
        ```bash
        // Включаем OpenCASCADE
        SetFactory("OpenCASCADE");

        // Создание прямоугольной поверхности
        Rectangle(1) = {0, 0, 0, 2, 1, 0};

        // Создание круглой поверхности (диска)
        Disk(2) = {1, 0.5, 0, 0.25};

        // Вычитание диска из прямоугольника
        BooleanDifference(3) = { Surface{1}; Delete; }{ Surface{2}; Delete; };

        // Генерация 2D-сетки
        Mesh 2;
    """)

    if st.button("Пример 1"):    
        run_gmsh("rectangle_geometry.geo")
            
    st.write("""
            Объяснение кода:
            1. **Rectangle(1):**
            - Создает прямоугольник с координатами левого нижнего угла (0,0) и размерами 2 (по оси Х) на 1 (по оси Y).
            2. **Circle(2):**
            - Создает круг с центром в точке (1, 0.5) и радиусом 0.25.
            3. **BooleanDifference(3):**
            - Вычитает круг (Surface{2}) из прямоугольника (Surface{1}), создавая новую поверхность (Surface{3}).
            4. **Mesh 2:**
            - Генерирует 2D-сетку для полученной геометрии.""")
    
    st.markdown("###### Применение CSG в построении геометрии:")
    st.write("""
            CSG особенно полезна в задачах, где требуется создание сложных форм из простых примитивов.
            Примеры применения:
            1. **Инженерные конструкции:**
                - Создание деталей с отверстиями, пазами или сложными формами.
                - Пример: пластина с отверстиями для крепления.
            2. **Архитектурное моделирование:**
                - Построение зданий с окнами, дверьми и другими элементами.
                - Пример: здание с арочными проёмами.
            3. **Биомедицинское моделирование:**
                - Создание моделей органов или имплантатов.
                - Пример: кость с полостью для имплантата.
            4. **Физическое моделирование:**
                - Построение геометрии для задач CFD (вычислительной гидродинамики) или FEM (метода конечных элементов).
                - Пример: труба с внутренними перегородками.""")
            

    st.markdown("###### Преимущества CSG:")
    st.write("""
        - **Простота:** Использование простых примитивов (кубы, сферы, цилиндры) для создания сложных форм.
        - **Гибкость:** Возможность комбинировать фигуры с помощью булевых операций.
        - **Точность:** Точное задание геометрии, что важно для численного моделирования.
    """)
    
    st.markdown("###### Пример сложной геометрии с использованием CSG:")
    st.write("""
    Создадим геометрию, состоящую из двух пересекающихся цилиндров (труб).

    **Код в Gmsh:**
    ```bash
    // Включаем OpenCASCADE
    SetFactory("OpenCASCADE");
    // Создание первого цилиндра
    Cylinder(1) = {0, 0, 0, 2, 0, 0, 0.5, 2*Pi};
    // Центр (0,0,0), ось (2,0,0), радиус 0.5

    // Создание второго цилиндра
    Cylinder(2) = {1, -1, 0, 0, 2, 0, 0.5, 2*Pi};
    // Центр (1,-1,0), ось (0,2,0), радиус 0.5

    // Применение булевой операции Union
    BooleanUnion(3) = { Volume{1}; Delete; }{ Volume{2}; Delete; };

    // Генерация 3D-сетки
    Mesh 3;

    """)
    
    if st.button("Пример 2"):    
        run_gmsh("complex_geometry.geo")

    st.markdown("###### Итоги:")
    st.write("""
            CSG — это мощный инструмент для создания сложных геометрий в Gmsh. Он позволяет комбинировать простые фигуры с помощью булевых операций, что делает его незаменимым для инженерных, архитектурных и научных задач.""")

elif choice == "Библиотеки Python pygmsh и meshio":

    st.write("""
    `pygmsh` — это Python-интерфейс для работы с `gmsh`, популярной open-source программой для генерации сеток.
    Он позволяет создавать геометрии и генерировать сетки с использованием Python, что делает процесс более гибким и интегрируемым.
    """)

    # Основные возможности
    st.markdown("##### Основные возможности `pygmsh`")
    st.write("""
    - Создание геометрий: точки, линии, поверхности, объемы.
    - Генерация сеток: 1D, 2D, 3D.
    - Поддержка булевых операций: объединение, вычитание, пересечение.
    - Экспорт сеток в форматы `.msh`, `.vtk`, `.stl` и другие.
    - Интеграция с Python-библиотеками: `numpy`, `scipy`, `matplotlib`, `meshio`.
    """)

    # Основные функции
    st.markdown("###### 1. Точки")
    st.write("""
    - **`add_point()`**: Добавляет точку в геометрию. Параметры: координаты `[x, y, z]` и опционально **`mesh_size`** (размер элемента сетки).
    """)
    st.code("""
    p1 = geom.add_point([0.0, 0.0, 0.0], mesh_size=0.1)
    """, language="python")

    st.write("""- Аналог в **gmsh**
    """)

    st.code("""
    Point(1) = {0.0, 0.0, 0.0, 0.1};
    """, language="python")

    st.markdown("###### 2. Линии")
    st.write("""
    - **`add_line()`**: Создает линию между двумя точками. **`add_circle_arc()`**: Создает дугу окружности.
    """)
    st.code("""
    l1 = geom.add_line(p1, p2)
    arc = geom.add_circle_arc(p1, p2, p3)
    """, language="python")

    st.write("""- Аналог в **gmsh**""")

    st.code("""
    Line(1) = {1, 2};
    Circle(1) = {1, 2, 3};
    """, language="python")

    st.markdown("###### 3. Кривые и контуры")
    st.write("""
    - **`add_curve_loop()`**: Создает замкнутый контур из линий или кривых.
    """)
    st.code("""
    loop = geom.add_curve_loop([l1, l2, l3, l4])
    """, language="python")

    st.write("""- Аналог в **gmsh**
    """)

    st.code("""
    Curve Loop(1) = {1, 2, 3, 4};
    """, language="python")

    st.markdown("###### 4. Поверхности")
    st.write("""
    - **`add_plane_surface()`**: Создает плоскую поверхность внутри замкнутого контура.
    """)
    st.code("""
    surface = geom.add_plane_surface(loop)
    """, language="python")

    st.write("""- Аналог в **gmsh**
    """)

    st.code("""
    Plane Surface(1) = {1};
    """, language="python")

    st.markdown("###### 5. Объемы")
    st.write("""
    - **`add_volume()`**: Создает объем на основе поверхностей.
    """)
    st.code("""
    volume = geom.add_volume([surface1, surface2])
    """, language="python")

    st.write("""- Аналог в **gmsh**
    """)

    st.code("""
    Volume(1) = {1, 2};
    """, language="python")

    st.markdown("###### 6. Булевы операции")
    st.write("""
    - **`boolean_union()`**: Объединяет объекты.

    - **`boolean_difference()`**: Вычитает один объект из другого.

    - **`boolean_intersection()`**: Находит пересечение объектов.
    """)
    st.code("""
    result = geom.boolean_union([obj1, obj2])
    result = geom.boolean_difference(obj1, obj2)
    result = geom.boolean_intersection([obj1, obj2])
    """, language="python")

    st.write("""- Аналог в **gmsh**
    """)

    st.code("""
    BooleanUnion{ Surface{1}; Delete; }{ Surface{2}; Delete; }
    BooleanDifference{ Surface{1}; Delete; }{ Surface{2}; Delete; }
    BooleanIntersection{ Surface{1}; Delete; }{ Surface{2}; Delete; }
    """, language="python")

    st.markdown("###### 7. Физические группы")
    st.write("""
    - **`add_physical_group()`**: Группирует объекты для задания физических свойств.
    """)
    st.code("""
    phys_group = geom.add   _physical_group("Line", [l1, l2])
    """, language="python")

    st.write("""- Аналог в **gmsh**
    """)

    st.code("""
    Physical Line(1) = {1, 2};
    """, language="python")

    def run_python_script_1():
        result = subprocess.run(['python3', 'gmsh_example.py'], capture_output=True, text=True)

    def run_python_script_2():
        
        result = subprocess.run(['python3', 'p_example.py'], capture_output=True, text=True)
        

    # Кнопка для запуска скрипта
    if st.button('Запустить пример 1'):
        output = run_python_script_1()

    # Кнопка для запуска скрипта
    if st.button('Запустить пример 2'):
        output = run_python_script_2()

    # Сравнение с `gmsh`
    st.markdown("##### Сравнение `pygmsh` и `gmsh`")
    st.write("""
    | Характеристика               | `pygmsh`                                                                 | `gmsh`                                                                 |
    |------------------------------|--------------------------------------------------------------------------|------------------------------------------------------------------------|
    | **Интерфейс**                | Python-интерфейс, удобен для интеграции с Python-библиотеками.           | Собственный скриптовый язык (.geo файлы) и графический интерфейс.      |
    | **Гибкость**                 | Высокая, благодаря использованию Python.                                 | Ограничена синтаксисом .geo файлов.                                    |
    | **Создание сложных геометрий**| Удобно использовать циклы и условия Python.                             | Требуется ручное описание в .geo файлах.                               |
    | **Интеграция с другими инструментами** | Легко интегрируется с `numpy`, `scipy`, `matplotlib`, `meshio`.      | Требуется экспорт/импорт данных.                                       |
    | **Поддержка форматов**       | Поддерживает экспорт в `.msh`, `.vtk`, `.stl` и другие.                 | Поддерживает множество форматов, включая `.msh`, `.stl`, `.step`.      |
    | **Производительность**       | Немного медленнее из-за Python-обертки.                                 | Высокая, так как это нативный C++ код.                                 |
    """)

    st.markdown("##### Что такое `meshio`?")
    st.write("""
    `meshio` — это библиотека для работы с файлами сеток (mesh files) в Python. Она предоставляет унифицированный интерфейс для чтения, записи и обработки сеток в различных форматах, таких как `.msh`, `.vtk`, `.stl`, `.xdmf` и многих других.
    """)

    # Основные возможности
    st.markdown("##### Основные возможности `meshio`")
    st.write("""
    - **Чтение и запись сеток**: Поддержка более 30 форматов.
    - **Унифицированная структура данных**: Точки, ячейки и данные.
    - **Поддержка различных типов ячеек**: Треугольники, тетраэдры, линии и другие.
    - **Обработка данных**: Добавление, удаление или изменение данных.
    - **Конвертация между форматами**: Упрощает преобразование сеток.
    - **Интеграция с другими библиотеками**: `numpy`, `scipy`, `matplotlib`, `pyvista`.
    """)

    # Поддерживаемые форматы
    st.markdown("##### Поддерживаемые форматы")
    st.write("""
    `meshio` поддерживает множество форматов, включая:
    - **Gmsh**: `.msh`
    - **VTK**: `.vtk`, `.vtu`
    - **STL**: `.stl`
    - **XDMF**: `.xdmf`, `.xmf`
    - **OBJ**: `.obj`
    - **OFF**: `.off`
    - **PLY**: `.ply`
    - **ABAQUS**: `.inp`
    - **ANSYS**: `.cdb`
    - **и многие другие**.
    """)

    # Сравнение с другими библиотеками
    st.markdown("##### Сравнение с другими библиотеками")
    st.write("""
    | Характеристика               | `meshio`                                                                 | Другие библиотеки (например, `pyvista`, `vtk`)                        |
    |------------------------------|--------------------------------------------------------------------------|------------------------------------------------------------------------|
    | **Поддержка форматов**       | Более 30 форматов.                                                       | Ограниченное количество форматов.                                      |
    | **Удобство использования**   | Простой и понятный API.                                                  | Может требовать больше кода для выполнения аналогичных задач.          |
    | **Интеграция с Python**      | Полная интеграция с `numpy`, `scipy`, `matplotlib`, `pyvista`.           | Зависит от библиотеки.                                                |
    | **Обработка данных**         | Поддержка point data и cell data.                                        | Ограниченная поддержка данных.                                         |
    | **Производительность**       | Высокая, но может уступать нативным библиотекам (например, `vtk`).       | Высокая, особенно для нативных библиотек.                              |
    """)

    
