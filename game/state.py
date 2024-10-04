class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
            cls.instance._initialized = False
        return cls.instance
    
    def __init__(self): 
        if not self._initialized:
            self._initialized = True
            

class Settings(Singleton):
    def __new__(cls):
        instance = super(Settings, cls).__new__(cls) 
        return instance
    
    def __init__(self) -> None:
        self.cell_size:int = 30
        self.cell_count_x:int = 20
        self.cell_count_y:int = 20
        self.fps:float = 6.0
        self.fps_increment:float = 0.7
        self.screen = Screen(self.cell_count_x,self.cell_count_y,self.cell_size)    
        self.game_end = False
  

class Screen(Singleton):
    def __new__(cls, cell_count_x:int,cell_count_y:int,cell_size:int):
        instance = super(Screen, cls).__new__(cls)    
        return instance
    
    def __init__(self,cell_count_x:int,cell_count_y:int,cell_size:int) -> None:
        if not self._initialized:
            super(Screen, self).__init__()
            self.width:int = cell_count_y * cell_size
            self.height:int = cell_count_x * cell_size
            self.caption:str = 'Snake'

