from flask import Blueprint, request, jsonify
from utils.gps_dummy import get_dummy_gps
from utils.tmap_api import get_route_from_tmap
from utils.tmap_parser import fix_description
import json

call_robot_bp = Blueprint('call_robot', __name__)

@call_robot_bp.route('/', methods=['POST'])
def call_robot():
    user_data = request.get_json()
    user_lat = user_data['lat']
    user_lon = user_data['lon']

    robot_location = get_dummy_gps()
    robot_lat = robot_location['lat']
    robot_lon = robot_location['lon']

    route_data = get_route_from_tmap(
        start_lon=robot_lon,
        start_lat=robot_lat,
        end_lon=user_lon,
        end_lat=user_lat
    )

    detailed_route = []

    for feature in route_data.get("features", []):
        geo = feature.get("geometry", {})
        props = feature.get("properties", {})
        geo_type = geo.get("type")

        turn = props.get("turnType", -1)
        name = props.get("name", "")
        distance = props.get("distance", 0)
        desc = fix_description(props.get("description", ""), name, distance)

        if geo_type == "Point":
            lon, lat = geo.get("coordinates", [])
            detailed_route.append({
                "lat": lat,
                "lon": lon,
                "turn": turn,
                "desc": desc
            })

        elif geo_type == "LineString":
            for lon, lat in geo.get("coordinates", []):
                detailed_route.append({
                    "lat": lat,
                    "lon": lon,
                    "turn": turn,
                    "desc": desc
                })

    # 저장
    with open("called_route.json", "w", encoding="utf-8") as f:
        json.dump(detailed_route, f, ensure_ascii=False, indent=2)

    return jsonify({
        "message": "사용자 위치까지의 경로를 저장했습니다.",
        "total_points": len(detailed_route),
        "first_2": detailed_route[:2]
    })

