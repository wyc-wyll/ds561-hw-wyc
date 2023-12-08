from __future__ import annotations
import sqlalchemy
import socket
import platform

from collections import defaultdict
from collections.abc import Iterable

from google.cloud import compute_v1

project_id = "ds561-wyc-f2023"
region = "us-east1"
instance_name = "hw5--db"

def getZone(
    project_id: str,
):
    
    instance_client = compute_v1.InstancesClient()
    request = compute_v1.AggregatedListInstancesRequest()
    request.project = project_id
    request.max_results = 50

    agg_list = instance_client.aggregated_list(request=request)

    zone_result = 'No Match'
    for zone, response in agg_list:
        for instance in response.instances:
            if (instance.name == socket.gethostname()):
                zone_result = zone
    return zone_result

print(getZone(project_id=project_id))