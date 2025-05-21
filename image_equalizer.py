from PIL import Image
import numpy as np
import cv2

def image_stats(image):
    (l, a, b) = cv2.split(image.astype("float32"))
    return (l.mean(), l.std(), a.mean(), a.std(), b.mean(), b.std())

def color_transfer_pil(source_pil, target_pil):
    # Converte PIL para NumPy (RGB)
    source = np.array(source_pil)
    target = np.array(target_pil)

    # Converte RGB para BGR (para OpenCV)
    source = cv2.cvtColor(source, cv2.COLOR_RGB2BGR)
    target = cv2.cvtColor(target, cv2.COLOR_RGB2BGR)

    # Converte para LAB
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    # Estatísticas
    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_stats(source)
    (lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = image_stats(target)

    (l, a, b) = cv2.split(target)

    # Evita divisão por zero
    l = ((l - lMeanTar) * (lStdSrc / np.where(lStdTar == 0, 1, lStdTar))) + lMeanSrc
    a = ((a - aMeanTar) * (aStdSrc / np.where(aStdTar == 0, 1, aStdTar))) + aMeanSrc
    b = ((b - bMeanTar) * (bStdSrc / np.where(bStdTar == 0, 1, bStdTar))) + bMeanSrc

    # Combina, clampa, e volta para uint8
    transfer = cv2.merge([l, a, b])
    transfer = np.clip(transfer, 0, 255).astype("uint8")

    # Volta para BGR e depois RGB
    transfer = cv2.cvtColor(transfer, cv2.COLOR_LAB2BGR)
    transfer = cv2.cvtColor(transfer, cv2.COLOR_BGR2RGB)

    # Converte para PIL
    return Image.fromarray(transfer)

import os,  glob

orig_path = "./image_stack_pre/"
outp_path = "./image_stack/"

for filename in os.listdir(outp_path):
   file_path = os.path.join(outp_path, filename)
   if os.path.isfile(file_path):
      os.remove(file_path)

print(f'Removed all files from {outp_path}')

source_name = "./image_stack_pre\\03.png"
source = Image.open(source_name)

image_files = sorted(
    glob.glob(os.path.join(orig_path, "[0-9][0-9].png")))

for img in image_files:
    name = img[-6:]
    if img != source_name:
        target = Image.open(img)
        result = color_transfer_pil(source, target)
    else:
        result = Image.open(img)
    result.save(f'./image_stack/{name}')

print("Equalized all images successfully")