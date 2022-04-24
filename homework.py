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
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self, action: int, duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    MIN_IN_HOUR = 60
    MEAN_SPEED_MULTIPLIER = 18
    MEAN_SPEED_SUBTRAHEND = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Вычисление промежуточного значения для скорости:
        mean_speed_transf = (self.MEAN_SPEED_MULTIPLIER
                             * self.get_mean_speed()
                             - self.MEAN_SPEED_SUBTRAHEND)
        # Вычисление продолжительности в минутах:
        duration_in_min = self.duration * self.MIN_IN_HOUR
        return mean_speed_transf * self.weight / self.M_IN_KM * duration_in_min


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: float
    MIN_IN_HOUR = 60
    WEIGHT_MULTIPIER = 0.035
    SPEED_BY_HEIGHT_MULTIPLIER = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Вычисление первого слагаемого в выражении:
        weight_transf = self.WEIGHT_MULTIPIER * self.weight
        # Вычисление второго слагаемого в выражении:
        sq_speed_by_h_w = (self.get_mean_speed()**2
                           // self.height
                           * self.SPEED_BY_HEIGHT_MULTIPLIER
                           * self.weight)
        # Вычисление продолжительности в минутах:
        duration_in_min = self.duration * self.MIN_IN_HOUR
        return (weight_transf + sq_speed_by_h_w) * duration_in_min


class Swimming(Training):
    """Тренировка: плавание."""
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    MEAN_SPEED_ADDENDUM = 1.1
    MEAN_SPEED_MULTIPLIER = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # Вычисление пройденной дистанции в метрах:
        distance_m_pool = self.length_pool * self.count_pool
        # Вычисление пройденной дистанции в километрах:
        distance_km_pool = distance_m_pool / self.M_IN_KM
        return distance_km_pool / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Вычисление промежуточного значения для скорости:
        mean_speed_transf = ((self.get_mean_speed()
                             + self.MEAN_SPEED_ADDENDUM)
                             * self.MEAN_SPEED_MULTIPLIER)
        return mean_speed_transf * self.weight


# Словарь со всеми известными типами тренировок:
ALL_ACTIVITIES = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные, полученные от датчиков."""
    if workout_type not in ALL_ACTIVITIES:
        raise KeyError(f'Незвестный тип тренировки - {workout_type}')
    return ALL_ACTIVITIES[workout_type](*data)


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
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        # Определить тип тренировки:
        training = read_package(workout_type, data)
        # Выполнить основную функцию для данного типа тренировки:
        main(training)
