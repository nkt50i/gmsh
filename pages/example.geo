
                SetFactory("OpenCASCADE");

                // Создаем два куба
                Box(1) = {0, 0, 0, 1, 1, 1};
                Box(2) = {1, 0, 0, 1, 1, 1};

                // Объединяем их через BooleanUnion
                BooleanUnion(3) = {Volume{1}; Delete;} {Volume{2}; Delete;};
                Physical Surface("External_Walls") = {Surface{:}};

                // Назначаем физическую группу на результат
                Physical Volume("Merged_Volumes") = {3};

                // Объединяем границы для сетки
                Compound Surface(200) = {1, 2, 5, 6}; // Внешние грани
                Physical Surface("External_Walls") = {200};
                
                Mesh.CharacteristicLengthMin = 0.2;
                Geometry.PointNumbers = 1;
                Geometry.SurfaceNumbers = 2;
                Geometry.VolumeNumbers = 3;
                Geometry.Color.Points = {160, 255, 0};
                General.Color.Text = White;
                Geometry.Color.Surfaces = Geometry.Color.Points;
                Mesh 3;
                