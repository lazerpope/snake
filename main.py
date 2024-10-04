import pygame as pg
# from time import perf_counter
from game.game_objects import Player , Food, is_collided
from game.state import Settings
from colors import Colors
from input_map import Input_map

settings = Settings()
player = Player()
food = Food()

pg.init()
screen_size = (settings.screen.width,settings.screen.height)

screen = pg.display.set_mode(screen_size)
print(type(screen))
pg.display.set_caption(settings.screen.caption)
clock = pg.time.Clock()

while not settings.game_end:
    # start_time =   perf_counter ()
    screen.fill(Colors.BLACK)
    
    for event in pg.event.get():
        # print(event)
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == 27):
            settings.game_end = True        
        if event.type == pg.KEYDOWN and event.scancode in [item.value for item in Input_map] :
            player.change_direction(event.scancode)
            break
            
    if is_collided(player,food):  
        player.tail.add_piece(player.x,player.y)      
        food.move()
        settings.fps += settings.fps_increment
    
    player.move()   
    food.draw(screen)
    player.draw(screen)

    pg.display.flip()
    # print(round((perf_counter () - start_time)*1000,2), 'ms')
    clock.tick(settings.fps)

