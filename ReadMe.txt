
# db 명령어
# db_helper.py 파일은 명령어로 동작할 수 있도록 작성했습니다.
# 터미널에서 python3 db_helper.py 라고 입력하면 도움말을 볼 수 있습니다.



# 1차 데이터 형식
# ['국가',     '채집 시기', '', '',      '지역(도명)', '지역(시/읍/면명)', '계통명',  '주소',    '좌표x',          '좌표y',
# ['Country', 'Year', 'Month', 'Day', 'Local 01', 'Local 02',    'Strain', 'Address', 'Coordinate_X', 'Coordinate_Y',
# '기주식물', '해충종명',  '령기',    '살충제 계열',          '계열번호',       '살충제 원제이름', '살충제 한글명',                '제품 추천농도',
# 'Host',  'Species', 'Stages', 'Insecticide class', '2016.04월 기준', 'Insecticide', 'Insecticide common name', 'Recommanded concentration (ppm)',
# '방법',     '약량',   '사충율 관찰 시간',           '반수치사약량', '단위정의',           '단일농도사충율(%)',         '단위',             '참고문헌',     '출판년도',           '저항성비']
# 'Method', 'Amount', 'Observation time (hr)', 'LC or LD50', 'Unit definition', 'Single dose mortality', 'Unit definition', 'Reference', 'Publication year', 'Resistance ratio']

# 2차 데이터 형식(11월 11일)
# Species                       생물종명(흰가루병)
# Strain                        계통명(SL_2)
# Site                          채집장소(서울 관악구 낙성대동 207-26)
# Host                          기주식물(오미자)
# Date                          채집 시기(년-월-일)(42846.0)
# Insecticide_Origin            살충제 원제이름(abamectin)
# Insecticide_Product           살충제 제품명(올스타)
# Recommanded_Concentration     제품 추천농도(ppm)(0.007)
# Method                        처리 방법(스프레이법)
# Amount                        약량(10.0)
# Observation_Time              사충율 관찰 시간(hr)(48.0)
# LC_or_LD50                    반수치사약량(10.0)
# Single_Dose_Mortality         단일농도사충율(%)(0.1)
# Unit_Definition               단위(ug-cm)
# Resistance_Ratio              저항성비(1.0)
# Reference                     참고문헌(1.0)
