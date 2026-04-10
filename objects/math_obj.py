import pygame

"""
MATRIX2
A simple 2x2 matrix representation
"""

class Matrix2:
    def __init__(self,a=0,b=0,c=0,d=0):
        if type(a) == int or type(a) == float:
            self.a, self.b, self.c, self.d = a, b, c, d
        if type(a) == tuple or type(a) == list:
            if len(a) == 4:  # noqa
                self.a, self.b, self.c, self.d = a
            if len(a) == 2 and (type(a) == tuple or type(a) == list) and len(b) == 2:  # noqa
                self.a, self.b = a
                self.c, self.d = b
        if type(a) == pygame.Vector2 and type(b) == pygame.Vector2:
            self.a, self.b, self.c, self.d = a.x,b.x,a.y,b.y # noqa

    def __add__(self,next):
        if type(next) == Matrix2:
            return Matrix2(
                self.a + next.a,
                self.b + next.b,
                self.c + next.c,
                self.d + next.d,
            )

    def __mul__(self,next):
        if type(next) == Matrix2:
            return Matrix2(
                self.a * next.a + self.b * next.c,
                self.a * next.b + self.b * next.d,
                self.c * next.a + self.d * next.c,
                self.c * next.b + self.d * next.d,
            )
        if type(next) == pygame.Vector2:
            return pygame.Vector2(
                self.a * next.x + self.b * next.y,
                self.c * next.x + self.d * next.y,
            )
        if type(next) == int or type(next) == float:
            return Matrix2(
                self.a * next,
                self.b * next,
                self.c * next,
                self.d * next,
            )

    def copy(self):
        return Matrix2(
            self.a,
            self.b,
            self.c,
            self.d,
        )

    def transpose(self):
        return Matrix2(
            self.a,
            self.c,
            self.b,
            self.d,
        )

    def inverse(self):
        determinant = self.a * self.d - self.b * self.c
        return Matrix2(
            self.d,
            - self.b,
            - self.c,
            self.a,
        ) * (1/determinant)