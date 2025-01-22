

from feature.sql_csv.core.data_pipeline.filter_pipeline import filter_pipeline
from feature.sql_csv.core.point_maker.plan_point_maker import plan_point_make
from feature.sql_csv.core.data_pipeline.utils.ETL_dataframe_generate import ETL_dataframe_generate

def plan_system(system_input: list[dict], special_request_list):
    '''
    ```
    Args: 
        system_input : 情境搜索端含分數的向量搜尋結果
        special_request_list : 特殊要求
    return:
        points : 傳給 情境搜尋的資料
    ```

    '''
    placeID_list = system_input[0].keys()
    
    # 篩選
    placeID_list = filter_pipeline(
                                    placeID_list=placeID_list,
                                    restaurant_view_classify='',
                                    special_request_list=special_request_list,
                                )
    
    # 製造 points
    points = []
    for placeID in placeID_list:
        point = plan_point_make(
                                place_ID=placeID,
                                retrival_score=system_input[0][placeID]['分數'],
                                ETL_dataframe=ETL_dataframe_generate(),
                            )
        points.append(point)

    return points


if __name__ == '__main__':
    from pprint import pprint

    plan_system_input = [{
                            'ChIJqelWmSGnQjQR0oQv0a6ZJ8o':{"分數": 0.5} ,  # 康小玲      ['外帶外送', '其他支付']
                            'ChIJI-NIexYdaDQRfldAuHBbwmY':{"分數": 0.6} ,  # 無名涼麵    ['現金']
                            'ChIJ28UWAQAdaDQRBDGBOwEMJIY':{"分數": 0.7} ,  # 冰品店      ['外帶外送', '內用座位']
                            'ChIJHRHjiIOuQjQRwvkYlwIEcTQ':{"分數": 0.8} ,  # SK-II       ['無障礙', '其他支付']
                        }]
    special_request_list = [{ '其他支付': True,}]
    
    points = plan_system (
                        system_input=plan_system_input, 
                        special_request_list=special_request_list,
                    )
    
    pprint(points, sort_dicts=False)



