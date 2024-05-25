import random as rd
import math
from gdpc import Editor, Block, geometry, Transform
from utils.Enums import COLLUMN_STYLE, BORDER_RADIUS
from utils.functions import *
from buildings.geometry.Point import Point
from buildings.geometry.Vertice import Vertice

class Window:
    def __init__(self, rdata, max_width : int, max_height : int):
        self.rdata = rdata
        self.width, self.height = self.get_size(max_width, max_height)
        self.is_grounded = self.is_grounded()
        self.has_multiple_windows = self.has_multiple_windows()
        self.is_alternate = self.is_alternate()
        self.has_vertical_crossbar, self.has_horizontal_crossbar = self.has_crossbars()
        self.border_radius = self.border_radius()
        self.padding = 0
        self.editor, self.materials = None,None
        
    def build(self, editor : Editor, facade_len : int, facade_height : int, materials : list[str]):
        self.editor = editor
        self.materials = materials
        
        # correction to avoid asymetry
        self.padding = (facade_len - self.width)//2
        self.width = facade_len - self.padding*2
        
        if not self.is_grounded: editor.transform @= Transform((0,(facade_height-self.height)//2,0))
        editor.transform @= Transform((self.padding,0,0))
        
        if self.has_multiple_windows: self.build_multiple_windows()
        else :
            self.place_glasses(0, self.width)
        
    def build_multiple_windows(self):
        slices = rd.randint(3, self.width//self.rdata["size"]["min_width"])
        mid = math.ceil(slices/2)
        windows_count = mid
        inter_count = slices - windows_count
        window_size = rd.randint(self.rdata["size"]["min_width"], (self.width-inter_count) // windows_count) 
        inter_size = (self.width - window_size*windows_count) // inter_count
        
        is_even= slices % 2 == 0
        is_window, gap = True, 0
        remainder = self.width - (window_size*windows_count + inter_size*inter_count)
        for i in range(1,slices+1):
            wsize,isize = window_size, inter_size
            if is_even and i == mid: wsize, isize = wsize*2, isize*2
            if i ==  mid: wsize, isize = wsize + remainder, isize + remainder
            
            # kepp a spacing between windows, "is revert" is used to keep symetry
            if is_window:               
                self.place_glasses(gap, gap+wsize)
                gap += wsize
            else : 
                gap += isize
                
            is_window = not is_window
    
    def place_glasses(self, x1 : int, x2 : int):
        len = x2 - x1
        if self.is_alternate:
            mid = x1 + len//2
            
            is_block, is_even = False, len % 2 == 0
            for x in range(x1,x2):
                if is_even and x == mid: is_block = not is_block # to keep symetry
                id = 1 if not is_block else 2
                geometry.placeCuboid(self.editor,(x,0,0),(x,self.height,0),Block(self.materials[id]))
                is_block = not is_block
            
        else:
            geometry.placeCuboid(self.editor,(x1,0,0),(x2-1,self.height,0),Block(self.materials[1]))
            
        self.build_crossbars(x1, x2-1, len)
        if len > 1: self.build_border_radius(x1, x2-1)
        
    def get_size(self, max_width : int ,max_height : int) -> tuple[int,int]:
        return (
                rd.randint(self.rdata["size"]["min_width"],max_width),
                rd.randint(self.rdata["size"]["min_height"],max_height)
            )
                 
    def build_crossbars(self, x1 : int, x2 : int, len : int):
        if self.has_vertical_crossbar and self.height >= self.rdata["crossbars"]["min_height_for_vertical_crossbar"]:
            y = self.height//2
            geometry.placeCuboid(self.editor,(x1,y,0),(x2,y,0),Block(self.materials[3]))
        if self.has_horizontal_crossbar and len >= self.rdata["crossbars"]["min_width_for_horizontal_crossbar"]:
            x = len//2
            geometry.placeCuboid(self.editor,(x1+x,0,0),(x2-x,self.height,0),Block(self.materials[3], {"up" : "true"})) 
            
    def build_border_radius(self, x1 : int, x2 : int):
        if self.border_radius != BORDER_RADIUS.NONE:
            self.editor.placeBlock((x1,self.height,0),Block(self.materials[4], {"facing": "west", "half": "top"}))
            self.editor.placeBlock((x2,self.height,0),Block(self.materials[4], {"facing": "east", "half": "top"}))
        if self.border_radius == BORDER_RADIUS.TOP_AND_BOTTOM:
            self.editor.placeBlock((x1,0,0),Block(self.materials[4], {"facing": "west"}))
            self.editor.placeBlock((x2,0,0),Block(self.materials[4], {"facing": "east"}))
                          
    def is_grounded(self):
        # if the window is grounded or if there is a padding between the window and the ground
        return self.rdata["grounded"] >= rd.random()
    
    def has_multiple_windows(self):
        if self.width >  self.rdata["size"]["max_width"]: return True
        elif self.width >=  self.rdata["multiple"]["min_width"]:
            return self.rdata["multiple"]["proba"] >= rd.random()
        else : return False
    
    def is_alternate(self):
        # if the window alternate between glass_blocks and glass_panes
        return self.rdata["alternate"] >= rd.random()
    
    def has_crossbars(self):
        # if the window has crossbars
        data = self.rdata["crossbars"]
        
        return (data["vertical_crossbar"] >= rd.random(), data["horizontal_crossbar"] >= rd.random())
    
    def border_radius(self):
        return select_random(self.rdata["border_radius"], BORDER_RADIUS)