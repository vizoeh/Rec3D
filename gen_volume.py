import pyvista as pv
import glob, os

def render(width : int, height : int, depth : int):

    """
    Renders the cube using pyvista.\n
    Parameters:
        width : width of the box
        height : lenght of the box (counter-intuitive, I know!)
        depth : height of the box

    """

    #! Simple dictionary that associates the position with the file.
    to_wrap = {"Top":"./temp/imageTop.png",
            "Bottom":"./temp/imageBottom.png",
            "Front":"./temp/imageFront.png",
            "Back":"./temp/imageBack.png",
            "Left":"./temp/imageLeft.png",
            "Right":"./temp/imageRight.png"
    }

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

    textures = {face: pv.read_texture(file) for face, file in to_wrap.items()}
    
    plotter = pv.Plotter()

    for face_name, plane in faces.items():
        plotter.add_mesh(plane, texture=textures[face_name])

    plotter.show_axes()
    plotter.show()

if __name__ == "__main__":
    render(1000,1000,48)