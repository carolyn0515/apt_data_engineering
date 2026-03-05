def processing_datas(root):
    """
        데이터 저장 형태
        [{거래 #1}, {거래 #2}]
    """
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

def get_apt_trade_from_api(service_key: str, lawd_cd: str, deal_ymd: str):
    import xml.etree.ElementTree as ET
    import requests

    list_result = list()
    num_of_rows = 50
    page_no = 1


    while True:
        end_point_url = ("http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade?"
                         f"serviceKey={service_key}&LAWD_CD={lawd_cd}&DEAL_YMD={deal_ymd}"
                         f"&numOfRows={num_of_rows}&pageNo={page_no}")

        response = requests.get(end_point_url)
        root = ET.fromstring(response.text)
        total_count = int(root.find("body/totalCount").text)

        # 2. 데이터 가공하기
        list_result += processing_datas(root)

        # Pagination
        if len(list_result) >= total_count:
            break

        page_no += 1

    return list_result


def save_file(content, file_name, file_type):
    """
        데이터 저장 형태
        { 거래 #1 정보 }
        { 거래 #2 정보 }
        ...
        { 거래 #n 정보 }
    """
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
        print("AWS 자격 증명을 찾을 수 없습니다.")

def main():
    from dotenv import load_dotenv
    import os

    # 변수 설정
    load_dotenv()

    service_key = os.getenv("SERVICE_KEY")
    file_type = "json"
    bucket_name = "metacode-realestate-test-0304"

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

    for deal_ymd in ["202401"]:
        for lawd_cd in list_lawd_cd:
            file_name = f"json_data/{deal_ymd}_{lawd_cd}_result.json"
            object_name = f"apt-trade-raw/deal_ymd={deal_ymd}/lawd_cd={lawd_cd}/result.json"

            # 1. API를 통해서 데이터 가져오기
            trade_result = get_apt_trade_from_api(service_key, lawd_cd, deal_ymd)

            # 3. 데이터를 파일로 저장하기
            save_file(trade_result, file_name, file_type)

            # 4. S3에 업로드하기
            upload_to_s3(file_name, bucket_name, object_name)

if __name__ == "__main__":
    main()
