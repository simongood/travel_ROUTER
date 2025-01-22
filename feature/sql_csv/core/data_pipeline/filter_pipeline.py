from feature.sql_csv.core.data_pipeline.utils.ETL_dataframe_generate import ETL_dataframe_generate
from feature.sql_csv.core.data_pipeline.utils.classify_restaurant_or_view import classify_restaurant_or_view
from feature.sql_csv.core.data_pipeline.utils.special_request import special_request

def filter_pipeline(
                        placeID_list: list, 
                        restaurant_view_classify: str = '',
                        special_request_list: list[dict] = [],
                      ) -> list: 
    '''
    篩選管線 :
        輸入一組 placeID_list 
        輸出一組 經過篩選的 placeID_list

    Args :
        placeID_list : ["PlaceID1", "PlaceID2", ..., "PlaceIDN"]
        restaurant_view_classify : 'restaurant'|'view'|''
        special_request_list: 特殊需求 list[dict]|[]
    return :
        placeID_list : ["PlaceID1", "PlaceID2", ..., "PlaceIDN"]
    '''
    ETL_dataframe = ETL_dataframe_generate()

    # 第一節 : 餐廳景點篩選
    if restaurant_view_classify in ['restaurant', 'view']:
        # 若有指定 trip 或 plan 則進行 餐廳景點篩選
        placeID_list = classify_restaurant_or_view(
                                        placeID_list=placeID_list,
                                        restaurant_view_classify=restaurant_view_classify,
                                        ETL_dataframe=ETL_dataframe,
                                        )
    else : print('不進行餐廳景點篩選')
    
    # 第二節 : 特殊需求篩選
    if len(special_request_list)> 0 : 
        # 若 special_request_list = [] 則不進行篩選
        placeID_list = special_request(
                        placeID_list=placeID_list,
                        special_request_list=special_request_list,
                        ETL_dataframe=ETL_dataframe,
                    )
    else : print('不進行特殊篩選')

    return placeID_list


if __name__ == '__main__':
    placeID_list = [
                'ChIJqelWmSGnQjQR0oQv0a6ZJ8o',    # 康小玲      ['外帶外送', '其他支付']
                'ChIJI-NIexYdaDQRfldAuHBbwmY',    # 無名涼麵    ['現金']
                'ChIJ28UWAQAdaDQRBDGBOwEMJIY',    # 冰品店      ['外帶外送', '內用座位']
                'ChIJHRHjiIOuQjQRwvkYlwIEcTQ',    # SK-II       ['無障礙', '其他支付']
                ]
    placeID_list = filter_pipeline(
        placeID_list=placeID_list,
        restaurant_view_classify='restaurant',
        special_request_list= [{'現金': True}],
        # special_request_list=[],
        # restaurant_view_classify='',
    )

    print(placeID_list)