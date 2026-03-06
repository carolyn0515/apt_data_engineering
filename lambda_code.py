import json
import urllib.parse
import boto3

s3 = boto3.client("s3")
dict_sgg_nm = {
    "11110": "종로구",
    "11140": "중구",
    "11170": "용산구",
    "11200": "성동구",
    "11215": "광진구",
    "11230": "동대문구",
    "11260": "중랑구",
    "11290": "성북구",
    "11305": "강북구",
    "11320": "도봉구",
    "11350": "노원구",
    "11380": "은평구",
    "11410": "서대문구",
    "11440": "마포구",
    "11470": "양천구",
    "11500": "강서구",
    "11530": "구로구",
    "11545": "금천구",
    "11560": "영등포구",
    "11590": "동작구",
    "11620": "관악구",
    "11650": "서초구",
    "11680": "강남구",
    "11710": "송파구",
    "11740": "강동구"
}

def lambda_handler(event, context):
    # TODO implement
    print(f"EVENT: {event}")
    print(f"CONTEXT: {context}")

    # 이벤트가 들어오는 S3 정보를 가져오는 부분
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")

    print(f"BUCKET: {bucket}")
    print(f"KEY: {key}")

    # S3 정보를 이용해서 실제 들어온 데이터를 가져오고 가공하는 부분
    try:
        response = s3.get_object(Bucket=bucket, Key=key)

        raw_data = response["Body"].read().decode("utf-8")

        list_result = []
        for line in raw_data.strip().split("\n"):
            dict_temp = dict()
            if line.strip():
                line_json = json.loads(line)
                
                dict_temp["sgg_cd"] = line_json["sggCd"]
                dict_temp["sgg_nm"] = dict_sgg_nm.get(line_json["sggCd"], "") 
                dict_temp["umd_nm"] = line_json["umdNm"]
                dict_temp["apt_nm"] = line_json["aptNm"]
                dict_temp["jibun"] = line_json["jibun"]
                dict_temp["exclu_use_ar"] = float(line_json["excluUseAr"])
                dict_temp["deal_year"] = int(line_json["dealYear"])
                dict_temp["deal_month"] = int(line_json["dealMonth"])
                dict_temp["deal_day"] = int(line_json["dealDay"])
                dict_temp["deal_amount"] = int(line_json["dealAmount"].replace(",", ""))
                dict_temp["floor"] = int(line_json["floor"])
                dict_temp["build_year"] = int(line_json["buildYear"])
                dict_temp["cdeal_type"] = None if line_json["cdealType"] == " " else line_json["cdealType"]
                dict_temp["cdeal_day"] = None if line_json["cdealDay"] == " " else line_json["cdealDay"]
                dict_temp["dealing_gbn"] = None if line_json["dealingGbn"] == " " else line_json["dealingGbn"]
                dict_temp["estate_agent_sgg_nm"] = None if line_json["estateAgentSggNm"] == " " else line_json[
                    "estateAgentSggNm"]
                dict_temp["rgst_date"] = None if line_json["rgstDate"] == " " else line_json["rgstDate"]
                dict_temp["apt_dong"] = None if line_json["aptDong"] == " " else line_json["aptDong"]
                dict_temp["sler_gbn"] = None if line_json["slerGbn"] == " " else line_json["slerGbn"]
                dict_temp["buyer_gbn"] = None if line_json["buyerGbn"] == " " else line_json["buyerGbn"]
                dict_temp["land_leasehold_gbn"] = None if line_json["landLeaseholdGbn"] == " " else line_json[
                    "landLeaseholdGbn"]
                list_result.append(dict_temp)

        # 가공한 데이터를 다시 S3에 저장
        processed_data = "\n".join(json.dumps(result, ensure_ascii=False) for result in list_result)
        s3.put_object(Bucket=bucket, Key=f"apt-trade-processed-lambda/{key}", Body=processed_data)

    except Exception as e:
        print(f"ERROR: {e}")

    return {
        "statusCode": 200,
        "body": json.dumps("Hello from Lambda!")
    }
