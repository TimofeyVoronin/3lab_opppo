from abc import ABC, abstractmethod


# ============================================================
# АБСТРАКТНЫЙ БАЗОВЫЙ КЛАСС
# ============================================================

class Transport(ABC):
    """
    Абстрактный базовый класс транспорта.
    Содержит общие параметры для всех видов транспорта.
    """

    def __init__(self, owner: str, speed: int, distance: int):
        # Проверка типов входных данных
        if not isinstance(owner, str):
            raise TypeError("owner must be a string")
        if not isinstance(speed, int):
            raise TypeError("speed must be an integer")
        if not isinstance(distance, int):
            raise TypeError("distance must be an integer")

        self.owner = owner
        self.speed = speed
        self.distance = distance

    @abstractmethod
    def info(self) -> str:
        """
        Абстрактный метод.
        Должен возвращать строку с описанием объекта.
        """
        pass


# ============================================================
# КЛАСС: САМОЛЁТ
# ============================================================

class Plane(Transport):
    """
    Класс самолёта.
    """

    def __init__(
        self,
        owner: str,
        speed: int,
        distance: int,
        flight_range: int,
        capacity: int
    ):
        # Проверка типов
        if not isinstance(flight_range, int):
            raise TypeError("flight_range must be an integer")
        if not isinstance(capacity, int):
            raise TypeError("capacity must be an integer")

        super().__init__(owner, speed, distance)

        self.flight_range = flight_range
        self.capacity = capacity

    def info(self) -> str:
        return (
            f"[Самолет] Владелец: {self.owner}, "
            f"Скорость: {self.speed}, "
            f"Расстояние: {self.distance}, "
            f"Дальность: {self.flight_range}, "
            f"Грузоподъемность: {self.capacity}"
        )


# ============================================================
# КЛАСС: ПОЕЗД
# ============================================================

class Train(Transport):
    """
    Класс поезда.
    """

    def __init__(self, owner: str, speed: int, distance: int, wagons: int):
        if not isinstance(wagons, int):
            raise TypeError("wagons must be an integer")

        super().__init__(owner, speed, distance)
        self.wagons = wagons

    def info(self) -> str:
        return (
            f"[Поезд] Владелец: {self.owner}, "
            f"Скорость: {self.speed}, "
            f"Расстояние: {self.distance}, "
            f"Вагоны: {self.wagons}"
        )


# ============================================================
# КЛАСС: ГРУЗОВИК
# ============================================================

class Truck(Transport):
    """
    Класс грузовика.
    """

    def __init__(
        self,
        owner: str,
        speed: int,
        distance: int,
        capacity: int,
        volume: float
    ):
        if not isinstance(capacity, int):
            raise TypeError("capacity must be an integer")
        if not isinstance(volume, (int, float)):
            raise TypeError("volume must be a number")

        super().__init__(owner, speed, distance)

        self.capacity = capacity
        self.volume = volume

    def info(self) -> str:
        return (
            f"[Грузовик] Владелец: {self.owner}, "
            f"Скорость: {self.speed}, "
            f"Расстояние: {self.distance}, "
            f"Грузоподъемность: {self.capacity}, "
            f"Объем: {self.volume}"
        )


# ============================================================
# КОНТЕЙНЕР ДЛЯ ХРАНЕНИЯ ОБЪЕКТОВ
# ============================================================

class TransportContainer:
    """
    Контейнер для хранения объектов транспорта.
    """

    def __init__(self):
        self.items: list[Transport] = []

    def add(self, obj: Transport):
        if not isinstance(obj, Transport):
            raise TypeError("Only Transport objects can be added")

        self.items.append(obj)

    def remove_by_condition(self, field: str, operator: str, value) -> int:
        """
        Удаляет объекты по условию.
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

        self.items = [obj for obj in self.items if not check(obj)]
        return before - len(self.items)

    def print_all(self):
        for obj in self.items:
            print(obj.info())


# ============================================================
# ФАБРИКА СОЗДАНИЯ ОБЪЕКТОВ
# ============================================================

def create_transport(transport_type: str, params: dict) -> Transport | None:
    """
    Фабричный метод создания объектов транспорта.
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


# ============================================================
# ОБРАБОТКА КОМАНД
# ============================================================

def parse_add(parts: list[str], container: TransportContainer):
    params = {}

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

    obj = create_transport(parts[1], params)
    if obj:
        container.add(obj)


def parse_rem(parts: list[str], container: TransportContainer):
    field, operator, value = parts[1], parts[2], int(parts[3])
    removed = container.remove_by_condition(field, operator, value)
    print("[REM]")
    print(f"Удалено объектов: {removed}")


def parse_print(container: TransportContainer):
    print("[PRINT]")
    if not container.items:
        print("Контейнер пуст")
    else:
        container.print_all()


# ============================================================
# ТОЧКА ВХОДА
# ============================================================

def process_file(filename: str):
    """
    Читает команды из файла и выполняет их.
    """
    container = TransportContainer()

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

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
