import requests
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

def get_route_from_tmap(start_lon, start_lat, end_lon, end_lat):
    api_key = os.getenv("TMAP_API_KEY")
    url = "https://apis.openapi.sk.com/tmap/routes/pedestrian"
    
    print(api_key)

    headers = {
        "appKey": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "startX": start_lon,
        "startY": start_lat,
        "endX": end_lon,
        "endY": end_lat,
        "reqCoordType": "WGS84GEO",
        "resCoordType": "WGS84GEO",
        "startName": "로봇위치",
        "endName": "사용자위치"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def get_coordinates_from_keyword(keyword):
    api_key = os.getenv("TMAP_API_KEY")
    url = "https://apis.openapi.sk.com/tmap/pois"

    params = {
        "version": 1,
        "searchKeyword": keyword,
        "resCoordType": "WGS84GEO",
        "reqCoordType": "WGS84GEO",
        "count": 1
    }

    headers = {
        "appKey": api_key
    }

    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    if result.get("searchPoiInfo", {}).get("pois", {}).get("poi"):
        poi = result["searchPoiInfo"]["pois"]["poi"][0]
        lat = float(poi["frontLat"])
        lon = float(poi["frontLon"])
        return lat, lon
    else:
        return None, None

