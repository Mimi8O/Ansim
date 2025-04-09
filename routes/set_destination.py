from flask import Blueprint, request, jsonify
from utils.gps_dummy import get_dummy_gps
from utils.tmap_api import get_route_from_tmap, get_coordinates_from_keyword
from utils.tmap_parser import extract_coordinates, extract_detailed_route
import json


set_destination_bp = Blueprint('set_destination', __name__)

@set_destination_bp.route('/', methods=['POST'])

def set_destination():
    data = request.get_json()
    keyword = data.get("destination")

    if not keyword:
        return jsonify({"error": "목적지가 누락되었습니다."}), 400

    # 장소 이름 → 좌표 변환
    dest_lat, dest_lon = get_coordinates_from_keyword(keyword)

    if not dest_lat or not dest_lon:
        return jsonify({"error": "목적지를 찾을 수 없습니다."}), 404

    # 출발지: 더미 GPS
    robot_location = get_dummy_gps()
    robot_lat = robot_location['lat']
    robot_lon = robot_location['lon']

    # 경로 요청
    route_data = get_route_from_tmap(
        start_lon=robot_lon,
        start_lat=robot_lat,
        end_lon=dest_lon,
        end_lat=dest_lat
    )
    
    # 경로 좌표 추출
    route_coords = extract_coordinates(route_data)
    
    # 상세 경로 정보 추출
    detailed_route = extract_detailed_route(route_data)

    # JSON 파일로 저장
    with open("last_route.json", "w", encoding='utf-8') as f:
        json.dump(detailed_route, f, ensure_ascii=False, indent=2)

    return jsonify({
        "message": f"{keyword}까지의 경로를 저장했습니다.",
        "total_points": len(detailed_route),
        "first_2": detailed_route[:2]
    })

