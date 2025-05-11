from csv_reader import start_size
from gen_image import image_gen
from gen_volume import render

if __name__ == '__main__':

    print("Regular spacing between images of stack?")
    regSpacing = bool(input())

    path = "./image_stack_2"

    width, height, depth = image_gen(regSpacing, path, start_size)

    print(f'\nVolume dimensions: {width} x {height} x {depth}')

    render(width, height, depth)