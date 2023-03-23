from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.utils import secure_filename
import csv
import os
import xlrd
import db_helper        # db 처리 파일

UPLOAD_FOLDER = 'database'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = ['xls', 'xlsx']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.xls_filename = 'data.xlsx'          # 확장자가 다를 경우 안 열릴 수 있다.

df = 'background-color:#D8D8D8;border: 1px solid #ccc;border-radius:0.5em;'

# ---------------------- < 애멸구 > -------------------------------------
@app.route('/')
def drugs_info_a(first='drugs_info_a', second='drugs_info_b', setting=df):
    return render_template('drugs_info_a.html', first=first, second=second, setting=setting)

@app.route('/greeting_a')
def greeting_a(first='greeting_a', second='greeting_b', setting=df):
    return render_template('greeting_a.html', first=first, second=second, setting=setting)

@app.route('/life_a')
def life_a(first='life_a', second='life_b', setting=df):
    return render_template('life_a.html', first=first, second=second, setting=setting)

@app.route('/resistance_info_a')
def resistance_info_a(first='resistance_info_a', second='resistance_info_b', setting=df):
    f = open('static/resistance_info_a.csv', 'r', encoding='utf-8')
    rows = list(csv.reader(f))
    f.close()

    return render_template('resistance_info_a.html', rows=rows, first=first, second=second, setting=setting)

@app.route('/view_a')
def view_a(first='view_a', second='view_b', setting=df):
    header = ['생물종명', '계통명', '채집장소', '기주식물', '채집 시기',
              '살충제 원제이름', '살충제 제품명', '제품 추천농도(ppm)', '처리 방법',
              '약량', '사충율 관찰시간(hr)', '반수치사약량', '단일농도 사충율(%)',
              '단위', '저항성비', '참고문헌', '등록자']
    rows = [header]
    rows += db_helper.fetch_all(db_helper.DB_PATH_A, db_helper.TABLE_NAME_A)
    return render_template('view_a.html', rows=enumerate(rows), first=first, second=second, setting=setting)

@app.route('/upload_a')
def upload_a(first='upload_a', second='upload_b', setting=df):
    return render_template('upload_a.html', first=first, second=second, setting=setting)

@app.route('/reference_a')
def reference_a(first='reference_a', second='reference_b', setting=df):
    return render_template('reference_a.html', first=first, second=second, setting=setting)

# --------------------- < 배추좀나방 > -----------------------------------
@app.route('/drugs_info_b')
def drugs_info_b(first='drugs_info_a', second='drugs_info_b', setting=df):
    return render_template('drugs_info_b.html', first=first, second=second, setting=setting)

@app.route('/greeting_b')
def greeting_b(first='greeting_a', second='greeting_b', setting=df):
    return render_template('greeting_b.html', first=first, second=second, setting=setting)

@app.route('/life_b')
def life_b(first='life_a', second='life_b', setting=df):
    return render_template('life_b.html', first=first, second=second, setting=setting)

@app.route('/resistance_info_b')
def resistance_info_b(first='resistance_info_a', second='resistance_info_b', setting=df):
    f = open('static/resistance_info_b.csv', 'r', encoding='utf-8')
    rows = list(csv.reader(f))
    f.close()

    return render_template('resistance_info_b.html', rows=rows, first=first, second=second, setting=setting)

@app.route('/view_b')
def view_b(first='view_a', second='view_b', setting=df):
    header = ['생물종명', '계통명', '채집장소', '기주식물', '채집 시기',
              '살충제 원제이름', '살충제 제품명', '제품 추천농도(ppm)', '처리 방법',
              '약량', '사충율 관찰시간(hr)', '반수치사약량', '단일농도 사충율(%)',
              '단위', '저항성비', '참고문헌', '등록자']
    rows = [header]
    rows += db_helper.fetch_all(db_helper.DB_PATH_B, db_helper.TABLE_NAME_B)
    return render_template('view_b.html', rows=enumerate(rows), first=first, second=second, setting=setting)

@app.route('/upload_b')
def upload_b(first='upload_a', second='upload_b', setting=df):
    return render_template('upload_b.html', first=first, second=second, setting=setting)

@app.route('/reference_b')
def reference_b(first='reference_a', second='reference_b', setting=df):
    return render_template('reference_b.html', first=first, second=second, setting=setting)

#--------------------------------------------------
@app.route('/login')
def login(first='greeting_a', second='greeting_b', setting=df):
    return render_template('login.html', first=first, second=second, setting=setting)

#--------------------------------------------------
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/upload_file', methods=['GET', 'POST'])
@app.route('/upload_file_a', methods=['POST'])
def upload_file_a():
    if request.method != 'POST':
        # flash는 이동 페이지에 데이터를 전달하는 가장 쉬운 방법. html 페이지에 수신 코드 있어야 함.
        flash('지원하지 않는 프로토콜 입니다. [{}]'.format(request.method))
        return redirect(url_for('upload_a'))

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('수신 내용에 file 부분이 없습니다.')
        return redirect(url_for('upload_a'))

    file = request.files['file']

    # if user does not select file, browser also
    # submit a empty part without filename
    if not file.filename:
        flash('파일을 선택하지 않았습니다.')
        return redirect(url_for('upload_a'))

    if not allowed_file(file.filename):
        # 빈 문자열을 반환하면 현재 주소 페이지로 남아 있는다.
        # ALLOWED_EXTENSIONS이 리스트라서 []는 자동으로 표시된다.
        flash('엑셀 파일만 업로드할 수 있습니다. {}'.format(ALLOWED_EXTENSIONS))
        return redirect(url_for('upload_a'))

    if not file:
        # 빈 문자열을 반환하면 현재 주소 페이지로 남아 있는다.
        flash('다시 시도해 주세요.')
        return redirect(url_for('upload_a'))

    # 파일로 저장한다면, 아래 코드 사용
    # secure_filename 함수는 파일 이름에서 안전한 부분만 반환.
    filename, extension = secure_filename(file.filename).split('.')# 파일 이름
    userName = request.form['userName']      # 사용자 이름

    # 확장자 읽기
    # extension = os.path.splitext(file.filename)[1]

    # 해킹 위험 때문에 임의의 파일 이름 사용. 한 개 파일만 있으면 되기 때문에 가능.
    # "원래_파일이름 + 사용자_이름".xls
    save_name = filename + '_' + userName + '_a.' + extension

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], save_name))
    book = xlrd.open_workbook(os.path.join(UPLOAD_FOLDER, save_name))
    # print(file)
    # print(file.read())
    #
    # # 파일 내용 직접 출력. 파일이기 때문에 읽고 나면 포인터 이동. 다시 읽을 수 없다.
    contents = file.read()
    # print(contents.decode('cp-949'))      # utf-8, euc-kr, cp-949 모두 읽을 수 없다. 바이너리인듯..

    # 파일 저장 없이 메모리에서 직접 읽는다.
    # book = xlrd.open_workbook(file_contents=contents)
    # print(book)

    # 0번째 시트만 사용. 나머지는 무시
    sheets = book.sheets()
    sheet = sheets[1]
    # print(type(sheets))

    # 0번 데이터 건너뛰기. '생물종명'과 같은 헤더.
    rows, row_count = [], sheet.nrows-1
    for i in range(1, row_count+1):
        row = sheet.row_values(i)
        print(row)
        rows.append(row)

    # 실패하면 False 반환.
    if not db_helper.insert_all(rows, db_helper.DB_PATH_A, db_helper.TABLE_NAME_A, userName):
        flash('올바르지 않은 데이터가 있거나 필드 갯수가 맞지 않습니다.')
        return redirect(url_for('upload_a'))

    # 0번 시트만 출력
    # for row in range(sheet.nrows):
    #     print(sheet.row_values(row))

    # 모든 시트의 내용 출력
    # for i, sheet in enumerate(sheets):
    #     for r in range(sheet.nrows):
    #         # values = sheet.row_values(r)
    #         # print(values)
    #
    #         for c in range(sheet.ncols):
    #             v = sheet.cell_value(r, c)
    #             print(v, end='  ')
    #         print()

    # 아래 redirect는 주소창에 파일 이름을 명시한다. 그래서, 전달하면 안 된다.
    # redirect는 현재 함수의 주소이기 때문에 'upload_file'이므로 사용할 수 없다.
    # '/upload_file'은 파일 수신에서만 사용한다.
    # return redirect(url_for('upload_finished', filename=filename))

    flash('업로드한 파일을 저장했습니다. (데이터 갯수 : {}개)'.format(row_count))
    return redirect(url_for('upload_a'))

@app.route('/upload_file_b', methods=['POST'])
def upload_file_b():
    if request.method != 'POST':
        # flash는 이동 페이지에 데이터를 전달하는 가장 쉬운 방법. html 페이지에 수신 코드 있어야 함.
        flash('지원하지 않는 프로토콜 입니다. [{}]'.format(request.method))
        return redirect(url_for('upload_b'))

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('수신 내용에 file 부분이 없습니다.')
        return redirect(url_for('upload_b'))

    file = request.files['file']

    # if user does not select file, browser also
    # submit a empty part without filename
    if not file.filename:
        flash('파일을 선택하지 않았습니다.')
        return redirect(url_for('upload_b'))

    if not allowed_file(file.filename):
        # 빈 문자열을 반환하면 현재 주소 페이지로 남아 있는다.
        # ALLOWED_EXTENSIONS이 리스트라서 []는 자동으로 표시된다.
        flash('엑셀 파일만 업로드할 수 있습니다. {}'.format(ALLOWED_EXTENSIONS))
        return redirect(url_for('upload_b'))

    if not file:
        # 빈 문자열을 반환하면 현재 주소 페이지로 남아 있는다.
        flash('다시 시도해 주세요.')
        return redirect(url_for('upload_b'))

    # 파일로 저장한다면, 아래 코드 사용
    # secure_filename 함수는 파일 이름에서 안전한 부분만 반환.
    filename, extension = secure_filename(file.filename).split('.')# 파일 이름
    userName = request.form['userName']      # 사용자 이름

    # 확장자 읽기
    # extension = os.path.splitext(file.filename)[1]

    # 해킹 위험 때문에 임의의 파일 이름 사용. 한 개 파일만 있으면 되기 때문에 가능.
    # "원래_파일이름 + 사용자_이름".xls
    save_name = filename + '_' + userName + '_b.' + extension

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], save_name))
    book = xlrd.open_workbook(os.path.join(UPLOAD_FOLDER, save_name))
    # print(file)
    # print(file.read())
    #
    # # 파일 내용 직접 출력. 파일이기 때문에 읽고 나면 포인터 이동. 다시 읽을 수 없다.
    contents = file.read()
    # print(contents.decode('cp-949'))      # utf-8, euc-kr, cp-949 모두 읽을 수 없다. 바이너리인듯..

    # 파일 저장 없이 메모리에서 직접 읽는다.
    # book = xlrd.open_workbook(file_contents=contents)
    # print(book)

    # 0번째 시트만 사용. 나머지는 무시
    sheets = book.sheets()
    sheet = sheets[1]
    # print(type(sheets))

    # print(sheet)
    # print(sheet.nrows)
    # for i in range(1, sheet.nrows):
    #     print(sheet.row_values(i), '**')

    # 0번 데이터 건너뛰기. '생물종명'과 같은 헤더.
    rows, row_count = [], sheet.nrows-1
    for i in range(1, row_count+1):
        row = sheet.row_values(i)
        print(row)
        rows.append(row)

    # 실패하면 False 반환.
    if not db_helper.insert_all(rows, db_helper.DB_PATH_B, db_helper.TABLE_NAME_B, userName):
        flash('올바르지 않은 데이터가 있거나 필드 갯수가 맞지 않습니다.')
        return redirect(url_for('upload_b'))

    # 0번 시트만 출력
    # for row in range(sheet.nrows):
    #     print(sheet.row_values(row))

    # 모든 시트의 내용 출력
    # for i, sheet in enumerate(sheets):
    #     for r in range(sheet.nrows):
    #         # values = sheet.row_values(r)
    #         # print(values)
    #
    #         for c in range(sheet.ncols):
    #             v = sheet.cell_value(r, c)
    #             print(v, end='  ')
    #         print()

    # 아래 redirect는 주소창에 파일 이름을 명시한다. 그래서, 전달하면 안 된다.
    # redirect는 현재 함수의 주소이기 때문에 'upload_file'이므로 사용할 수 없다.
    # '/upload_file'은 파일 수신에서만 사용한다.
    # return redirect(url_for('upload_finished', filename=filename))

    flash('업로드한 파일을 저장했습니다. (데이터 갯수 : {}개)'.format(row_count))
    return redirect(url_for('upload_b'))



if __name__ == '__main__':
    app.run(debug=True)

















