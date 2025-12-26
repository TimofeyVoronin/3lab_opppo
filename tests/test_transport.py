import pytest
from main import (
    TransportContainer,
    Plane,
    Train,
    Truck
)

# ==================================================
# ТЕСТЫ СОЗДАНИЯ ОБЪЕКТОВ
# ==================================================

def test_create_plane():
    plane = Plane("Alex", 600, 1500, 3000, 8000)
    assert plane.owner == "Alex"
    assert plane.speed == 600
    assert plane.distance == 1500
    assert plane.flight_range == 3000
    assert plane.capacity == 8000


def test_create_train():
    train = Train("Ivan", 120, 500, 20)
    assert train.owner == "Ivan"
    assert train.wagons == 20


def test_create_truck():
    truck = Truck("Max", 90, 300, 4000, 20.5)
    assert truck.capacity == 4000
    assert truck.volume == 20.5


# ==================================================
# ТЕСТЫ КОНТЕЙНЕРА
# ==================================================

def test_add_to_container():
    container = TransportContainer()
    plane = Plane("Alex", 600, 1500, 3000, 8000)

    container.add(plane)

    assert len(container.items) == 1


def test_remove_by_condition():
    container = TransportContainer()

    container.add(Plane("A", 600, 1500, 3000, 8000))
    container.add(Train("B", 100, 900, 10))
    container.add(Truck("C", 90, 400, 5000, 30))

    removed = container.remove_by_condition("speed", ">", 100)

    assert removed == 1
    assert len(container.items) == 2


# ==================================================
# ТЕСТ НА ОБРАБОТКУ ОШИБОК
# ==================================================

def test_remove_with_invalid_field():
    container = TransportContainer()
    container.add(Plane("Alex", 600, 1500, 3000, 8000))

    removed = container.remove_by_condition("unknown", ">", 10)

    # ничего не должно удалиться
    assert removed == 0
    assert len(container.items) == 1
