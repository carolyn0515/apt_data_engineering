select sggCd as sgg_cd
     , case when sggCd = '11110' then '종로구'
            when sggCd = '11140' then '중구'
            when sggCd = '11170' then '용산구'
            when sggCd = '11200' then '성동구'
            when sggCd = '11215' then '광진구'
            when sggCd = '11230' then '동대문구'
            when sggCd = '11260' then '중랑구'
            when sggCd = '11290' then '성북구'
            when sggCd = '11305' then '강북구'
            when sggCd = '11320' then '도봉구'
            when sggCd = '11350' then '노원구'
            when sggCd = '11380' then '은평구'
            when sggCd = '11410' then '서대문구'
            when sggCd = '11440' then '마포구'
            when sggCd = '11470' then '양천구'
            when sggCd = '11500' then '강서구'
            when sggCd = '11530' then '구로구'
            when sggCd = '11545' then '금천구'
            when sggCd = '11560' then '영등포구'
            when sggCd = '11590' then '동작구'
            when sggCd = '11620' then '관악구'
            when sggCd = '11650' then '서초구'
            when sggCd = '11680' then '강남구'
            when sggCd = '11710' then '송파구'
            when sggCd = '11740' then '강동구'
            else ''
       end as sgg_nm
     , umdNm as umd_nm
     , aptNm as apt_nm
     , jibun
     , cast(excluUseAr as float) as exclu_use_ar
     , cast(dealYear as int) as deal_year
     , cast(dealMonth as int) as deal_month
     , cast(dealDay as int) as deal_day
     , cast(replace(dealAmount, ',', '') as int) as deal_amount
     , cast(floor as int) as floor
     , cast(buildYear as int) as build_year
     , case when cdealType == ' ' then null
            else cdealType
       end as cdeal_type
     , case when cdealDay == ' ' then null
            else cdealDay
       end as cdeal_day
     , case when dealingGbn == ' ' then null
            else dealingGbn
       end as dealing_gbn
     , case when estateAgentSggNm == ' ' then null
            else estateAgentSggNm
       end as estate_agent_sgg_nm
     , case when rgstDate == ' ' then null
            else rgstDate
       end as rgst_date
     , case when aptDong == ' ' then null
            else aptDong
       end as apt_dong
     , case when slerGbn == ' ' then null
            else slerGbn
       end as sler_gbn
     , case when buyerGbn == ' ' then null
            else buyerGbn
       end as buyer_gbn
     , case when landLeaseholdGbn == ' ' then null
            else landLeaseholdGbn
       end as land_leasehold_gbn
     , deal_ymd
     , lawd_cd
  from apt_trade_raw
