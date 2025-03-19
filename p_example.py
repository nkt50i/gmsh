import meshio
import gmsh
import pygmsh

# Задание разрешения сетки
resolution = 0.01

# Параметры канала
L = 2.2  # Длина канала
H = 0.41  # Высота канала
c = [0.2, 0.2, 0]  # Центр окружности
r = 0.05  # Радиус окружности

# Инициализация пустой геометрии с использованием встроенного ядра GMSH
geometry = pygmsh.geo.Geometry()

# Получение модели, к которой будем добавлять данные
model = geometry.__enter__()

# Добавление окружности
circle = model.add_circle(c, r, mesh_size=resolution)

# Добавление точек с более крупной сеткой на левой стороне
points = [
    model.add_point((0, 0, 0), mesh_size=5 * resolution),  # Левая нижняя точка
    model.add_point((L, 0, 0), mesh_size=5 * resolution),  # Правая нижняя точка
    model.add_point((L, H, 0), mesh_size=5 * resolution),  # Правая верхняя точка
    model.add_point((0, H, 0), mesh_size=5 * resolution),  # Левая верхняя точка
]

# Добавление линий между точками для создания прямоугольника
channel_lines = [
    model.add_line(points[i], points[i + 1]) for i in range(-1, len(points) - 1)
]

# Создание контура и поверхности для сетки
channel_loop = model.add_curve_loop(channel_lines)
plane_surface = model.add_plane_surface(channel_loop, holes=[circle.curve_loop])

# Синхронизация модели перед добавлением физических объектов
model.synchronize()

# Добавление физических групп
volume_marker = 6
model.add_physical([plane_surface], "Volume")  # Физическая группа для объёма
model.add_physical([channel_lines[0]], "Inflow")  # Физическая группа для входного потока
model.add_physical([channel_lines[2]], "Outflow")  # Физическая группа для выходного потока
model.add_physical([channel_lines[1], channel_lines[3]], "Walls")  # Физическая группа для стенок
model.add_physical(circle.curve_loop.curves, "Obstacle")  # Физическая группа для препятствия

# Генерация 2D сетки
geometry.generate_mesh(dim=2)

# Запись сетки в файл
gmsh.write("mesh.msh")

# Очистка модели и завершение работы
gmsh.clear()
geometry.__exit__()
