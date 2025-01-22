def filter_by_weekday(restaurants, weekday):
    """
    根據指定的星期篩選餐廳。
    
    :restaurants: 餐廳列表，包含 placeID 和 schedule。珣的那包
    :weekday: 使用者提供的星期 (1=週一, 2=週二, ..., 7=週日)。pon那包
    :return: 符合條件的 placeID 列表。
    """
    fliter_placeID = []
    for restaurant in restaurants:
        hours = restaurant.get("hours", {})
        if weekday in hours and hours[weekday] != 'none':
            fliter_placeID.append(restaurant['placeID'])
    return fliter_placeID

if __name__ == "__main__":
    # 測試數據
    restaurants = [
        {
            "placeID": 1,
            "hours": {
                1: 'none',
                2: [{'start': '09:00', 'end': '21:00'}],
                3: [{'start': '09:00', 'end': '21:00'}],
                4: [{'start': '09:00', 'end': '21:00'}],
                5: [{'start': '09:00', 'end': '21:00'}],
                6: [{'start': '09:00', 'end': '21:00'}],
                7: [{'start': '09:00', 'end': '17:00'}]
            }
        },
        {
            "placeID": 2,
            "hours": {
                1: 'none',
                2: [{'start': '10:00', 'end': '20:00'}],
                3: [{'start': '10:00', 'end': '20:00'}],
                4: [{'start': '10:00', 'end': '20:00'}],
                5: [{'start': '10:00', 'end': '20:00'}],
                6: [{'start': '10:00', 'end': '20:00'}],
                7: [{'start': '10:00', 'end': '16:00'}]
            }
        },
        {
            "placeID": 3,
            "hours": {
                1: 'none',
                2: 'none',
                3: 'none',
                4: [{'start': '12:00', 'end': '18:00'}],
                5: [{'start': '12:00', 'end': '18:00'}],
                6: [{'start': '12:00', 'end': '18:00'}],
                7: [{'start': '12:00', 'end': '18:00'}]
            }
        }
    ]

    # 使用者輸入
    user_requirements = [         
        {
            "星期別": 5,
            "時間": "16:00",
            "類別": "咖啡廳",
            "預算": 300,
            "出發地": (25.0375, 121.5637),
            "可接受距離門檻(KM)": "none",
            "交通類別": "步行"
        }
    ]
    user_weekday = user_requirements[0]['星期別']

    # 篩選結果
    open_restaurants = filter_by_weekday(restaurants, user_weekday)
    placeID = open_restaurants
    
    # 輸出符合條件的 placeID
    print("有營業的餐廳 placeID:", placeID)
