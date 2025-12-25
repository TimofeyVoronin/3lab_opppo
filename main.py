"""
Модуль для обработки транспортных объектов и выполнения команд ADD, REM, PRINT.
Реализация соответствует варианту 4 (Транспорт).
"""

from abc import ABC, abstractmethod


# АБСТРАКТНЫЙ БАЗОВЫЙ КЛАСС: TRANSPORT
class Transport(ABC):
    """
    Абстрактный базовый класс транспорта.
    Содержит общие параметры для всех видов транспорта.
    """

    def __init__(self, owner: str, speed: int, distance: int):
        self.owner = owner          # Имя владельца
        self.speed = speed          # Скорость
        self.distance = distance    # Расстояние между пунктами

    @abstractmethod
    def info(self) -> str:
        """
        Абстрактный метод.
        Должен возвращать строку с описанием объекта транспорта.
        """
        pass


# КЛАСС: САМОЛЁТ
class Plane(Transport):
    """Класс самолёта."""

    def __init__(
        self,
        owner: str,
        speed: int,
        distance: int,
        flight_range: int,
        capacity: int
    ):
        super().__init__(owner, speed, distance)
        self.flight_range = flight_range    # Дальность полёта
        self.capacity = capacity            # Грузоподъёмность

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

    def __init__(self, owner: str, speed: int, distance: int, wagons: int):
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

    def __init__(
        self,
        owner: str,
        speed: int,
        distance: int,
        capacity: int,
        volume: float
    ):
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
    Контейнер для хранения объектов транспорта.
    Реализован на основе стандартного списка list.
    """

    def __init__(self):
        self.items: list[Transport] = []

    def add(self, obj: Transport):
        """Добавление объекта в контейнер."""
        self.items.append(obj)

    def remove_by_condition(self, field: str, operator: str, value) -> int:
        """
        Удаление объектов по условию вида:
        field operator value (например: speed > 100)
        Возвращает количество удалённых объектов.
        """
        before = len(self.items)

        def check(obj: Transport) -> bool:
            # Получаем значение атрибута по имени
            attr = getattr(obj, field, None)
            if attr is None:
                return False

            # Словарь операторов (результаты вычисляются сразу)
            operators = {
                ">": attr > value,
                "<": attr < value,
                "==": attr == value
            }

            return operators.get(operator, False)

        # Оставляем только те объекты, которые не подходят под условие
        self.items = [obj for obj in self.items if not check(obj)]
        return before - len(self.items)

    def print_all(self):
        """Вывод всех объектов контейнера."""
        for obj in self.items:
            print(obj.info())


# СОЗДАНИЕ ОБЪЕКТОВ ТРАНСПОРТА
def create_transport(transport_type: str, params: dict) -> Transport | None:
    """
    Создание объекта транспорта по типу и параметрам.
    Возвращает объект транспорта или None.
    """
    if transport_type == "PLANE":
        return Plane(
            params["owner"],
            params["speed"],
            params["distance"],
            params["range"],
            params["capacity"]
        )

    if transport_type == "TRAIN":
        return Train(
            params["owner"],
            params["speed"],
            params["distance"],
            params["wagons"]
        )

    if transport_type == "TRUCK":
        return Truck(
            params["owner"],
            params["speed"],
            params["distance"],
            params["capacity"],
            params["volume"]
        )

    return None


# ОБРАБОТКА КОМАНД
def parse_add(parts: list[str], container: TransportContainer):
    """
    Обработка команды ADD.
    Создаёт объект транспорта и добавляет его в контейнер.
    """
    transport_type = parts[1]
    params = {}

    # Разбор параметров формата key=value
    for part in parts[2:]:
        key, value = part.split("=")
        params[key] = value

    # Приведение типов
    params["speed"] = int(params["speed"])
    params["distance"] = int(params["distance"])

    if "capacity" in params:
        params["capacity"] = int(params["capacity"])
    if "range" in params:
        params["range"] = int(params["range"])
    if "wagons" in params:
        params["wagons"] = int(params["wagons"])
    if "volume" in params:
        params["volume"] = float(params["volume"])

    obj = create_transport(transport_type, params)
    if obj:
        container.add(obj)


def parse_rem(parts: list[str], container: TransportContainer):
    """
    Обработка команды REM.
    Удаляет объекты из контейнера по заданному условию.
    """
    field, operator, value = parts[1], parts[2], int(parts[3])
    removed = container.remove_by_condition(field, operator, value)
    print("[REM]")
    print(f"Удалено объектов: {removed}")


def parse_print(container: TransportContainer):
    """
    Обработка команды PRINT.
    Выводит содержимое контейнера.
    """
    print("[PRINT]")
    if not container.items:
        print("Контейнер пуст")
    else:
        container.print_all()


# ОСНОВНАЯ ФУНКЦИЯ ЧТЕНИЯ ФАЙЛА
def process_file(filename: str):
    """
    Читает файл с командами и выполняет их последовательно.
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
