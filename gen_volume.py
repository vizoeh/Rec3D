import pyvista as pv
from gen_image import image_gen
from csv_reader import start_size

path = './image_stack/'
regSpacing = False

width, height, depth = image_gen(regSpacing, path, start_size, 100, 100)

def texture():
    #! Simple dictionary that associates the position with the file.
    to_wrap = {"Top":"./temp/imageTop.png",
                "Bottom":"./temp/imageBottom.png",
                "Front":"./temp/imageFront.png",
                "Back":"./temp/imageBack.png",
                "Left":"./temp/imageLeft.png",
                "Right":"./temp/imageRight.png"
        }
    return to_wrap
def planes(width, height, depth):
    w, h, d = width / 2, height / 2, depth / 2

    #! Dictionary that associates name with position in space
    faces = { 
        "Right":  pv.Plane(center=(+w, 0, 0), direction=(1, 0, 0), i_size=height, j_size=depth),
        "Left":   pv.Plane(center=(-w, 0, 0), direction=(-1, 0, 0), i_size=height, j_size=depth),
        "Top":    pv.Plane(center=(0, +d, 0), direction=(0, 1, 0), i_size=height, j_size=width),
        "Bottom": pv.Plane(center=(0, -d, 0), direction=(0, -1, 0), i_size=height, j_size=width),
        "Front":  pv.Plane(center=(0, 0, +h), direction=(0, 0, 1), i_size=width, j_size=depth),
        "Back":   pv.Plane(center=(0, 0, -h), direction=(0, 0, -1), i_size=width, j_size=depth),
        }
    return faces
def textures(): 
    textures = {face: pv.read_texture(file) for face, file in texture().items()}
    return textures

        
plotter = pv.Plotter()
plane_actors = {}

for face_name, plane in planes(width, height, depth).items():
    actor = plotter.add_mesh(plane, texture=textures()[face_name])
    plane_actors[face_name] = actor

plotter.show_axes()

cuts = {"xy":100, "yz":100}

def update(): #Defines the function that will generate the new images, remove the old ones and plot the newer
    width, height, depth = image_gen(False, path, start_size, round(cuts["xy"],1), round(cuts["yz"],1))

    for actor in plane_actors.values():
        plotter.remove_actor(actor)
    plane_actors.clear()

    for face_name, plane in planes(width, height, depth).items():
        actor = plotter.add_mesh(plane, texture=textures()[face_name])
        plane_actors[face_name] = actor

    plotter.render()
    print(f'\nRendering image at XY {round(cuts["xy"],1)}% and YZ {round(cuts["yz"],1)}', end='\n')
def xy_update(value): #Defines the XY specific
    cuts["xy"] = value
    update()
def yz_update(value): #Defines the YZ Specific
    cuts["yz"] = value
    update()

plotter.add_slider_widget(
    callback=xy_update,
    rng=[10, 100],  # Slider range for YZ cut (adjust as necessary)
    value=100,       # Initial value for slider
    title="XY Cut (%)",
    style="modern",
    pointa= (0,0.92),
    pointb= (0.3, 0.92)
)

plotter.add_slider_widget(
    callback=yz_update,
    rng=[10, 100],  # Slider range for YZ cut (adjust as necessary)
    value=100,       # Initial value for slider
    title="YZ Cut (%)",
    style="modern",
    pointa= (0.3,0.92),
    pointb= (0.6, 0.92)
)

plotter.show()
