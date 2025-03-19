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