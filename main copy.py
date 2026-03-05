# api 주소
# request 
# xml -> parsing
# json -> upload s3
def preprocessing_datas(root):
    list_temp = list()

    for item in root.iter("item"):
        dict_item = {
            "sggCd": item.find("sggCd").text,
            "umdNm": item.find("umdNm").text,
            "aptNm": item.find("aptNm").text,
            "jibun": item.find("jibun").text,
            "excluUseAr": item.find("excluUseAr").text,
            "dealYear": item.find("dealYear").text,
            "dealMonth": item.find("dealMonth").text,
            "dealDay": item.find("dealDay").text,
            "dealAmount": item.find("dealAmount").text,
            "floor": item.find("floor").text,
            "buildYear": item.find("buildYear").text,
            "cdealType": item.find("cdealType").text,
            "cdealDay": item.find("cdealDay").text,
            "dealingGbn": item.find("dealingGbn").text,
            "estateAgentSggNm": item.find("estateAgentSggNm").text,
            "rgstDate": item.find("rgstDate").text,
            "aptDong": item.find("aptDong").text,
            "slerGbn": item.find("slerGbn").text,
            "buyerGbn": item.find("buyerGbn").text,
            "landLeaseholdGbn": item.find("landLeaseholdGbn").text
        }
        list_temp.append(dict_item)

    return list_temp

def get_apt_trade_from_api(lawd_cd: str, deal_ymd: str, service_key: str):
    list_result = list()
    num_of_rows = 50
    page_no = 1

    import requests
    import xml.etree.ElementTree as ET

    while True:
        end_point_url = ("http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade?"
                         f"serviceKey={service_key}&LAWD_CD={lawd_cd}&DEAL_YMD={deal_ymd}"
                         f"&numOfRows={num_of_rows}&pageNo={page_no}")
        response = requests.get(end_point_url)
        total_count = ET.fromstring(response.text)

        list_result += preprocessing_datas(response)
        
        if len(list_result) >= total_count: break

        page_no += 1
    
    return list_result

def save_file(content, file_name, file_type):
    import jsonlines
    if file_type == "json":
        with jsonlines.open(file_name, "w") as f:
            f.write_all(content)
    
def upload_to_s3(file_name, bucket_name, object_name):
    from botocore.exceptions import NoCredentialsError
    import boto3
    
    s3_client = boto3.client("s3")

    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
    except NoCredentialsError:
        print("AWS 자격 증명 찾을 수 없음")
        
def main(): 

    # env에서 key 가져오기
    from dotenv import load_dotenv
    import os
    load_dotenv()
    service_key = os.getenv("SERVICE_KEY")
    
    # 지역별 데이터 가져오기 _ 202401
    list_lawd_cd = [
        "11110"  # 종로구
        , "11140"  # 중구
        , "11170"  # 용산구
        , "11200"  # 성동구
        , "11215"  # 광진구
        , "11230"  # 동대문구
        , "11260"  # 중랑구
        , "11290"  # 성북구
        , "11305"  # 강북구
        , "11320"  # 도봉구
        , "11350"  # 노원구
        , "11380"  # 은평구
        , "11410"  # 서대문구
        , "11440"  # 마포구
        , "11470"  # 양천구
        , "11500"  # 강서구
        , "11530"  # 구로구
        , "11545"  # 금천구
        , "11560"  # 영등포구
        , "11590"  # 동작구
        , "11620"  # 관악구
        , "11650"  # 서초구
        , "11680"  # 강남구
        , "11710"  # 송파구
        , "11740"  # 강동구
    ]

    file_type = "json"
    bucket_name = "metacode-realestate-test-0304"

    for deal_ymd in ["202401"]:
        for lawd_cd in list_lawd_cd:
            file_name = f"{deal_ymd}_{lawd_cd}_result.json"
            object_name = f"apt-trade-raw/deal_ymd={deal_ymd}/lawd_cd={lawd_cd}/result.json"

            # API로 데이터 가져오기
            trade_result = get_apt_trade_from_api(lawd_cd, deal_ymd, service_key)
            save_file(trade_result, file_name, file_type)
            upload_to_s3(file_name, bucket_name, object_name)

if __name__ == "__main__":
    main()