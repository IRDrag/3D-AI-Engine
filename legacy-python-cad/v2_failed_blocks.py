import cadquery as cq

# =======================================================
# ГЕОМЕТРИЧЕСКИЕ ПАРАМЕТРЫ (в мм)
# =======================================================
h_base = 68          # Высота стены до зубцов
h_total = 80         # Полная высота с зубцами
w_floor = 16         # Толщина основания у пола
thick_wall = 5.0     # Толщина верхней зубчатой стены
cable_w = 10         # Ширина кабель-канала
cable_h = 20         # Высота кабель-канала
sample_length = 120  # Длина тестового образца

thick_main = thick_wall + 1.5  

# =======================================================
# 1. ПОСТРОЕНИЕ БАЗОВОГО ПРОФИЛЯ (Высота до бойниц — 68 мм)
# =======================================================
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0).lineTo(0, 4)
    .lineTo(cable_w, 4).lineTo(cable_w, 4 + cable_h).lineTo(0, 4 + cable_h)
    .lineTo(0, h_base)
    .lineTo(8, h_base)
    .lineTo(8, h_base - 12)
    .lineTo(8 + thick_wall, h_base - 12)
    .lineTo(8 + thick_wall, h_base)
    .lineTo(8 + thick_main, h_base - 6)
    .lineTo(8 + thick_main, 25)
    .lineTo(w_floor, 12).lineTo(w_floor, 4)
    .lineTo(w_floor + 2, 0).lineTo(w_floor - 2, 0)
    .close()
)

plinth_base = profile.extrude(sample_length)

# =======================================================
# 2. ЭКСПЕРИМЕНТАЛЬНЫЙ ЦИКЛ СБОРКИ ЗУБЦОВ (Критическая точка)
# =======================================================
# Проблема: При итерациях цикла метод .translate() некорректно 
# воспринял локальные оси выдавливания, из-за чего блоки зубцов 
# сместились по оси X наружу и повисли в воздухе справа от модели.

tooth_w = 15.0       # Длина зубца по оси Y
gap_w = 15.0         # Длина прорези по оси Y
tooth_height = 12.0  # Высота зубца

for i in range(4):
    # Вычисление стартовой позиции каждого зубца по длине
    y_start = i * (tooth_w + gap_w)
    
    # Создание отдельного 3D-блока зубца
    tooth = cq.Solid.makeBox(thick_wall, tooth_w, tooth_height)
    
    # Смещение блока (Ошибка интерпретации локального пространства OpenCASCADE)
    tooth_shifted = tooth.translate(cq.Vector(8, y_start, h_base))
    
    # Логическое объединение, зафиксировавшее геометрию с багом
    plinth_base = plinth_base.union(tooth_shifted)

# =======================================================
# ЭКСПОРТ АНОМАЛЬНОЙ МОДЕЛИ
# =======================================================
cq.exporters.export(plinth_base, 'v2_failed_blocks.summary.stl')
