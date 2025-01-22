from feature.plan.utils.Norma_lization.similarity_score_normalized import normalize_similarity
from feature.plan.utils.Norma_lization.comment_score_normalized import normalize_and_match, load_extracted_data
from feature.plan.utils.Norma_lization.distances_score_normalized import calculate_reverse_normalized_distances_no_threshold

def calculate_weighted_scores(points, user_location, weights):
    """
    計算每個地點的加權總分，並排序。
    
    :param points: 地點資料列表。
    :param user_location: 使用者出發地 (lat, lon)。
    :param weights: 權重字典，包含距離、評論分數、相似性。
    :return: 排序後的地點列表，按加權分數降序排列。
    """
    # 步驟 1: 計算相似性標準化分數
    points = normalize_similarity(points)

    # 步驟 2: 加載評論數據並標準化評論總分
    emotion_analysis_path =r"./data/emotion_analysis.csv"
    extracted_data = load_extracted_data(emotion_analysis_path)
    points = normalize_and_match(points, extracted_data).to_dict(orient="records")

    # 步驟 3: 計算距離的反向標準化分數
    distance_scores = calculate_reverse_normalized_distances_no_threshold(points, user_location)
    distance_map = {d['place_id']: d['distance_normalized_score'] for d in distance_scores}
    for point in points:
        point['distance_normalized_score'] = distance_map.get(point['place_id'], 0)

    # 步驟 4: 計算加權總分
    for point in points:
        point['weighted_score'] = (
            weights['distance'] * point.get('distance_normalized_score', 0) +
            weights['comments'] * point.get('comment_score_normalized', 0) +
            weights['similarity'] * point.get('retrival_Normalization', 0)
        )

    # 步驟 5: 排序
    points.sort(key=lambda x: x['weighted_score'], reverse=True)
    return points[:10]


if __name__ == "__main__":
    # 測試數據
    points = [
        {
            'place_id': 'ChIJ-aSxVAAdaDQR69yHKL4i-jc',
            'place_name': '店名1',
            'rating': 4.5,
            'retrival_score': 0.8,
            'comments': 150,
            'lat': 25.0375,
            'lon': 121.5637,
            'new_label_type': '咖啡廳',
            'hours': {
                1: [{'start': '09:00', 'end': '21:00'}],
                2: [{'start': '09:00', 'end': '21:00'}],
                3: 'none',
                4: [{'start': '09:00', 'end': '21:00'}],
                5: [{'start': '09:00', 'end': '21:00'}],
                6: [{'start': '09:00', 'end': '21:00'}],
                7: [{'start': '09:00', 'end': '17:00'}],
            },
            'new_avg_cost': 300,
            'Location_URL': 'https://example.com',
            '圖片URL': 'https://example.com',
        },
        {
            'place_id': 'ChIJ-8OvfTepQjQR6_LN00q5_IY',
            'place_name': '店名1',
            'rating': 4.5,
            'retrival_score': 0.8,
            'comments': 150,
            'lat': 25.0375,
            'lon': 121.5637,
            'new_label_type': '咖啡廳',
            'hours': {
                1: [{'start': '09:00', 'end': '21:00'}],
                2: [{'start': '09:00', 'end': '21:00'}],
                3: 'none',
                4: [{'start': '09:00', 'end': '21:00'}],
                5: [{'start': '09:00', 'end': '21:00'}],
                6: [{'start': '09:00', 'end': '21:00'}],
                7: [{'start': '09:00', 'end': '17:00'}],
            },
            'new_avg_cost': 300,
            'Location_URL': 'https://example.com',
            '圖片URL': 'https://example.com',
        },
        {
            'place_id': 'ChIJ-2qAiBJTXTQRFT23-FNNQwg',
            'place_name': '店名2',
            'rating': 4.2,
            'retrival_score': 0.7,
            'comments': 120,
            'lat': 25.0402,
            'lon': 121.5657,
            'new_label_type': '餐廳',
            'hours': {
                1: 'none',
                2: [{'start': '10:00', 'end': '20:00'}],
                3: [{'start': '10:00', 'end': '20:00'}],
                4: [{'start': '10:00', 'end': '20:00'}],
                5: [{'start': '10:00', 'end': '20:00'}],
                6: [{'start': '10:00', 'end': '20:00'}],
                7: [{'start': '10:00', 'end': '16:00'}],
            },
            'new_avg_cost': 500,
            'Location_URL': 'https://example.com',
            '圖片URL': 'https://example.com',
        },
    ]
    # 使用者位置
    user_location = (25.0375, 121.5637)

    # 權重設定
    weights = {
        'distance': 0.2,   # 距離 20%
        'comments': 0.4,   # 評論總分 40%
        'similarity': 0.4, # 相似性 40%
    }

    # 計算排序結果
    sorted_points = calculate_weighted_scores(points, user_location, weights)

    # 輸出結果
    print("加權總分排序結果:")
    for point in sorted_points:
        print(f"Place ID: {point['place_id']}, Weighted Score: {point['weighted_score']:.2f}")

