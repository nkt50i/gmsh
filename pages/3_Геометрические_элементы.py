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

st.set_page_config(page_title="🌐 ", layout="wide")

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

st.write("""##### Геометрические элементы""")
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
         - С помощью встроенной библиотеки геометрии создается сплайн Catmull-Rom.
         - С помощью библиотеки OpenCASCADE создается BSpline.
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
         - Со встроенной библиотекой геометрии дуга должна быть строго меньше числа π.
         - С библиотекой OpenCASCADE, если указано от 4 до 6 точек, первые три определяют координаты центра, следующие определяет радиус, а последние 2 определяют угол.
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
         - С библиотекой OpenCASCADE, если указано от 5 до 7 выражений, первые три определяют координаты центра, следующие два определяют большой (вдоль оси x) и малый радиусы (вдоль оси y), а следующие два — начальный и конечный угол.
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
             - С помощью встроенной геометрической библиотеки кривые должны быть упорядочены и ориентированы, используя отрицательные теги для указания обратной ориентации.
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
         - С помощью встроенной геометрической библиотеки кривые должны быть упорядочены и ориентированы, используя отрицательные теги для указания обратной ориентации.
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

        // Настройки сетки
        Geometry.PointNumbers = 1;
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
         - Поверхность Безье доступна только с библиотекой OpenCASCADE.
         - Поверхность Сплайнов доступна только с библиотекой OpenCASCADE.
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

        // Настройки цветов
        Geometry.PointNumbers = 1;
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

        // Строим отрезки
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

        // Создаем замкнутый контур поверхностей
        Surface Loop(25) = {14, 16, 18, 20, 22, 24};

        // Настройки цветов
        Geometry.PointNumbers = 1;
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
        Line(2) = {2, 3}; 
        Line(3) = {3, 4};
        Line(4) = {4, 1};

        Curve Loop(1) = {4, 1, -2, 3};
        Plane Surface(1) = {1};

        Physical Curve(5) = {1, 2, 4};

        Physical Surface("My surface") = {1};


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
         - Сфера доступна только с библиотекой OpenCASCADE.
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
         - Доступен только с библиотекой OpenCASCADE.
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
         - Доступен только с библиотекой OpenCASCADE.
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
         - Доступен только с библиотекой OpenCASCADE.
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
         - Доступен только с библиотекой OpenCASCADE.
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
         - Доступен только с библиотекой OpenCASCADE.
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