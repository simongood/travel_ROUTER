import ast

def plan_point_make(place_ID: str, retrival_score: float, ETL_dataframe):
    '''
    ```
    Args:
        place_ID : 單個 place_ID
        retrival_score : 向量搜尋相似度分數
        ETL_dataframe : ETL csv dataframe
    return :
        point : 給 情境搜尋端 的單個point格式
    ```
    ---
    - point =

        ```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        {   
            'placeID' : str,            
            'place_name' : '店名1',
            'rating' : 1-5,             # googlemap 星數
            'retrival_score' : float,   # 向量分數
            'comments' : int            # 評論數
            'lat' : float,
            'lon' : float,
            'new_label_type' : str      # 大分類
            'hours' : { 
                    1: [{'start': '14:30', 'end': '21:00'}],
                    2: [{'start': '14:30', 'end': '21:00'}],
                    3: 'none', 
                    4: [{'start': '14:30', 'end': '21:00'}], 
                    5: [{'start': '14:30', 'end': '21:00'}], 
                    6: [{'start': '14:30', 'end': '21:00'}], 
                    7: [{'start': '14:30', 'end': '21:00'}]  
                },
            'new_avg_cost' : int,       # 新價格(清理過)
            'Location_URL' : https://example.com        # googlemap url 
            '圖片URL' : https://example.com
        }
        ```
    '''

    filter_series = ETL_dataframe.loc[place_ID]
    point = {
                'placeID': place_ID,
                'place_name': filter_series['place_name'],
                'rating': float(filter_series['rating']),
                'retrival_score': float(retrival_score),
                'comments': int(filter_series['comments']),
                'lat': float(filter_series['lat']),
                'lon': float(filter_series['lon']),
                'new_label_type': filter_series['new_label_type'],
                'hours': ast.literal_eval(filter_series['hours']),      # 字串 hours 格式 轉 dict 格式輸出
                'new_avg_cost': int(filter_series['new_avg_cost']),
                'location_url': filter_series['location_url'],
                'image_url': filter_series['image_url']
            }


    return point



if __name__ == '__main__':
    from pprint import pprint

    from feature.sql_csv.core.data_pipeline.utils.ETL_dataframe_generate import ETL_dataframe_generate
    ETL_dataframe = ETL_dataframe_generate()
    place_ID = 'ChIJqelWmSGnQjQR0oQv0a6ZJ8o'  # 康小玲      ['外帶外送', '其他支付']
    retrival_score = 0.7

    point = plan_point_make(
                place_ID= place_ID,
                retrival_score= retrival_score,
                ETL_dataframe= ETL_dataframe,
            )

    pprint(point, sort_dicts=False)