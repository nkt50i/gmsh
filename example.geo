
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

                