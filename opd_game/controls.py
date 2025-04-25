import pygame as pg
import sys

def events():
    """обработка событий"""
    for event in pg.event.get():

        # выход из игры
        if event.type == pg.QUIT:
            sys.exit()

        