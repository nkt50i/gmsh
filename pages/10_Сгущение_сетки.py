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
st.set_page_config(page_title="֎", layout="wide")

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
    "Сгущение сетки": "",
    "Пример сгущения 2D-сеток на границе": "",
}

choice = st.sidebar.radio("Выберите раздел", list(sections.keys()))


if choice == "Сгущение сетки":
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
    **Characteristic Length**: используется для управления размером элементов. Это делается через скрипты .geo или в графическом интерфейсе Gmsh.
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
    - **Аэродинамика и гидродинамика**: сгущение сетки используется для моделирования обтекания объектов, где важно 
    точно рассчитать поток в зонах высоких скоростей или давлений;
    - **Механика деформируемого тела**: сгущение сетки в зонах высоких напряжений или деформаций позволяет улучшить 
    точность моделирования;
    - и т.д.
    """)


elif choice == "Пример сгущения 2D-сеток на границе":
    # Основной код Streamlit
    st.markdown("##### Пример сгущения 2D-сеток на границе")

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