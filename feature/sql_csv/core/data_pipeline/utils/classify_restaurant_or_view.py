def classify_restaurant_or_view(placeID_list: list, 
                                restaurant_view_classify: str,
                                ETL_dataframe):
    '''
    - 根據分類篩選 placeID_list 中的項目。

    ```
    Args:
        placeID_list (list): 包含 placeID 的列表 ['placeID1', 'placeID2', ....]
        classify (str): 篩選類型，'restaurant' 或 'view'
        ETL_dataframe : ETL_df 表 

    Returns:
        list: 篩選後的 placeID 列表。
    ```
    '''
    classify_map = {
        'restaurant': ["小吃", "餐廳", "咖啡廳"],
        'view': ["一般商店", "日用品商店", "休閒設施", "伴手禮商店", "室內旅遊景點", "室外旅遊景點",
                            "購物商場", "文化/歷史景點", "自然景點", "一般商店", "甜品店/飲料店"]
    }

    # 篩選邏輯
    filtered_series = ETL_dataframe['new_label_type'].loc[placeID_list]
    filtered_list = (
        filtered_series[filtered_series.isin(classify_map[restaurant_view_classify])]
        .index
        .tolist()
    )

    return filtered_list


if __name__ == '__main__':
    from feature.sql_csv.core.data_pipeline.utils.ETL_dataframe_generate import ETL_dataframe_generate
    placeID_list = [
                    'ChIJqelWmSGnQjQR0oQv0a6ZJ8o',    # 康小玲 線上書店交易平台 online bookstores
                    'ChIJI-NIexYdaDQRfldAuHBbwmY',    # 無名涼麵/雙醬涼麵/現場營業時間下午4~9點/線上營業時間24小時
                    'ChIJ28UWAQAdaDQRBDGBOwEMJIY',    # 冰品店
                    'ChIJHRHjiIOuQjQRwvkYlwIEcTQ',    # SK-II大葉高島屋專櫃
                    ]
    ETL_dataframe = ETL_dataframe_generate()
    
    placeID_list = classify_restaurant_or_view(
                                    placeID_list=placeID_list,
                                    classify='view',
                                    ETL_dataframe=ETL_dataframe,
                                    )
    print(placeID_list)