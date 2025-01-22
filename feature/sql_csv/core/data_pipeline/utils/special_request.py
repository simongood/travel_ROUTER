def special_request(    
                    placeID_list, 
                    special_request_list: list[dict],
                    ETL_dataframe, 
                    ): 
    '''
    根據 request_list 篩選符合條件的選項
    只要內含全部 request_list true 的選項的 placeID , 都篩進最後 list
    
    ```
    Args:
        placeID_list (list): 包含 placeID 的列表 ['placeID1', 'placeID2', ....]
        special_request_list (list[dict]): 篩選要求
        ETL_dataframe : ETL_df 表 
    
    Returns:
        list: 篩選後的 placeID 列表。
    ```
    '''

    filtered_series = ETL_dataframe['device_cat'].loc[placeID_list]

    # 篩出 true 的選項 :    ['其他支付': true, '無障礙': true] -> ['其他支付', '無障礙']
    request_true_list = []
    for key, value in special_request_list[0].items():
        if value == True:
            request_true_list.append(key)

    # 篩出遮罩 
    filtered_mask = (filtered_series
                     .apply(lambda x: all(item in x for item in request_true_list))
                    )
    
    # 取得符合條件的 place_id
    filtered_list = filtered_series.index[filtered_mask].tolist()


    return filtered_list

'''
filtered_mask 內部結構 : 
ChIJqelWmSGnQjQR0oQv0a6ZJ8o    False
ChIJI-NIexYdaDQRfldAuHBbwmY    False
ChIJ28UWAQAdaDQRBDGBOwEMJIY    False
ChIJHRHjiIOuQjQRwvkYlwIEcTQ     True
'''



if __name__ == '__main__':
    from feature.sql_csv.core.data_pipeline.utils.ETL_dataframe_generate import ETL_dataframe_generate
    placeID_list = [
                    'ChIJqelWmSGnQjQR0oQv0a6ZJ8o',    # 康小玲      ['外帶外送', '其他支付']
                    'ChIJI-NIexYdaDQRfldAuHBbwmY',    # 無名涼麵    ['現金']
                    'ChIJ28UWAQAdaDQRBDGBOwEMJIY',    # 冰品店      ['外帶外送', '內用座位']
                    'ChIJHRHjiIOuQjQRwvkYlwIEcTQ',    # SK-II       ['無障礙', '其他支付']
                    ]
    ETL_dataframe = ETL_dataframe_generate()

    special_request_list = [{'內用座位': False, '洗手間': False, '適合兒童': False, '適合團體': False, '現金': False,
          '其他支付': True, '收費停車': False, '免費停車': False, 'wi-fi': False, '無障礙': False}]
    
    # 預期篩出 SK-II
    placeID_list = special_request(
                        placeID_list=placeID_list,
                        special_request_list=special_request_list,
                        ETL_dataframe=ETL_dataframe,
                    )
    
    print(placeID_list)