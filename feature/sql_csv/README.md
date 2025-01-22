# sql_csv.py 用法
points = pandas_search(  
                    system: 'plan'|'trip',
                    system_input: 向量搜索端 input , 
                    special_request_list: [],   //  指定 [] 的化判定不篩選特殊要求
                ) : 
> 1. 指定 系統
> 2. 進入 plan_system | trip_system
>       * 使用 data_pipeline/filter_pipeline 篩選
>       * 使用 point_maker/point_make 形成單個 point 最後輸出 points
> 3. return points


---

# core/ 
- data_pipeline/ 
    - 主要控制 placeID_list 的篩選
- point_maker/
    - 主要控制 將 placeID 轉成 point 格式
- plan_system.py, trip_system.py
    - 主要控制 
        data_pipeline 篩選
        point_maker 轉換成 point
        收集 point 形成最終 point 格式