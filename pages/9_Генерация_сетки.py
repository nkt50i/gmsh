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
st.set_page_config(page_title="⌗", layout="wide")

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
    "Алгоритмы построения 2D сеток": "",
    "Типы сеток в Gmsh": "",
    "Генерация 2D-сеток на прямоугольнике с использованием Gmsh": "",
    "Различия между методом Delaunay и методом Frontal": "",
    "Алгоритмы для построения 3D сеток": "",
    "Генерация 3D-сеток": ","
}

choice = st.sidebar.radio("Выберите раздел", list(sections.keys()))

if choice == "Алгоритмы построения 2D сеток":
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

elif choice == "Типы сеток в Gmsh":
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

elif choice == "Генерация 2D-сеток на прямоугольнике с использованием Gmsh":

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


elif choice == "Различия между методом Delaunay и методом Frontal":

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
        st.markdown("###### 1. Принцип работы")
        st.write("""
        - **Метод Delaunay**:  
        Основан на триангуляции Delaunay, где каждый треугольник удовлетворяет условию: внутри описанной окружности нет других точек сетки. Это обеспечивает равномерность и высокое качество элементов.
        
        - **Метод Frontal**:  
        Комбинирует фронтальный метод с триангуляцией Delaunay. Начинается с границ объекта и постепенно добавляет новые точки, поддерживая условие Delaunay для каждого нового элемента.
        """)

    # Скорость генерации
    elif aspect == "Скорость генерации":
        st.markdown("###### 2. Скорость генерации")
        st.write("""
        - **Метод Delaunay**:  
        Быстрее, так как использует оптимизированные алгоритмы триангуляции.  
        
        - **Метод Frontal**:  
        Медленнее, так как фронтальный метод требует более сложных вычислений  
        для поддержания качества элементов.
        """)

    # Качество элементов
    elif aspect == "Качество элементов":
        st.markdown("###### 3. Качество элементов")
        st.write("""
        - **Метод Delaunay**:  
        Обеспечивает хорошие, но не всегда оптимальные треугольники.  
        
        - **Метод Frontal**:  
        Генерирует почти равносторонние треугольники, минимизируя искажения. Это особенно важно в задачах с высокими требованиями к точности.
        """)

    # Надёжность
    elif aspect == "Надёжность":
        st.markdown("###### 4. Надёжность")
        st.write("""
        - **Метод Delaunay**:  
        Высокая устойчивость к сложной геометрии.  
        
        - **Метод Frontal**:  
        Средняя устойчивость, возможны трудности с очень сложными геометриями.
        """)

    # Применение
    elif aspect == "Применение":
        st.markdown("###### 5. Применение")
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

elif choice == "Алгоритмы для построения 3D сеток":
    # Заголовок страницы
    st.markdown("##### Алгоритмы для построения 3D сеток")

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
        st.markdown("###### 1. Алгоритм Делоне для 3D сеток")
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


elif choice == "Генерация 3D-сеток":
    # Основной код Streamlit
    st.markdown("##### Генерация 3D-сеток")
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