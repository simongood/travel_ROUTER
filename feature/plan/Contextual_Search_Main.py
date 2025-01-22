from feature.plan.utils.Filter_Criteria.check_class import filter_by_label_type
from feature.plan.utils.Filter_Criteria.check_budget import filter_by_budget
from feature.plan.utils.Filter_Criteria.check_distance import filter_by_distance
from feature.plan.utils.Filter_Criteria.check_date import filter_by_weekday
from feature.plan.utils.Filter_Criteria.check_time import filter_by_time_without_weekday
from feature.plan.utils.Norma_lization.similarity_score_normalized import normalize_similarity
from feature.plan.utils.Norma_lization.comment_score_normalized import normalize_and_match, load_extracted_data
from feature.plan.utils.Norma_lization.distances_score_normalized import calculate_reverse_normalized_distances_no_threshold


def main(points, user_requirements):
    """
    根據使用者需求篩選符合條件的餐廳。
    
    :param points: 資料列表。
    :param user_requirements: 使用者需求列表。
    :return: 符合條件的餐廳 placeID 列表。
    """
    user_filters = user_requirements[0]
    matching_placeID = set(r['placeID'] for r in points)

    # 篩選條件
    desired_label = user_filters.get("類別")
    if desired_label != "none":
        matching_placeID.intersection_update(filter_by_label_type(points, desired_label))

    user_budget = user_filters.get("預算")
    if user_budget != "none":
        matching_placeID.intersection_update(filter_by_budget(points, user_budget))

    start_location = user_filters.get("出發地", "none")
    max_distance_km = user_filters.get("可接受距離門檻(KM)", "none")
    if max_distance_km == "none":
        max_distance_km = 100
    else:
        max_distance_km = float(max_distance_km)

    if start_location == "none":
        start_location = (25.0418, 121.5654)

    matching_placeID.intersection_update(filter_by_distance(points, start_location, max_distance_km))

    user_weekday = user_filters.get("星期別")
    if user_weekday != "none":
        matching_placeID.intersection_update(filter_by_weekday(points, user_weekday))

    user_arrival_time = user_filters.get("時間")
    if user_arrival_time != "none":
        matching_placeID.intersection_update(filter_by_time_without_weekday(points, user_arrival_time))

    return list(matching_placeID)


def calculate_weighted_scores(points, user_location, weights):
    """
    計算每個地點的加權總分，並僅返回指定欄位。
    
    :param points: 地點資料列表。
    :param user_location: 使用者出發地 (lat, lon)。
    :param weights: 權重字典，包含距離、評論分數、相似性。
    :return: 排序後的前 10 地點列表（僅包含指定欄位）。
    """
    points = normalize_similarity(points)
    emotion_analysis_path = r"./data/emotion_analysis.csv"
    extracted_data = load_extracted_data(emotion_analysis_path)
    points = normalize_and_match(points, extracted_data).to_dict(orient="records")

    distance_scores = calculate_reverse_normalized_distances_no_threshold(points, user_location)
    distance_map = {d['placeID']: d['distance_normalized_score'] for d in distance_scores}
    for point in points:
        point['distance_normalized_score'] = distance_map.get(point['placeID'], 0)

    for point in points:
        point['weighted_score'] = (
            weights['distance'] * point.get('distance_normalized_score', 0) +
            weights['comments'] * point.get('comment_score_normalized', 0) +
            weights['similarity'] * point.get('retrival_Normalization', 0)
        )

    points.sort(key=lambda x: x['weighted_score'], reverse=True)
    
    # 過濾需要的欄位
    required_fields = {'placeID', 'place_name', 'rating', 'lat', 'lon', 'new_avg_cost', 'hours', 'Location_URL', 'image_url'}
    filtered_points = [
        {k: v for k, v in point.items() if k in required_fields}
        for point in points[:10]
    ]
    
    return filtered_points

def filter_and_calculate_scores(points, user_requirements, weights):
    """
    篩選地點並計算加權總分。
    
    :param points: 地點資料列表。
    :param user_requirements: 使用者需求列表。
    :param weights: 權重字典，包含距離、評論分數、相似性。
    :return: 排序後的前 10 地點列表（僅包含指定欄位）。
    """
    # 篩選符合條件的 placeID
    filtered_placeID = main(points, user_requirements)

    # 從原始資料中篩選符合條件的地點
    filtered_points = [point for point in points if point['placeID'] in filtered_placeID]

    # 檢查篩選結果是否為空
    if not filtered_points:
        print("No places match the given criteria.")
        return []

    # 計算加權總分並排序
    user_location = user_requirements[0].get("出發地", (25.0418, 121.5654))  # 預設台北車站
    if user_location == "none":
        user_location = (25.0418, 121.5654)

    sorted_points = calculate_weighted_scores(filtered_points, user_location, weights)
    
    return sorted_points


if __name__ == "__main__":
    from pprint import pprint
    # 測試數據
    points = [
    {
        'placeID': 'ChIJocPd9VEdaDQRkSOV5E-sUtA',
        'place_name': '有夠香串燒',
        'rating': 4.9,
        'retrival_score': 0.8313335,
        'comments': 10,
        'lat': 25.0188387,
        'lon': 121.4100592,
        'new_label_type': '餐廳',
        'hours': {
            1: 'none',
            2: [{'start': '16:00', 'end': '23:00'}],
            3: [{'start': '16:00', 'end': '23:00'}],
            4: [{'start': '16:00', 'end': '23:00'}],
            5: [{'start': '16:00', 'end': '23:00'}],
            6: [{'start': '09:00', 'end': '17:00'}],
            7: 'none'
        },
        'new_avg_cost': 250,
        'location_url': 'https://www.google.com/maps/place/?q=place_id:ChIJocPd9VEdaDQRkSOV5E-sUtA',
        'image_url': 'https://lh5.googleusercontent.com/p/AF1QipN5s8Q1dcqUrzRL7Q9oY3Vwsn_t_Xsij9pCQKyL=w408-h724-k-no'
    },
    {
        'placeID': 'ChIJWdNbzTOpQjQRU-20gLib18A',
        'place_name': '瑞龍早點',
        'rating': 4.3,
        'retrival_score': 0.8297816,
        'comments': 47,
        'lat': 25.0913426,
        'lon': 121.4462196,
        'new_label_type': '餐廳',
        'hours': {
            1: 'none',
            2: [{'start': '08:00', 'end': '14:00'}],
            3: [{'start': '08:00', 'end': '14:00'}],
            4: [{'start': '08:00', 'end': '14:00'}],
            5: [{'start': '08:00', 'end': '14:00'}],
            6: [{'start': '08:00', 'end': '14:00'}],
            7: [{'start': '08:00', 'end': '14:00'}]
        },
        'new_avg_cost': 150,
        'location_url': 'https://www.google.com/maps/place/?q=place_id:ChIJWdNbzTOpQjQRU-20gLib18A',
        'image_url': 'https://lh5.googleusercontent.com/p/AF1QipN5e8B3NR1tQWTcCCJ-8SaPsNeqRwM62BjvZHSU=w408-h272-k-no'
    },
    {
        'placeID': 'ChIJP32vueGrQjQRPgNBS1YU0HA',
        'place_name': '小巷子私廚麵舖',
        'rating': 4.3,
        'retrival_score': 0.8214917,
        'comments': 68,
        'lat': 25.0050485,
        'lon': 121.6012979,
        'new_label_type': '小吃',
        'hours': {
            1: [{'start': '11:15', 'end': '14:00'}, {'start': '17:00', 'end': '20:00'}],
            2: [{'start': '11:15', 'end': '14:00'}, {'start': '17:00', 'end': '20:00'}],
            3: [{'start': '11:15', 'end': '14:00'}, {'start': '17:00', 'end': '20:00'}],
            4: [{'start': '11:15', 'end': '14:00'}, {'start': '17:00', 'end': '20:00'}],
            5: [{'start': '11:15', 'end': '14:00'}, {'start': '17:00', 'end': '20:00'}],
            6: 'none',
            7: 'none'
        },
        'new_avg_cost': 150,
        'location_url': 'https://www.google.com/maps/place/?q=place_id:ChIJP32vueGrQjQRPgNBS1YU0HA',
        'image_url': 'https://lh5.googleusercontent.com/p/AF1QipPW-c-9RJSVDC21DCriO7kZvxxOP85MUMMBtp1p=w408-h305-k-no'
    },
    {
        'placeID': 'ChIJf9sPh3McaDQRcUl1hns5Kek',
        'place_name': '魯國滷味（北大店）',
        'rating': 3.1,
        'retrival_score': 0.81893075,
        'comments': 34,
        'lat': 24.9469853,
        'lon': 121.380295,
        'new_label_type': '小吃',
        'hours': {
            1: [{'start': '15:00', 'end': '21:00'}],
            2: [{'start': '15:00', 'end': '21:00'}],
            3: [{'start': '15:00', 'end': '21:00'}],
            4: [{'start': '15:00', 'end': '21:00'}],
            5: [{'start': '15:00', 'end': '21:00'}],
            6: [{'start': '15:00', 'end': '21:00'}],
            7: [{'start': '15:00', 'end': '21:00'}]
        },
        'new_avg_cost': 250,
        'location_url': 'https://www.google.com/maps/place/?q=place_id:ChIJf9sPh3McaDQRcUl1hns5Kek',
        'image_url': 'https://lh5.googleusercontent.com/p/AF1QipN-UqEPpWOZHAJj8RM6nS0fUHUxjhd1uy3G-iBY=w408-h544-k-no'
        }
        ]


    # 測試使用者需求
    user_requirements = [
        {
            "星期別": 2,
            "hours": "none",
            "類別": "none",
            "預算": 200,
            "出發地": (25.0478, 121.5171),
            "可接受距離門檻(KM)": "none",
            "交通類別": "步行",
        }
    ]

    weights = {'distance': 0.2, 'comments': 0.4, 'similarity': 0.4}

    results = filter_and_calculate_scores(points, user_requirements, weights)
    print("Filtered and Sorted Results:")
    for result in results:
        pprint(result,sort_dicts=False) 

        # filtered_placeID = main(points, user_requirements)
        # filtered_points = [point for point in points if point['placeID'] in filtered_placeID]
        # sorted_results = calculate_weighted_scores(filtered_points, (25.0375, 121.5637), weights)

        # print("排序結果:")
        # for result in sorted_results:
        #     pprint(result, sort_dicts=False)
        
