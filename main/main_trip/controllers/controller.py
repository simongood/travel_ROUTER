import os
from dotenv import load_dotenv
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor

from feature.llm.LLM import LLM_Manager
from feature.retrieval.parallel_search import ParallelSearchManager
from feature.retrieval.qdrant_search import qdrant_search
from feature.sql import csv_read
from feature.trip import TripPlanningSystem


class TripController:
    """行程規劃系統控制器"""

    def __init__(self, config: dict):
        """
        初始化控制器

        輸入:
            config: dict，包含所需的所有設定
                - jina_url: Jina AI 的 URL
                - jina_headers_Authorization: Jina 認證金鑰
                - qdrant_url: Qdrant 資料庫 URL
                - qdrant_api_key: Qdrant API 金鑰
                - ChatGPT_api_key: ChatGPT API 金鑰
        """
        self.config = config
        self.trip_planner = TripPlanningSystem()

    def process_message(self, input_text: str) -> str:
        """
        處理輸入訊息並返回結果

        輸入:
            input_text (str): 使用者輸入文字，例如"想去台北文青的地方"

        輸出:
            str: 規劃好的行程或錯誤訊息
        """
        try:
            # 1. LLM意圖分析
            period_describe, unique_requirement, base_requirement = self._analyze_intent(
                input_text
            )

            # 2. 向量檢索
            placeIDs = self._vector_retrieval(period_describe)

            # 3. 取得景點詳細資料
            location_details = self._get_places(placeIDs, unique_requirement)

            # 4. 規劃行程
            return self._plan_trip(location_details, base_requirement)

        except Exception as e:
            return f"抱歉，系統發生錯誤: {str(e)}"

    def _analyze_intent(self, text: str) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        分析使用者意圖

        輸入:
            text (str): 使用者輸入

        輸出:
            Tuple[List[Dict], List[Dict], List[Dict[str, Union[int, str, None]]]]:
                - List[Dict]: 旅遊各時段形容詞 (對應圖中的 'a')
                - List[Dict]: 特殊需求 (對應圖中的 'b')
                - List[Dict[str, Union[int, str, None]]]: 客戶基本要求 (對應圖中的 'c')
        """
        LLM_obj = LLM_Manager(self.config['ChatGPT_api_key'])

        return LLM_obj.Thinking_fun(text)

    def _vector_retrieval(self, period_describe: List[Dict]) -> Dict:
        """
        平行處理多個時段的向量搜尋

        輸入:
            period_describe: List[Dict] 
                各時段的描述，例如：
                [
                    {'上午': '文青咖啡廳描述'},
                    {'中餐': '餐廳描述'}
                ]

        輸出:
            Dict: 各時段對應的景點ID
                {
                    '上午': ['id1', 'id2', ...],
                    '中餐': ['id3', 'id4', ...]
                }
        """
        try:
            # 建立 qdrant_search 實例
            qdrant_obj = qdrant_search(
                collection_name='view_restaurant_test',
                config=self.config,
                score_threshold=0.5,
                limit=30
            )
            # period_describe = [
            #     {'上午': '喜歡在文青咖啡廳裡享受幽靜且美麗的裝潢'},
            #     {'中餐': '好吃很辣便宜加飯附湯環境整潔很多人可以停車'},
            #     {'下午': '充滿歷史感的日式建築'},
            #     {'晚餐': '適合多人聚餐的餐廳'},
            #     {'晚上': '可以看夜景的地方'}
            # ]

            # 使用 ThreadPoolExecutor 進行平行處理
            results = {}
            with ThreadPoolExecutor() as executor:
                future_to_query = {
                    executor.submit(qdrant_obj.trip_search, query): query
                    for query in period_describe
                }

                for future in future_to_query:
                    try:
                        result = future.result()
                        results.update(result)
                    except Exception as e:
                        print(f"搜尋過程發生錯誤: {str(e)}")
                        continue

            return results

        except Exception as e:
            raise Exception(f"向量搜尋發生錯誤: {str(e)}")

    def _get_places(self, placeIDs: Dict, unique_requirement: List[Dict]) -> List[Dict]:
        """
        從資料庫取得景點詳細資料

        輸入:
            placeIDs: Dict 
                各時段的景點ID，格式如：
                {
                    '上午': ['id1', 'id2'],
                    '中餐': ['id3', 'id4']
                }
            unique_requirement: List[Dict]
                使用者的特殊需求，例如：
                [{'無障礙': True, '適合兒童': True}]

        輸出:
            List[Dict]: 景點的詳細資料列表
        """
        unique_requirement = [{'無障礙': False}]

        return csv_read.pandas_search(
            condition_data=placeIDs,
            detail_info=unique_requirement
        )

    def _plan_trip(self, location_details: List[Dict], base_requirement: List[Dict]) -> str:
        """
        根據景點資料和基本需求規劃行程

        輸入:
            location_details: List[Dict] 
                景點詳細資料列表
            base_requirement: List[Dict]
                基本需求，如時間、交通方式等

        輸出:
            str: 格式化的行程規劃結果
        """
        # 使用已初始化的 trip_planner
        return self.trip_planner.plan_trip(location_details, base_requirement)


def init_config():
    """初始化設定

    載入環境變數並整理成設定字典

    回傳:
        dict: 包含所有 API 設定的字典，包括:
            - jina_url: Jina API 端點
            - jina_headers_Authorization: Jina 認證金鑰
            - qdrant_url: Qdrant 伺服器位址
            - qdrant_api_key: Qdrant 存取金鑰
            - ChatGPT_api_key: OpenAI API 金鑰
    """
    # 直接載入環境變數，這樣在容器中也能正常運作
    load_dotenv()

    config = {
        'jina_url': os.getenv('jina_url'),
        'jina_headers_Authorization': os.getenv('jina_headers_Authorization'),
        'qdrant_url': os.getenv('qdrant_url'),
        'qdrant_api_key': os.getenv('qdrant_api_key'),
        'ChatGPT_api_key': os.getenv('ChatGPT_api_key')
    }

    # 驗證所有設定都存在
    missing = [key for key, value in config.items() if not value]
    if missing:
        raise ValueError(f"缺少必要的API設定: {', '.join(missing)}")

    return config


if __name__ == "__main__":
    try:
        config = init_config()
        controller_instance = TripController(config)

        test_input = "想去台北文青的地方，吃午餐要便宜又好吃，下午想去逛有特色的景點，晚餐要可以跟朋友聚餐"
        result = controller_instance.process_message(test_input)
        controller_instance.trip_planner.print_itinerary(
            result,
        )

    except Exception as e:
        print("DEBUG: ", str(e))  # 完整錯誤訊息