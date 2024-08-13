import json

from image_processor import find_spot_parameters
from pathlib import Path

results = []

pathlist = Path('./Test Data').glob('**/*.png')
for path in pathlist:
    parameters = find_spot_parameters(path)

    results.append({
        'filename': path.stem,
        'std': parameters['std'], 
        'dispersion': parameters['dispersion'],
        'position': parameters['position']
    })

with open('image_metrics.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)