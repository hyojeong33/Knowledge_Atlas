import json
import time
import os
import requests
from datetime import datetime
# dotenv는 나중에 설치해야 할 수도 있습니다: pip install python-dotenv
# from dotenv import load_dotenv

def load_json(filepath):
    """JSON 파일을 읽어오는 헬퍼 함수"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filepath):
    """결과를 JSON 파일로 저장하는 헬퍼 함수"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def search_unsplash(query, api_key):
    """Unsplash API를 호출하여 이미지 데이터를 가져오는 함수"""
    # TODO: Unsplash API 엔드포인트에 맞게 요청을 보내고 결과를 파싱하는 로직 작성
    pass

def main():
    # 1. 환경 변수에서 API 키 불러오기 (보안)
    # load_dotenv()
    # UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
    
    # 2. 입력 데이터 불러오기
    # 주의: 실제 실행 위치에 따라 경로가 달라질 수 있으니 상대 경로를 잘 맞춰야 합니다.
    space_types_path = "../data/space_types.json"
    sources_path = "../data/image_sources.json"
    
    space_types = load_json(space_types_path)
    sources = load_json(sources_path)
    
    results = []
    
    # 3. 방 유형별로 순회하며 검색 수행 (Looping)
    for room_type, details in space_types.items():
        search_terms = details["search_terms"]
        print(f"[{room_type}] 검색을 시작합니다...")
        
        for term in search_terms:
            print(f"  - 검색어: {term}")
            
            # API 호출 (예: Unsplash)
            # data = search_unsplash(term, UNSPLASH_ACCESS_KEY)
            # if data is None or len(data) == 0:
            #     print(f"    경고: '{term}'에 대한 검색 결과가 없습니다.") # Error Logging
            # else:
            #     results.extend(data)
            
            # Rate Limiting: API 서버 과부하 방지
            time.sleep(1) 
            
    # 4. 결과 저장 (Output)
    save_json(results, "../data/search_results.json")
    print("검색 파이프라인 실행이 완료되었습니다!")

if __name__ == "__main__":
    main()