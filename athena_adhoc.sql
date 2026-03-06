-- 총 건수
SELECT COUNT(*) AS cnt
  FROM test.apt_trade_processed
;

-- 년월별 거래량 추이
SELECT deal_ymd, COUNT(*) AS cnt
  FROM test.apt_trade_processed
 GROUP BY deal_ymd
 ORDER BY deal_ymd
;

-- 구별 거래량 추이
SELECT sgg_nm, COUNT(*) AS cnt
  FROM test.apt_trade_processed
 WHERE deal_year=2025
 GROUP BY sgg_nm
 ORDER BY cnt DESC
;

-- 구별 최소, 최대, 평균 거래 가격
SELECT sgg_nm
     , MIN(deal_amount) AS min_price
     , MAX(deal_amount) AS max_price
     , CEIL(AVG(deal_amount)) AS avg_price
  FROM apt_trade_processed
 WHERE deal_year=2025
 GROUP BY sgg_nm
 ORDER BY avg_price DESC
;

-- 특정 구의 평균 거래 가격 추이
SELECT deal_ymd
     , sgg_nm
     , CEIL(AVG(deal_amount)) AS avg_price
  FROM apt_trade_processed
 WHERE sgg_cd = '11710'
 GROUP BY deal_ymd
        , sgg_nm
 ORDER BY deal_ymd
;
