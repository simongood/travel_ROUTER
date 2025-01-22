from feature.sql_csv.core.data_pipeline.filter_pipeline import filter_pipeline
from feature.sql_csv.core.point_maker.trip_point_maker import trip_point_make
from feature.sql_csv.core.data_pipeline.utils.ETL_dataframe_generate import ETL_dataframe_generate

def trip_system(system_input, special_request_list):
    '''
     ```
    Args: 
        system_input : 旅遊推薦端的向量搜尋結果 (五包)
        special_request_list : 特殊要求
    return:
        points : 傳給 旅遊推薦的資料 (含 period)
    ```
    '''

    # 篩選
    for period, placeID_list in system_input.copy().items():
        if period in ['morning', 'afternoon', 'night']:
            placeID_list = filter_pipeline(
                                    placeID_list=placeID_list,
                                    restaurant_view_classify='view',
                                    special_request_list=special_request_list,
                                )
            system_input[period] = placeID_list
        elif period in ['lunch', 'dinner']:
            placeID_list = filter_pipeline(
                                    placeID_list=placeID_list,
                                    restaurant_view_classify='restaurant',
                                    special_request_list=special_request_list,
                                )
            system_input[period] = placeID_list

    # 製造 points
    ETL_dataframe = ETL_dataframe_generate()
    points = []
    for period, placeID_list in system_input.items():
        for place_ID in placeID_list:
            point = trip_point_make(
                        place_ID=place_ID,
                        period=period,
                        ETL_dataframe=ETL_dataframe,
                    )
            points.append(point)
            


    return points


if __name__ == "__main__":
    from pprint import pprint

    placeID_list = [
                'ChIJqelWmSGnQjQR0oQv0a6ZJ8o',    # 康小玲      ['外帶外送', '其他支付']
                'ChIJI-NIexYdaDQRfldAuHBbwmY',    # 無名涼麵    ['現金']
                'ChIJ28UWAQAdaDQRBDGBOwEMJIY',    # 冰品店      ['外帶外送', '內用座位']
                'ChIJHRHjiIOuQjQRwvkYlwIEcTQ',    # SK-II       ['無障礙', '其他支付']
                ]
    
    trip_system_input = {
                            'morning': placeID_list,
                            'lunch' : placeID_list,                         
                        }
    special_request_list=[{'現金': False}]
    
    result = trip_system(
                            system_input=trip_system_input,
                            special_request_list=special_request_list,
                        )
    
    pprint(result, sort_dicts=False)