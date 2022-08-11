from math import floor, sqrt
import collections.abc
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


def mm_to_px(mm, dpi):
    if isinstance(mm, collections.abc.Sequence):
        return tuple(floor(x*dpi/25.4) for x in mm)
    else:
        return floor(mm*dpi/25.4)

        

def get_square_grid(tile_size, paper_size, dpi):

    # Convert inputs form mm to pixels
    tile_size = mm_to_px(tile_size, dpi)
    paper_size = mm_to_px(paper_size, dpi)

    columns = floor(paper_size[0]/tile_size)
    rows    = floor(paper_size[1]/tile_size)

    print(f"columns: {columns}")
    print(f"rows: {rows}")

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


def draw_grid(img, tile_list):
    draw = ImageDraw.Draw(img)

    for tile in tile_list:
        draw.polygon(tile)

    return img


def create_image(paper_size, dpi):
    img_size = tuple(floor(x*dpi/25.4) for x in paper_size)
    return Image.new('1', img_size, COLOR_WHITE)



def get_hex_grid(tile_size, paper_size, dpi):

    # Convert inputs form mm to pixels
    tile_size = mm_to_px(tile_size, dpi)
    paper_size = mm_to_px(paper_size, dpi)

    h = _get_hex_heigth(tile_size)

    columns = floor(paper_size[0]/(1.5*tile_size))
    rows    = floor(paper_size[1]/h)

    if paper_size[0]%(1.5*tile_size) < (tile_size/2):
        columns = columns - 1

    print(f"columns: {columns}")
    print(f"rows: {rows}")

    margin_columns = (paper_size[0] - (columns*1.5*tile_size) - (tile_size/2))/2
    margin_rows    = (paper_size[1]%h)/2

    tile_list = []

    for i in range(columns):
        for j in range(rows):
            point_1 = (i*(1.5*tile_size) + (tile_size/2) + margin_columns, j*h + margin_rows)
            if i%2 != 0:
                if j == 0: continue
                point_1 = (point_1[0], point_1[1] - (h/2))
                
            point_2 = _get_hex_point_2(point_1, tile_size)
            point_3 = _get_hex_point_3(point_1, tile_size)
            point_4 = _get_hex_point_4(point_1, tile_size)
            point_5 = _get_hex_point_5(point_1, tile_size)
            point_6 = _get_hex_point_6(point_1, tile_size)
            tile_list.append([point_1, point_2, point_3, point_4, point_5, point_6])

    return tile_list



def _get_hex_heigth(tile_size):
    return sqrt(3)*tile_size 

def _get_hex_point_2(point_1, tile_size):
    return (point_1[0]+tile_size, point_1[1])

def _get_hex_point_3(point_1, tile_size):
    h = _get_hex_heigth(tile_size)
    return (point_1[0]+(1.5*tile_size), point_1[1]+(h/2))

def _get_hex_point_4(point_1, tile_size):
    h = _get_hex_heigth(tile_size)
    return (point_1[0]+tile_size, point_1[1]+h)

def _get_hex_point_5(point_1, tile_size):
    h = _get_hex_heigth(tile_size)
    return (point_1[0], point_1[1]+h)

def _get_hex_point_6(point_1, tile_size):
    h = _get_hex_heigth(tile_size)
    return (point_1[0]-(0.5*tile_size), point_1[1]+(h/2))





paper_size = SIZE_A4

# img = create_image(paper_size, DPI)
# tile_list = get_square_grid(18, paper_size, DPI)
# draw_grid(img, tile_list)
# img.show()

for i in range(10, 20):
    img = create_image(paper_size, DPI)
    tile_list = get_hex_grid(i, paper_size, DPI)
    draw_grid(img, tile_list)
    img.show()