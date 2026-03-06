-- COPY 명령어를 이용해서 진행해보기
-- S3의 파티션 키까지 가져올 수 없음.
-- 파티션 키까지 가져오려면 파티션 키를 포함하여 UNLOAD를 다시 하고 COPY해야 함.
CREATE TABLE metacode.real_estate_apt_trade (
    sgg_cd varchar(10),
    sgg_nm varchar(30),
    umd_nm varchar(20),
    apt_nm varchar(100),
    jibun varchar(10),
    exclu_use_ar float,
    deal_year int,
    deal_month int,
    deal_day int,
    deal_amount int,
    floor int,
    build_year int,
    cdeal_type varchar(10),
    cdeal_day varchar(10),
    dealing_gbn varchar(20),
    estate_agent_sgg_nm varchar(500),
    rgst_date varchar(50),
    apt_dong varchar(50),
    sler_gbn varchar(50),
    buyer_gbn varchar(50),
    land_leasehold_gbn varchar(5)
);

COPY metacode.real_estate_apt_trade
FROM 's3://'
IAM_ROLE ''
FORMAT AS PARQUET;


-- Spectrum을 이용하여 확인하기
-- Spectrum을 이용하면 파티션 키까지 모두 가져올 수 있음
CREATE EXTERNAL SCHEMA metacode_external
FROM DATA CATALOG
DATABASE 'test'
IAM_ROLE ''
CREATE EXTERNAL DATABASE IF NOT EXISTS;

-- Table 확인
SELECT *
  FROM metacode_external.apt_trade_processed
 LIMIT 10;

