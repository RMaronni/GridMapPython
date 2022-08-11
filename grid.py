from math import floor, sqrt
import collections.abc
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw


SIZE_A0  = (841, 1189)
SIZE_A1  = (594, 841)
SIZE_A2  = (420, 594)
SIZE_A3  = (297, 420)
SIZE_A4  = (210, 297)
SIZE_A5  = (148, 210)
SIZE_A6  = (105, 148)
SIZE_A7  = (74,  105)
SIZE_A8  = (52,  74)
SIZE_A9  = (37,  52)
SIZE_A10 = (26,  37)

DPI = 96
COLOR_WHITE = 1

class GridMap(ABC):

    def __init__(self):
        pass

    
    @abstractmethod
    def get_grid(self):
        pass  


    def draw_grid(self, img, tile_list):
        draw = ImageDraw.Draw(img)

        for tile in tile_list:
            draw.polygon(tile)

        return img 


    def create_image(self, paper_size, dpi):
        img_size = tuple(floor(x*dpi/25.4) for x in paper_size)
        return Image.new('1', img_size, COLOR_WHITE)     



    def mm_to_px(self, mm, dpi):
        if isinstance(mm, collections.abc.Sequence):
            return tuple(floor(x*dpi/25.4) for x in mm)
        else:
            return floor(mm*dpi/25.4)


    def create_grid_map(self, paper_size, tile_size, DPI, file_format):
        img = self.create_image(paper_size, DPI)
        tile_list = self.get_grid(tile_size, paper_size, DPI)
        self.draw_grid(img, tile_list)
        img.save(f"grid_map.{file_format}")
        img.show()




class SquareGridMap(GridMap):
    
    def get_grid(self, tile_size, paper_size, dpi):

        # Convert inputs form mm to pixels
        tile_size = self.mm_to_px(tile_size, dpi)
        paper_size = self.mm_to_px(paper_size, dpi)

        columns = floor(paper_size[0]/tile_size)
        rows    = floor(paper_size[1]/tile_size)

        margin_columns = (paper_size[0]%tile_size)/2
        margin_rows    = (paper_size[1]%tile_size)/2

        tile_list = []

        for i in range(columns):
            for j in range(rows):
                point_1 = (i*tile_size + margin_columns, j*tile_size + margin_rows)
                point_2 = (point_1[0]+tile_size, point_1[1])
                point_3 = (point_1[0]+tile_size, point_1[1]+tile_size)
                point_4 = (point_1[0], point_1[1]+tile_size)
                tile_list.append([point_1, point_2, point_3, point_4])

        return tile_list



class HexGridMap(GridMap):

    def get_grid(self, tile_size, paper_size, dpi):

        # Convert inputs form mm to pixels
        tile_size = self.mm_to_px(tile_size, dpi)
        paper_size = self.mm_to_px(paper_size, dpi)

        h = self._get_hex_heigth(tile_size)

        columns = floor(paper_size[0]/(1.5*tile_size))
        rows    = floor(paper_size[1]/h)

        if paper_size[0]%(1.5*tile_size) < (tile_size/2):
            columns = columns - 1

        margin_columns = (paper_size[0] - (columns*1.5*tile_size) - (tile_size/2))/2
        margin_rows    = (paper_size[1]%h)/2

        tile_list = []

        for i in range(columns):
            for j in range(rows):
                point_1 = (i*(1.5*tile_size) + (tile_size/2) + margin_columns, j*h + margin_rows)
                if i%2 != 0:
                    if j == 0: continue
                    point_1 = (point_1[0], point_1[1] - (h/2))
                    
                point_2 = self._get_hex_point_2(point_1, tile_size)
                point_3 = self._get_hex_point_3(point_1, tile_size)
                point_4 = self._get_hex_point_4(point_1, tile_size)
                point_5 = self._get_hex_point_5(point_1, tile_size)
                point_6 = self._get_hex_point_6(point_1, tile_size)
                tile_list.append([point_1, point_2, point_3, point_4, point_5, point_6])

        return tile_list
    
    def _get_hex_heigth(self, tile_size):
        return sqrt(3)*tile_size 

    def _get_hex_point_2(self, point_1, tile_size):
        return (point_1[0]+tile_size, point_1[1])

    def _get_hex_point_3(self, point_1, tile_size):
        h = self._get_hex_heigth(tile_size)
        return (point_1[0]+(1.5*tile_size), point_1[1]+(h/2))

    def _get_hex_point_4(self, point_1, tile_size):
        h = self._get_hex_heigth(tile_size)
        return (point_1[0]+tile_size, point_1[1]+h)

    def _get_hex_point_5(self, point_1, tile_size):
        h = self._get_hex_heigth(tile_size)
        return (point_1[0], point_1[1]+h)

    def _get_hex_point_6(self, point_1, tile_size):
        h = self._get_hex_heigth(tile_size)
        return (point_1[0]-(0.5*tile_size), point_1[1]+(h/2))




paper_size = SIZE_A4
tile_size = 15
file_format = 'pdf'

map = SquareGridMap()
map.create_grid_map(paper_size, tile_size, DPI, file_format)