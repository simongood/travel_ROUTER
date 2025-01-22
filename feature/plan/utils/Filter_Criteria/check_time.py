from datetime import datetime

def is_time_in_range(start, end, arrival_time):
    """
    檢查目標時間是否在指定的時間範圍內。 
    """
    arrival_time = datetime.strptime(arrival_time, '%H:%M')
    start_time = datetime.strptime(start, '%H:%M')
    end_time = datetime.strptime(end, '%H:%M')
    return start_time <= arrival_time <= end_time


def filter_by_time_without_weekday(restaurants, arrival_time):
    """
    根據到達時間篩選營業中的餐廳，忽略星期篩選。
    :param restaurants: 餐廳列表，包含 placeID 和 schedule。
    :param arrival_time: 使用者的到達時間 (格式: 'HH:MM')。
    :return: 符合條件的 placeID 列表。
    """
    open_at_time = []
    for restaurant in restaurants:
        hours = restaurant.get("hours", {})
        for time_ranges in hours.values():
            if time_ranges == 'none':  # 當日無營業時間，跳過
                continue
            if any(is_time_in_range(time_range['start'], time_range['end'], arrival_time) for time_range in time_ranges):
                open_at_time.append(restaurant['placeID'])
                break  # 跳出日期迴圈
    return open_at_time


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

    # 使用者輸入 # 到達時間

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
    user_arrival_time = user_requirements[0]['時間']

    # 篩選符合條件的餐廳
    open_restaurants = filter_by_time_without_weekday(restaurants, user_arrival_time)
    placeID = open_restaurants

    # 輸出結果
    print("符合 16:00 營業的餐廳 placeID:", placeID)
