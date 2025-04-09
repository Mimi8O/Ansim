def extract_coordinates(route_data):
    coords = []

    for feature in route_data.get("features", []):
        geo = feature.get("geometry", {})
        geo_type = geo.get("type")

        if geo_type == "LineString":
            for lon, lat in geo.get("coordinates", []):
                coords.append((lat, lon))  # 위도, 경도 순
        elif geo_type == "Point":
            lon, lat = geo.get("coordinates", [])
            coords.append((lat, lon))

    return coords


def choose_eul_reul(word):
    """단어에 맞는 '을/를' 조사 선택"""
    if not word:
        return "을"
    last_char = word[-1]
    code = ord(last_char) - 0xAC00
    jong = code % 28
    return "을" if jong else "를"


def fix_description(desc, name, distance):
    name = name.strip() if name else "이름 없는 도로"
    조사 = choose_eul_reul(name)
    if not desc or desc.startswith(",") or "따라" in desc:
        return f"{name}{조사} 따라 {distance}m 이동"
    return desc


def extract_detailed_route(route_data):
    parsed = []

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
            parsed.append({
                "lat": lat,
                "lon": lon,
                "turn": turn,
                "desc": desc
            })
        elif geo_type == "LineString":
            for lon, lat in geo.get("coordinates", []):
                parsed.append({
                    "lat": lat,
                    "lon": lon,
                    "turn": turn,
                    "desc": desc
                })

    return parsed



