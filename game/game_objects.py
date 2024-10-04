import pygame as pg
# from typing import TypeVar
from abc import ABC, abstractmethod
from game.state import Settings
from colors import Colors
from input_map import Input_map
import random
from typing import Type, Union

settings = Settings()


class GameObject(ABC):
    @abstractmethod
    def __init__(
        self,
        color: str = Colors.WHITE,
        x: int = settings.cell_count_x // 2 - 1,
        y: int = settings.cell_count_x // 2 - 1,
    ):
        self.x = float(x)
        self.y = float(y)
        self.size = settings.cell_size
        self.color = color

    @abstractmethod
    def draw(self, screen: pg.Surface) :
        pg.draw.rect(
            screen,
            self.color,
            (self.x * self.size, self.y * self.size, self.size, self.size),
        )

    @abstractmethod
    def move(self) :
        ...


class Player(GameObject):
    def __init__(
        self,
        color: str = Colors.SNAKE,
        x: int = settings.cell_count_x // 2 - 1,
        y: int = settings.cell_count_x // 2 - 1,
        direction: int = Input_map.NONE.value,
    ):
        super().__init__(
            color,
            x,
            y,
        )
        self.direction = direction
        self.tail = Tail()

    def draw(self, screen: pg.Surface):
        self.tail.draw(screen)
        super().draw(screen)

    def move(
        self,
    ) -> None:
        self.tail.move(self)
        match self.direction:
            case Input_map.UP.value:
                self.y -= 1
            case Input_map.DOWN.value:
                self.y += 1
            case Input_map.LEFT.value:
                self.x -= 1
            case Input_map.RIGHT.value:
                self.x += 1
            case Input_map.NONE.value:
                ...
            case _:
                ...

        if self.x < 0:
            self.x = settings.cell_count_x - 1
        if self.x >= settings.cell_count_x:
            self.x = 0
        if self.y < 0:
            self.y = settings.cell_count_y - 1
        if self.y >= settings.cell_count_y:
            self.y = 0

        if len(self.tail.pieces) > 3:
            for piece in self.tail.pieces[2:]:
                if is_collided(piece, self):
                    settings.game_end = True
                    

    def change_direction(self, direction: int):
        if (
            (direction == Input_map.UP.value and self.direction != Input_map.DOWN.value)
            or (
                direction == Input_map.DOWN.value
                and self.direction != Input_map.UP.value
            )
            or (
                direction == Input_map.LEFT.value
                and self.direction != Input_map.RIGHT.value
            )
            or (
                direction == Input_map.RIGHT.value
                and self.direction != Input_map.LEFT.value
            )
            or len(self.tail.pieces) == 0
        ):
            self.direction = direction


class Food(GameObject):
    def __init__(
        self,
        color: str = Colors.FOOD,
        x: int = random.randint(0, settings.cell_count_x - 1),
        y: int = random.randint(0, settings.cell_count_x - 1),
    ):
        super().__init__(
            color,
            x,
            y,
        )

    def draw(self, screen: pg.Surface):
        super().draw(screen)

    def move(
        self,
    ):
        self.x = random.randint(0, settings.cell_count_x - 1)
        self.y = random.randint(0, settings.cell_count_x - 1)


class TailPiece(GameObject):
    def __init__(
        self,
        x: int,
        y: int,
        color: str = Colors.TAIL,
    ):
        super().__init__(
            color,
            x,
            y,
        )

    def draw(self, screen: pg.Surface):
        super().draw(screen)

    def move(
        self,
    ):
        raise Exception("tail piece cant move by itself")


class Tail:
    def __init__(self):
        self.pieces: list[TailPiece] = []

    def draw(self, screen: pg.Surface):
        for piece in self.pieces:
            piece.draw(screen)

    def move(self, player: Player):
        if len(self.pieces) > 0:
            self.pieces[-1].x, self.pieces[-1].y = player.x, player.y
        if len(self.pieces) > 1:
            self.pieces.insert(0, self.pieces.pop())

    def add_piece(self, x: int, y: int):
        self.pieces.append(TailPiece(x, y))


any_gameobject = Union[Type[GameObject], GameObject]


def is_collided(obj1: any_gameobject, obj2: any_gameobject):
    if obj1.x == obj2.x and obj1.y == obj2.y:  # type: ignore
        return True
    else:
        return False
