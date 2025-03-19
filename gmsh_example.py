import gmsh

# Инициализация GMSH
gmsh.initialize()

# Задание разрешения сетки
resolution = 0.01

# Параметры канала
L = 2.2
H = 0.41
c = [0.2, 0.2, 0]
r = 0.05

# Создание новой модели
model = gmsh.model
model.add("channel")

# Добавление окружности
circle = model.occ.addCircle(c[0], c[1], c[2], r)
circle_loop = model.occ.addCurveLoop([circle])

# Добавление точек для канала
points = [
    model.occ.addPoint(0, 0, 0, meshSize=5 * resolution),
    model.occ.addPoint(L, 0, 0, meshSize=5 * resolution),
    model.occ.addPoint(L, H, 0, meshSize=5 * resolution),
    model.occ.addPoint(0, H, 0, meshSize=5 * resolution),
]

# Добавление линий между точками для создания прямоугольника
channel_lines = [
    model.occ.addLine(points[i], points[i + 1]) for i in range(3)
]
channel_lines.append(model.occ.addLine(points[3], points[0]))

# Создание контура и поверхности для сетки
channel_loop = model.occ.addCurveLoop(channel_lines)
plane_surface = model.occ.addPlaneSurface([channel_loop, circle_loop])

# Синхронизация модели
model.occ.synchronize()

# Добавление физических групп
volume_marker = 6
model.addPhysicalGroup(2, [plane_surface], volume_marker)
model.addPhysicalGroup(1, [channel_lines[0]], 1)  # Входной поток
model.addPhysicalGroup(1, [channel_lines[2]], 2)  # Выходной поток
model.addPhysicalGroup(1, [channel_lines[1], channel_lines[3]], 3)  # Стенки
model.addPhysicalGroup(1, [circle], 4)  # Препятствие

# Настройка параметров сетки для использования криволинейных элементов (второго порядка)
gmsh.option.setNumber("Mesh.ElementOrder", 2)  # Использовать элементы второго порядка
gmsh.option.setNumber("Mesh.SecondOrderLinear", 0)  # Гарантировать использование криволинейных элементов

# Создание поля размера для уточнения сетки вблизи окружности
# 1. Создание поля расстояния для измерения расстояния от окружности
distance_field = model.mesh.field.add("Distance")
model.mesh.field.setNumbers(distance_field, "CurvesList", [circle])

# 2. Создание порогового поля для задания размера сетки в зависимости от расстояния
threshold_field = model.mesh.field.add("Threshold")
model.mesh.field.setNumber(threshold_field, "IField", distance_field)
model.mesh.field.setNumber(threshold_field, "LcMin", resolution)  # Минимальный размер элементов вблизи окружности
model.mesh.field.setNumber(threshold_field, "LcMax", 5 * resolution)  # Максимальный размер элементов вдали от окружности
model.mesh.field.setNumber(threshold_field, "DistMin", r)  # Начало области уточнения на границе окружности
model.mesh.field.setNumber(threshold_field, "DistMax", 2 * r)  # Конец области уточнения на расстоянии 2*r от окружности

# 3. Установка порогового поля как фонового поля размера сетки
model.mesh.field.setAsBackgroundMesh(threshold_field)

# Генерация 2D сетки
model.mesh.generate(2)

# Запись сетки в файл
gmsh.write("meshik.msh")

# Опционально: визуализация сетки в графическом интерфейсе GMSH
gmsh.fltk.run()

# Очистка модели и завершение работы GMSH
gmsh.clear()
gmsh.finalize()