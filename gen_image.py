from PIL import Image, ImageEnhance
import os,  glob

def image_gen(inSpacing, stack_path, start_size, YZ):

    #? Creates an ordered list with all images ending with [double-digit number].png, ex: image00.png, image01.png ... image99.png
    image_files = sorted(
    glob.glob(os.path.join(stack_path, "[0-9][0-9].png")))

    #? Defines the top and bottom images, saving the top most image's dimensions
    imageTop, imageBottom = map(Image.open, (image_files[0], image_files[-1]))
    width, height = imageTop.size
    print(f"Stack dimensions: {width} x {height} - based on first image at {round(YZ,1)}%")

    cut_yz = int(YZ*width/100) 

    print(cut_yz)

    match inSpacing:
        case True:

            # Asks for a valid spacing distance
            print("Spacing distance (px)?")
            spacing = int(input())

            #? Creates the blank images that will become the side views
            imageRight = Image.new('RGB', (height, len(image_files)*spacing), (255,255,255))
            imageLeft = Image.new('RGB', (height, len(image_files)*spacing), (255,255,255))
            imageFront = Image.new('RGB', (height, len(image_files)*spacing), (255,255,255))
            imageBack = Image.new('RGB', (width, len(image_files)*spacing), (255,255,255))

            c = 0
            for imagePath in image_files:

                print(f'\rCurrently working image {image_files.index(imagePath)+1}/{len(image_files)}', end='')

                 # Turns the path from the image_files list into a PngImageFile object
                image = Image.open(imagePath)

                # Checking for possible errors
                if image.width != width or image.height != height:
                    print("ALL images in stack must have same dimensions")
                    break
                elif len(image_files) != len(start_size):
                    print("CSV file doesn't account for all image files")
                    break

                #! Crops the LAST pixel row/column in the current image to create size images. - MUST ACCOUNT FOR CROP!
                rowRight = image.crop((cut_yz-1,0,cut_yz,height)).rotate(-90, expand = True)
                imageRight.paste(rowRight.resize((height,spacing)), (0,c))

                rowLeft = image.crop((0,0,1,height)).rotate(90, expand = True)
                imageLeft.paste(rowLeft.resize((height,spacing)), (0,c))

                rowFront = image.crop((0,height-1,cut_yz,height))
                imageFront.paste(rowFront.resize((cut_yz,spacing)), (0,c))

                rowBack = image.crop((0,0,cut_yz,1)).rotate(180, expand = True)
                imageBack.paste(rowBack.resize((cut_yz,spacing)), (0,c))
                c += spacing


        case False:

            fac = 1 # Factor by which you multiply each coordinate
            # Variable that saves the volume depth
            temp = int((start_size[-1][0] + start_size[-1][1])*fac)

            #? Creates the blank images that will become the side views
            imageRight = Image.new('RGB', (height, temp), (255,255,255))
            imageLeft = Image.new('RGB', (height, temp), (255,255,255))
            imageFront = Image.new('RGB', (cut_yz, temp), (255,255,255))
            imageBack = Image.new('RGB', (cut_yz, temp), (255,255,255))
            print("Volume depth (px):", temp)

            c = 0
            for imagePath in image_files:

                print(f'\rCurrently working image {image_files.index(imagePath)+1}/{len(image_files)}', end='')

                 # Turns the path from the image_files list into a PngImageFile object
                image = Image.open(imagePath)

                # Checking for possible errors
                if image.width != width or image.height != height:
                    print("ALL images in stack must have same dimensions")
                    break
                elif len(image_files) != len(start_size):
                    print("CSV file doesn't account for all image files")
                    break
                
                rowRight = image.crop((cut_yz-1,0,cut_yz,height)).rotate(-90, expand = True)
                imageRight.paste(rowRight.resize((height,int(start_size[c][1]*fac))), (0, int(start_size[c][0]*fac)))

                rowLeft = image.crop((0,0,1,height)).rotate(90, expand = True)
                imageLeft.paste(rowLeft.resize((height,int(start_size[c][1]*fac))), (0, int(start_size[c][0]*fac)))

                rowFront = image.crop((0,height-1,cut_yz,height))
                imageFront.paste(rowFront.resize((cut_yz,int(start_size[c][1]*fac))), (0, int(start_size[c][0]*fac)))

                rowBack = image.crop((0,0,cut_yz,1)).rotate(180, expand = True)
                imageBack.paste(rowBack.resize((cut_yz,int(start_size[c][1]*fac))), (0, int(start_size[c][0]*fac)))
                c += 1
    

    imageBack.save("./temp/imageBack.png")
    imageFront.save("./temp/imageFront.png")
    imageLeft.save("./temp/imageLeft.png")

    if cut_yz == "full:":
        imageRight.save("./temp/imageRight.png")
    else: ImageEnhance.Brightness(imageRight).enhance(0.6).save("./temp/imageRight.png")

    imageBottom.crop((0,0,cut_yz,height)).rotate(90, expand=True).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save("./temp/imageBottom.png")
    imageTop.rotate(-90, expand=True).crop((0,0,height,cut_yz)).save("./temp/imageTop.png")

    """
    Saves four side images for reconstruction, and returns a list containing: [width, "height" (lenght), depth]
    """
    return [cut_yz,height,imageFront.height]

if __name__ == '__main__':
    from csv_reader import start_size
    image_gen(False,"./image_stack_pre", start_size, 100)