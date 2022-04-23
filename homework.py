"""
Модуль фитнес-трекера для расчета и отображения результата
трех типов тренировок: бег, плавание и спортивная ходьба.

Входные данные для бега: количество шагов, время тренировки в часах,
вес пользователя.
Входные данные для плавания: количество гребков,
время в часах, вес пользователя, длина бассейна, сколько раз
пользователь переплыл бассейн.
Входные данные для спортивной ходьбы: количество шагов, время
тренировки в часах, вес пользователя, рост пользователя.

Результаты вывода: тип и длительность тренировки, дистанция,
средняя скорость и кол-во потраченных калорий.
"""
from typing import List, Tuple


class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получить информационное сообщение о результатах тренировки."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self, action: int, duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_km = self.action * Training.LEN_STEP / Training.M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    MIN_IN_HOUR: int = 60
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        all_calories = ((Running.COEFF_CALORIE_1
                        * self.get_mean_speed()
                        - Running.COEFF_CALORIE_2)
                        * self.weight
                        / Running.M_IN_KM
                        * self.duration
                        * Running.MIN_IN_HOUR)
        return all_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: float
    MIN_IN_HOUR: int = 60
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        all_calories = ((SportsWalking.COEFF_CALORIE_1 * self.weight
                        + (self.get_mean_speed()**2 // self.height)
                        * SportsWalking.COEFF_CALORIE_2 * self.weight)
                        * self.duration
                        * SportsWalking.MIN_IN_HOUR)
        return all_calories


class Swimming(Training):
    """Тренировка: плавание."""
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int
    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_km = self.action * Swimming.LEN_STEP / Training.M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool
                      * self.count_pool
                      / Swimming.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        all_calories = ((self.get_mean_speed() + Swimming.COEFF_CALORIE_1)
                        * Swimming.COEFF_CALORIE_2
                        * self.weight)
        return all_calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные, полученные от датчиков."""
    dict_all_activities: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in dict_all_activities:
        # Получить объект соответствующего класса:
        training = dict_all_activities[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    # Вывести на экран результаты тренировки:
    print(info.get_message())


if __name__ == '__main__':
    CustomList = List[Tuple[str, List[int]]]
    packages: CustomList = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        # Определить тип тренировки:
        training = read_package(workout_type, data)
        # Выполнить основную функцию для данного типа тренировки:
        main(training)
