import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from image_processor import find_spot_parameters
from pathlib import Path

token = os.environ.get("INFLUXDB_TOKEN")
org = "1440_test_1_image"
url = "http://localhost:8086"
bucket="Bucket_1"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)
   
pathlist = Path('./Test Data').glob('**/*.png')
for path in pathlist:
    parameters = find_spot_parameters(path)

    point = Point("spot_metrics")
    point.tag("filename", path.stem)
    point.field("std", parameters['std'])
    point.field("dispersion", parameters['dispersion'])
    point.field("position_x", parameters['position'][0])
    point.field("position_y", parameters['position'][1])

    write_api.write(bucket=bucket, org="1440_test_1_image", record=point)