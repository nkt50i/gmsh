// Включаем OpenCASCADE
SetFactory("OpenCASCADE");

// Создание прямоугольной поверхности
Rectangle(1) = {0, 0, 0, 2, 1, 0};

// Создание круглого отверстия (диска)
Disk(2) = {1, 0.5, 0, 0.25};

// Вычитание диска из прямоугольника (удаляем исходные поверхности)
BooleanDifference(3) = { Surface{1}; Delete; }{ Surface{2}; Delete; };

// Контроль размера сетки (разбиение на мелкие элементы)
Mesh.CharacteristicLengthMax = 0.05; // Максимальный размер элемента
Mesh.CharacteristicLengthMin = 0.02; // Минимальный размер элемента

// Улучшение качества сетки
Mesh.Algorithm = 5;      // Алгоритм Delaunay
Mesh.Optimize = 1;       // Включить оптимизацию
Mesh.OptimizeNetgen = 1; // Дополнительное улучшение сетки

// Генерация сетки
Mesh 2;
    