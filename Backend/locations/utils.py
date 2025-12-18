import math

def is_inside_geofence(user_lat, user_lon, center_lat, center_lon, radius):
    R = 6371000  # meters

    lat1 = math.radians(user_lat)
    lon1 = math.radians(user_lon)
    lat2 = math.radians(center_lat)
    lon2 = math.radians(center_lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance <= radius
