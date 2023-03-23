import xlrd
import sqlite3
import os

DB_PATH_A = 'database/data_a.sqlite3'
DB_PATH_B = 'database/data_b.sqlite3'
TABLE_NAME_A = 'planthopper'
TABLE_NAME_B = 'butterfly'
FIELD_COUNT = 17


def create_db(db_path, table_name):
    ''' 파일 있으면 삭제 후에 생성 '''
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Date는 날짜 타입. 문자열로 넣고 함수를 이용해서 가져온다. (형식 YYYY-MM-DD)
    # date 또는 strftime 함수를 사용한다.

    # TEXT : 문자열, 날짜
    # REAL : 실수
    fields = '''Species TEXT, 
    Strain TEXT, 
    Site TEXT, 
    Host TEXT, 
    Date REAL,
    Insecticide_Origin TEXT, 
    Insecticide_Product TEXT, 
    Recommanded_Concentration REAL,
    Method TEXT, 
    Amount REAL, 
    Observation_Time REAL, 
    LC_or_LD50 REAL, 
    Single_Dose_Mortality REAL, 
    Unit_Definition TEXT, 
    Resistance_Ratio REAL,
    Reference REAL,
    UserName TEXT'''

    query = 'CREATE TABLE {} ({})'.format(table_name, fields)
    cursor.execute(query)

    conn.commit()
    conn.close()


def insert_all(rows, db_path, table_name, userName):
    ''' 잘못된 데이터가 있으면 False 반환.
    중간에 잘못되면 전체 데이터를 넣지 않는다. '''

    # 1차에서 만들었는데, 데이터 형식이 바뀌어서 사용 안함.
    # YYYY-MM-DD
    # def make_datetext(year, month, day):
    #     try:
    #         y4 = int(year)
    #         m2 = int(month)
    #         d2 = int(day)
    #     except ValueError:
    #         return None
    #
    #     if y4 <= 1900 or y4 >= 2030:
    #         return None
    #
    #     if m2 < 1 or m2 > 12:
    #         return None
    #
    #     if d2 < 1 or d2 > 31:
    #         return None
    #
    #     if m2 == 2 and d2 > 29:
    #         return None
    #
    #     if (m2 == 4 or m2 == 6 or m2 == 9 or m2 == 11) and m2 == 31:
    #         return None
    #
    #     return '{}-{:02}-{:02}'.format(y4, m2, d2)

    # print(make_datetext(2017, 12, 12))
    # print(make_datetext(2017, 12, 32))
    # print(make_datetext(2017, 0, 0))
    # print(make_datetext(2017, 5, 5))
    # print(make_datetext(2017, 2, 30))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 필드 갯수 16+1=17개(사용자명 까지). 따옴표는 문자열, 없으면 실수.                           Host                     Method      LC_or_LD50
    base = 'INSERT INTO ' + table_name + ' VALUES ("{}", "{}", "{}", "{}", {}, "{}", "{}", {}, "{}", {}, {}, {}, {}, "{}", {}, {}, "{}")'

    for row in rows:
        # 필드 갯수가 일치하지 않으면 에러.
        if len(row) != FIELD_COUNT-1:
            print('필드 갯수 :', len(row))#UserName +1
            print(row)
            conn.close()
            print('[에러] 필드 갯수 불일치')
            return False

        # 어떤 예외라도 발생하면 에러.
        try:
            query = base.format(*row, userName)
            cursor.execute(query)
        except Exception as e:
            conn.close()
            print('[예외]', e)
            print('[데이터]', row)
            return False

    conn.commit()
    conn.close()
    return True


def fetch_all(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = 'SELECT * FROM ' + table_name
    rows = list(cursor.execute(query))

    conn.commit()
    conn.close()

    return rows


def show_db(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = 'SELECT * FROM ' + table_name
    for row in cursor.execute(query):
        print(row)

    conn.commit()
    conn.close()


def db_test(db_path, table_name):
    ''' 삭제 후에 데이터 2개 추가하고 결과 출력 '''
    create_db(db_path, table_name)
    rows = [['흰가루병', 'SL_2', '서울 관악구 낙성대동 207-26', '오미자', 42846.0, 'abamectin', '올스타', 0.007, '스프레이법', 10.0, 48.0, 10.0,
             0.1, 'ug-cm', 1.0, 1.0],
            ['흰가루병', 'SL-3', '서울관악구 관악로1', '오미자', 42907.0, 'Abamectin', '올스타', 0.007, '스프레이법', 5.0, 48.0, 10.0, 0.002,
             'mg-cm', 2.0, 1.0]]
    insert_all(rows, db_path, table_name)
    print('insert : 2개 추가')
    print()

    show_db(db_path, table_name)
    print('모든 데이터 출력 완료')


if __name__ == '__main__':
    import sys

    # 소문자 변환. [1:]은 'db_helper.py' 건너뛰기.
    argv = [s.lower() for s in sys.argv[1:]]

    if 'reset' not in argv and 'show' not in argv and 'test' not in argv:
        print('[사용법]')
        print('옵션을 1개 또는 여러 개 나열.')
        print('v2 : python  {} reset show test'.format(__file__))
        print('v3 : python3 {} reset show test'.format(__file__))
        print()
        print('reset : db 파일을 삭제하고 다시 만들었습니다. (데이터 초기화)')
        print(' show : db에 포함된 모든 데이터를 표시합니다.')
        print(' test : db 삭제 후에 데이터 2개를 추가하고 추가한 내용을 표시합니다.')
        print()
        sys.exit(2)

    if 'reset' in argv:
        print('[알림] db 파일을 삭제하고 다시 만들었습니다. (데이터 초기화)')
        create_db(DB_PATH_A, TABLE_NAME_A)
        create_db(DB_PATH_B, TABLE_NAME_B)

    if 'show' in argv:
        print('[알림] db에 포함된 모든 데이터를 표시합니다.')
        show_db(DB_PATH_A, TABLE_NAME_A)
        show_db(DB_PATH_B, TABLE_NAME_B)

    if 'test' in argv:
        print('[알림] db 삭제 후에 데이터 2개를 추가하고 추가한 내용을 표시합니다.')
        db_test(DB_PATH_A, TABLE_NAME_A)
        db_test(DB_PATH_B, TABLE_NAME_B)
