
from feature.sql_csv.core.plan_system import plan_system
from feature.sql_csv.core.trip_system import trip_system

def pandas_search(  
                    system: str,
                    system_input: list|dict, 
                    special_request_list: list[dict] = [],
                ) : 
    '''
    ```
    Args :
        input : 情境搜索端的輸入 | 旅遊搜索端的輸入
        special_request_list : 特殊要求 list 
        system : "trip"|"plan"

        # ps : 若不進行 特殊要求 篩選則給 [] 值

    return :
        trip 端 : trip 端的 points
        plan 端 : plan 端的 points
    ```
    ---

    >> plan 情境搜索端 : 不進行餐廳景點篩選
    '''

    #　[trip / plan] system 分流
    if system == 'trip':
        points = trip_system(
            system_input=system_input,
            special_request_list=special_request_list
        )
    elif system == 'plan':
        points = plan_system(
                            system_input=system_input,
                            special_request_list=special_request_list,
                        )
    return points








if __name__ == "__main__":
    from pprint import pprint

    # ---------------------------------------------------------------------------
    # 旅遊推薦端
    print('\n\n-----------旅遊推薦------------------------------------------')
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
    trip_points = pandas_search(  
                    system= 'trip',
                    system_input= trip_system_input, 
                    special_request_list= [],           # 沒有特殊篩選，只有餐聽景點分流  
                )
    
    pprint(trip_points , sort_dicts= False)

    # ---------------------------------------------------------------------------
    # 情境搜索端
    print('\n\n-----------情境搜索------------------------------------------')
    plan_system_input = [{
                            'ChIJqelWmSGnQjQR0oQv0a6ZJ8o':{"分數": 0.5} ,  # 康小玲      ['外帶外送', '其他支付']
                            'ChIJI-NIexYdaDQRfldAuHBbwmY':{"分數": 0.6} ,  # 無名涼麵    ['現金']
                            'ChIJ28UWAQAdaDQRBDGBOwEMJIY':{"分數": 0.7} ,  # 冰品店      ['外帶外送', '內用座位']
                            'ChIJHRHjiIOuQjQRwvkYlwIEcTQ':{"分數": 0.8} ,  # SK-II       ['無障礙', '其他支付']
                        }]
    
    plan_points = pandas_search(  
                    system= 'plan',
                    system_input= plan_system_input, 
                    special_request_list= [{ '其他支付': True,}] ,
                )

    pprint(plan_points , sort_dicts= False)