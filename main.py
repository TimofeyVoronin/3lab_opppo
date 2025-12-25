"""Модуль для обработки транспортных объектов и команд ADD, REM, PRINT."""
from abc import ABC, abstractmethod


# АБСТРАКТНЫЙ БАЗОВЫЙ КЛАСС: ТРАНСПОРТ
class Transport(ABC):
    """
    Абстрактный базовый класс.
    Содержит общие параметры для всех видов транспорта.
    """

    def __init__(self, owner: str, speed: int, distance: int):
        self.owner = owner          # Имя владельца
        self.speed = speed          # Скорость
        self.distance = distance    # Расстояние

    @abstractmethod
    def info(self) -> str:
        """
        Абстрактный метод.
        Возвращает строку с описанием объекта.
        """
        pass


# КЛАСС: САМОЛЁТ
class Plane(Transport):
    """Класс самолёта."""
    def __init__(self, owner, speed, distance, flight_range, capacity):
        super().__init__(owner, speed, distance)
        self.flight_range = flight_range      # Дальность полёта
        self.capacity = capacity              # Грузоподъёмность

    def info(self) -> str:
        return (
            f"[Самолет] Владелец: {self.owner}, "
            f"Скорость: {self.speed}, "
            f"Расстояние: {self.distance}, "
            f"Дальность: {self.flight_range}, "
            f"Грузоподъемность: {self.capacity}"
        )


# КЛАСС: ПОЕЗД
class Train(Transport):
    """Класс поезда."""
    def __init__(self, owner, speed, distance, wagons):
        super().__init__(owner, speed, distance)
        self.wagons = wagons    # Количество вагонов

    def info(self) -> str:
        return (
            f"[Поезд] Владелец: {self.owner}, "
            f"Скорость: {self.speed}, "
            f"Расстояние: {self.distance}, "
            f"Вагоны: {self.wagons}"
        )


# КЛАСС: ГРУЗОВИК
class Truck(Transport):
    """Класс грузовика."""
    def __init__(self, owner, speed, distance, capacity, volume):
        super().__init__(owner, speed, distance)
        self.capacity = capacity    # Грузоподъёмность
        self.volume = volume        # Объём кузова

    def info(self) -> str:
        return (
            f"[Грузовик] Владелец: {self.owner}, "
            f"Скорость: {self.speed}, "
            f"Расстояние: {self.distance}, "
            f"Грузоподъемность: {self.capacity}, "
            f"Объем: {self.volume}"
        )


# КОНТЕЙНЕР ДЛЯ ХРАНЕНИЯ ОБЪЕКТОВ
class TransportContainer:
    """
    Контейнер реализован на основе стандартного списка list.
    """

    def __init__(self):
        self.items: list[Transport] = []

    def add(self, obj: Transport):
        """Добавление объекта в контейнер"""
        self.items.append(obj)

    def remove_by_condition(self, field, operator, value) -> int:
        """
        Удаление объектов по условию.
        Возвращает количество удалённых объектов.
        """
        before = len(self.items)

        def check(obj: Transport) -> bool:
            attr = getattr(obj, field, None)
            if attr is None:
                return False
            if operator == ">":
                return attr > value
            if operator == "<":
                return attr < value
            if operator == "==":
                return attr == value
            return False

        # Оставляем только те объекты, которые не удовлетворяют условию
        self.items = [obj for obj in self.items if not check(obj)]

        after = len(self.items)
        return before - after

    def print_all(self):
        """Вывод всех объектов контейнера"""
        for obj in self.items:
            print(obj.info())


# ОБРАБОТКА КОМАНДЫ ADD
def parse_add(parts, container: TransportContainer):
    """
    Создание объекта транспорта и добавление в контейнер.
    """
    transport_type = parts[1]
    params = {}

    # Разбор параметров формата key=value
    for part in parts[2:]:
        key, value = part.split("=")
        params[key] = value

    owner = params["owner"]
    speed = int(params["speed"])
    distance = int(params["distance"])

    if transport_type == "PLANE":
        obj = Plane(
            owner,
            speed,
            distance,
            int(params["range"]),
            int(params["capacity"])
        )
    elif transport_type == "TRAIN":
        obj = Train(
            owner,
            speed,
            distance,
            int(params["wagons"])
        )
    elif transport_type == "TRUCK":
        obj = Truck(
            owner,
            speed,
            distance,
            int(params["capacity"]),
            float(params["volume"])
        )
    else:
        return

    container.add(obj)


# ОБРАБОТКА КОМАНДЫ REM
def parse_rem(parts, container: TransportContainer):
    """
    Удаление объектов по условию.
    """
    field = parts[1]
    operator = parts[2]
    value = int(parts[3])

    print("[REM]")
    removed = container.remove_by_condition(field, operator, value)
    print(f"Удалено объектов: {removed}")


# ОБРАБОТКА КОМАНДЫ PRINT
def parse_print(container: TransportContainer):
    """
    Вывод содержимого контейнера.
    """
    print("[PRINT]")
    if not container.items:
        print("Контейнер пуст")
    else:
        container.print_all()


# ЧТЕНИЕ ФАЙЛА И ВЫПОЛНЕНИЕ КОМАНД
def process_file(filename: str):
    """
    Основная функция.
    Читает команды из файла и выполняет их.
    """
    container = TransportContainer()

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Пропуск пустых строк
            if not line:
                continue

            parts = line.split()

            if parts[0] == "ADD":
                parse_add(parts, container)
            elif parts[0] == "REM":
                parse_rem(parts, container)
            elif parts[0] == "PRINT":
                parse_print(container)


if __name__ == "__main__":
    process_file("commands.txt")
