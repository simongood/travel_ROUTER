from geopy.distance import geodesic

def filter_by_distance(points, start_location, max_distance_km):
    """
    根據距離篩選餐廳。
    
    :restaurants: 餐廳列表，每個地點包含 placeID 和經緯度。
    :start_location: 出發地的經緯度 (lat, lon)。
    :max_distance_km: 可接受的距離門檻（公里）。
    :return: 符合條件的 placeID 列表。
    """
    matching_places = []
    for points in points:
        points_location = (points['lat'], points['lon'])
        distance = geodesic(start_location, points_location).kilometers
        # 計算兩點的位置
        if distance <= max_distance_km:
            matching_places.append(points['placeID'])
    return matching_places


if __name__ == "__main__":
    # 測試數據
    points = [
        {'placeID': 1, 'lon': 121.5171, 'lat': 25.0478},
        {'placeID': 2, 'lon': 121.5314, 'lat': 25.0645},
        {'placeID': 3, 'lon': 121.5078, 'lat': 25.0339},
        {'placeID': 4, 'lon': 121.5289, 'lat': 25.0356},
        {'placeID': 5, 'lon': 121.4952, 'lat': 25.0213},
        {'placeID': 6, 'lon': 121.5501, 'lat': 25.0483},
        {'placeID': 7, 'lon': 121.5156, 'lat': 25.0612},
        {'placeID': 8, 'lon': 121.5082, 'lat': 25.0653},
        {'placeID': 9, 'lon': 121.5427, 'lat': 25.0296},
        {'placeID': 10, 'lon': 121.5209, 'lat': 25.0501},
        {'placeID': 11, 'lon': 121.4935, 'lat': 25.0462}
    ]

    user_info = [
        {
            "星期別": 1,
            "時間": "10:00",
            "類別": "餐廳",
            "預算": 700,
            "出發地": (25.0478, 121.5171),
            "可接受距離門檻(KM)":1,
            "交通類別": "步行"
        }
    ]

    # 使用者輸入
    start_location = user_info[0]['出發地']  # 出發地
    max_distance_km = user_info[0]['可接受距離門檻(KM)']  # 距離門檻

    # 篩選符合條件的餐廳
    matching_places = filter_by_distance(points, start_location, max_distance_km)

    # 輸出結果
    print(f"距離出發地小於 {max_distance_km} 公里的地點 placeID:", matching_places)
