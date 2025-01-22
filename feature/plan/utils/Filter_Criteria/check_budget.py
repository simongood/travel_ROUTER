def filter_by_budget(restaurants, user_budget, tolerance=150):
    """
    根據使用者的預算篩選餐廳。
    
    :restaurants: 餐廳列表，每個地點包含 placeID 和 new_avg_cost。
    :user_budget: 使用者的預算值。
    :tolerance: 預算容差範圍，默認為 150 元。
    :return: 符合條件的 placeID 列表。
    """
    matching_places = []
    for restaurant in restaurants:
        avg_cost = restaurant.get("new_avg_cost", None)
        if avg_cost is None:
            continue  # 如果沒有價格數據，跳過此餐廳(有可能嗎?)
        if user_budget - tolerance <= avg_cost <= user_budget + tolerance:
            matching_places.append(restaurant['placeID'])
    return matching_places


if __name__ == "__main__":
    # 測試數據
    restaurants = [
        {"placeID": 1, "new_avg_cost": 300},
        {"placeID": 2, "new_avg_cost": 500},
        {"placeID": 3, "new_avg_cost": 1000},
        {"placeID": 4, "new_avg_cost": 2000},
        {"placeID": 5, "new_avg_cost": 800},
        {"placeID": 6, "new_avg_cost": 1200},
        {"placeID": 7, "new_avg_cost": 700},
        {"placeID": 8, "new_avg_cost": 400}
    ]

    user_requirements = [
        {
            "星期別": 1,
            "時間": "10:00",
            "類別": "餐廳",
            "預算": 700,
            "出發地": (25.0478, 121.5171),
            "可接受距離門檻(KM)": 10,
            "交通類別": "步行"
        }
    ]

    # 使用者輸入的預算
    user_budget = user_requirements[0].get("預算", 0)

    # 篩選符合條件的餐廳
    matching_places = filter_by_budget(restaurants, user_budget)
    placeID = matching_places
    # 輸出結果
    print(f"符合預算 {user_budget} ±150 元的 placeID:", placeID)
