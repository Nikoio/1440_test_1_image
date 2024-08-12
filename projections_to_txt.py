import cv2
import numpy as np
from pathlib import Path

def find_projections(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    projection_x = np.sum(img, axis=0)
    projection_y = np.sum(img, axis=1)

    return {'projection_x': projection_x,
            'projection_y': projection_y}


result_str = []

pathlist = Path('./Test Data').glob('**/*.png')
for path in pathlist:
    projections = find_projections(path)

    result_str += f'{path.stem}:\n'
    result_str += f'projection_x: [{" ".join((str(i) for i in projections['projection_x']))}]\n'
    result_str += f'projection_y: [{" ".join((str(i) for i in projections['projection_y']))}]\n'

with open('projetions.txt', 'w') as f:
    f.writelines(result_str)

    