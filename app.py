from flask import Flask, request, render_template, session, redirect, flash
import pymysql
app = Flask(__name__)

app.secret_key = 'alstjr!!98'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/', methods=['GET', 'POST'])
def landing():

    # 로그인 세션이 있으면
    if session.get('logged_in'):
        
        print('로그인 기록이 존재합니다.')
        flash('로그인 기록이 존재합니다.')
        
        # mail 얻어내기
        mail = session.get('user_mail')
        
        # mysql 연결
        db = pymysql.connect(database='sys', host="hufs-apply.cnlazyly7sdf.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", password="alstjr!!98")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        # name 얻어내기
        name = cursor.execute('SELECT user_name from user_info where user_mail=%s',(mail))
        name = cursor.fetchall()
        name = name[0]['user_name']

        # major 얻어내기
        major = cursor.execute('SELECT user_major from user_info WHERE user_mail=%s',(mail))
        major = cursor.fetchall()
        major = major[0]['user_major']

        # major_cnt
        major_cnt = cursor.execute('SELECT COUNT(*) from user_info where user_major=%s',(major))
        major_cnt = cursor.fetchall()
        major_cnt = major_cnt[0]['COUNT(*)']

        # rank 구하기
        ranking = cursor.execute('SELECT user_mail, rank() over (order by user_GPA desc) as ranking from user_info WHERE user_major=%s',(major))
        ranking = cursor.fetchall()
        
        # 같은 전공에 지원한 지원자 중에서
        for applier in ranking:
            # mail이 같은 회원을 찾으면
            if applier['user_mail'] == mail:
                # rank를 할당
                rank = applier['ranking']

        # mysql 닫기
        db.commit()
        db.close()

        # show.html로
        return render_template('Show.html', name = name, major=major,sum=major_cnt,rank=rank)
    
    # 로그인 세션이 없고, POST방식으로 접근했으면,
    elif request.method == 'POST':
    
        # mail
        mail = request.form['mail']
        # password
        password = request.form['password']
        
        # mysql 연결
        db = pymysql.connect(database='sys', host="hufs-apply.cnlazyly7sdf.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", password="alstjr!!98")
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # 아이디 존재 여부
        is_exists = cursor.execute('SELECT EXISTS (SELECT user_name from user_info WHERE user_mail=%s) as isChk',(mail));
        is_exists = cursor.fetchall()
        is_exists = is_exists[0]['isChk']

        # db 끄기
        db.commit()
        db.close()

        # 아이디가 존재하며,
        if is_exists:
            
            # mysql 연결
            db = pymysql.connect(database='sys', host="hufs-apply.cnlazyly7sdf.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", password="alstjr!!98")
            cursor = db.cursor(pymysql.cursors.DictCursor)
            
            # 진짜 비밀번호가,
            correct_password = cursor.execute('SELECT user_password from user_info where user_mail=%s',(mail));
            correct_password = cursor.fetchall()
            correct_password = correct_password[0]['user_password']
            
            # db 끄기
            db.commit()
            db.close()

            # 제출한 비밀번호와 같으면,
            if correct_password == password:
                
                # 로그인 성공
                print('로그인되었습니다.')
                # alert
                flash('로그인되었습니다.')

                # 로그인 세션 True로 변경
                session['logged_in'] = True
                # mail 세션에 기록하기
                session['user_mail'] = mail

                # mysql 연결
                db = pymysql.connect(database='sys', host="hufs-apply.cnlazyly7sdf.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", password="alstjr!!98")
                cursor = db.cursor(pymysql.cursors.DictCursor)
                
                # major 뽑기
                major = cursor.execute('SELECT user_major from user_info where user_mail=%s',(mail))
                major = cursor.fetchall()
                major = major[0]['user_major']

                # db 끄기
                db.commit()
                db.close()

                # 이전에 지원한 적이 없으면, (전공이 NULL 이면)
                if not major:
                    # mysql 연결
                    db = pymysql.connect(database='sys', host="hufs-apply.cnlazyly7sdf.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", password="alstjr!!98")
                    cursor = db.cursor(pymysql.cursors.DictCursor)

                    # name
                    name = cursor.execute('SELECT user_name from user_info where user_mail=%s',(mail))
                    name = cursor.fetchall()
                    name = name[0]['user_name']

                    # db 끄기
                    db.commit()
                    db.close()

                    # apply.html로 (name 들고)
                    return render_template('Apply.html',name=name)

                # 이전에 지원한 적이 있으면, (전공이 NULL이 아니면)
                # mysql 연결
                db = pymysql.connect(database='sys', host="hufs-apply.cnlazyly7sdf.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", password="alstjr!!98")
                cursor = db.cursor(pymysql.cursors.DictCursor)

                # major
                major = cursor.execute('SELECT user_major from user_info where user_mail=%s',(mail))
                major = cursor.fetchall()
                major = major[0]['user_major']

                # name
                name = cursor.execute('SELECT user_name from user_info where user_mail=%s',(mail))
                name = cursor.fetchall()
                name = name[0]['user_name']

                # major_cnt
                major_cnt = cursor.execute('SELECT COUNT(*) from user_info where user_major=%s',(major))
                major_cnt = cursor.fetchall()
                major_cnt = major_cnt[0]['COUNT(*)']

                # rank 구하기
                ranking = cursor.execute('SELECT user_mail, rank() over (order by user_GPA desc) as ranking from user_info WHERE user_major=%s',(major))
                ranking = cursor.fetchall()
                
                # 같은 전공에 지원한 지원자 중에서
                for applier in ranking:
                    # mail이 같은 회원을 찾으면
                    if applier['user_mail'] == mail:
                        # rank를 할당
                        rank = applier['ranking']

                # db 끄기
                db.commit()
                db.close()

                # Show.html로 (name, major, major_cnt 들고)
                return render_template('Show.html',name=name,major=major,sum=major_cnt,rank=rank)
            
            # 아이디는 맞으나, 비밀번호가 틀리면
            else:
                print('비밀번호 오류입니다.')
                flash('비밀번호 오류입니다. 계속해서 로그인에 실패할 시 kurooru@hufs.ac.kr 로 문의해 주시기 바랍니다.')
                # 다시 첫 페이지로
                return redirect('/')
            
        # 기존 회원에 없으면
        else:
            print('존재하지 않는 아이디입니다.')
            flash('존재하지 않는 아이디입니다. 계속해서 로그인에 실패할 시 kurooru@hufs.ac.kr 로 문의해 주시기 바랍니다.')

        # 다시 첫 페이지로
        return redirect('/')
    
    # 로그인 세션이 없고, GET 방식으로 접근했으면,
    else:
        # mysql 연결
        db = pymysql.connect(database='sys', host="hufs-apply.cnlazyly7sdf.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", password="alstjr!!98")
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # 현재 이용자 수
        now_user = cursor.execute('SELECT COUNT(*) FROM user_info;')
        now_user = cursor.fetchall()
        now_user = now_user[0]['COUNT(*)']

        # mysql 닫기
        db.commit()
        db.close()

        return render_template('Landing.html', total=now_user)

@app.route('/signin', methods=['GET', 'POST'])
def signin():

    # POST 방식으로 접근했으면 (회원 등록 버튼을 눌렀으면)
    if request.method == 'POST':
        
        # mail
        mail = request.form['new_mail']
        
        # mail 유효성 검사
        # 아무것도 안적으면
        if not len(mail):
            print('메일을 적어주세요')
            flash('메일을 적어주세요')
            # 재연결
            return redirect('/signin')
        
        # hufs.ac.kr형식 이아니면,
        elif mail[-10:-1] != 'hufs.ac.k':
            print('아이디 형식을 확인해주세요(ㅇㅇㅇ@hufs.ac.kr)')
            flash('아이디 형식을 확인해주세요(ㅇㅇㅇ@hufs.ac.kr)')

        # name
        name = request.form['new_name']
        
        # name 유효성 검사
        # 아무것도 안적으면
        if not len(name):
            print('이름을 적어주세요.')
            flash('이름을 적어주세요.')
            # 재연결
            return redirect('/signin')
        
        # password
        password = request.form['new_password']
        # check_password
        check_password = request.form['check_password']
        
        # password 유효성 검사
        # 아무것도 안적으면
        if not len(password) or not len(check_password):
            print('비밀번호 혹은 비밀번호확인을 적어주세요.')
            flash('비밀번호 혹은 비밀번호확인을 적어주세요.')
            # 재연결
            return redirect('/signin')

        # 비밀번호와 비밀번호확인이 맞지 않으면,
        elif password != check_password:
            print('비밀번호가 맞지 않습니다.')
            flash('비밀번호가 맞지 않습니다.')
            return redirect('/signin')
        
        # GPA
        GPA = request.form['new_GPA']

        # GPA 유효성 검사
        if GPA == '' or not 0 <= float(GPA) <= 4.5:
            print('GPA가 올바르지 않습니다.')
            flash('GPA가 올바르지 않습니다.')
            return redirect('/signin')

        # 비밀번호와 비밀번호 확인이 맞고,
        else:
            # 등록가능한 회원이면(겹치는 회원이 없으면)
            try:
                print('회원 등록이 완료 되었습니다.')
                flash('회원 등록이 완료 되었습니다. 빠른 시일 내에 성적 및 본인 인증메일을 보내 주시기 바랍니다. 매 주 일요일 인증 여부를 확인하여 인증이 완료되지 않은 회원의 데이터는 삭제됩니다.')
                print(mail, name)

                # mysql 연결
                db = pymysql.connect(database='sys', host="hufs-apply.cnlazyly7sdf.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", password="alstjr!!98")
                cursor = db.cursor(pymysql.cursors.DictCursor)
                
                # 회원 정보에 추가
                cursor.execute('INSERT INTO user_info (user_mail, user_name, user_password, user_major, user_GPA) Values (%s, %s, %s, NULL, %s)',(mail, name, password, float(GPA)));

               # 현재 이용자 수
                now_user = cursor.execute('SELECT COUNT(*) FROM user_info;')
                now_user = cursor.fetchall()
                now_user = now_user[0]['COUNT(*)']
                
                # mysql 닫기
                db.commit()
                db.close()
                
                # 다시 처음 화면으로
                return render_template('Landing.html', total=now_user)
            
            # 등록 불가능한 회원이면(겹치는 회원이 있으면)
            except:
                
                print('이미 가입된 회원입니다.')
                flash('이미 가입된 회원입니다.')

                # mysql 연결
                db = pymysql.connect(database='sys', host="hufs-apply.cnlazyly7sdf.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", password="alstjr!!98")
                cursor = db.cursor(pymysql.cursors.DictCursor)

                # 현재 이용자 수
                now_user = cursor.execute('SELECT COUNT(*) FROM user_info;')
                now_user = cursor.fetchall()
                now_user = now_user[0]['COUNT(*)']

                # mysql 닫기
                db.commit()
                db.close()

                # 다시 처음 화면으로
                return render_template('Landing.html', total=now_user)

    # GET 방식으로 접근했으면 (처음 들어왔으면)
    else:
        return render_template('Signin.html')

@app.route('/show')
def show():
    return render_template('Show.html')
    

@app.route('/logout')
def logout():
    
    # logged_in 세션 False 처리
    session['logged_in'] = False
    # 세션 mail 삭제
    session['user_mail'] = ''
    print('성공적으로 로그아웃되었습니다.')
    flash('성공적으로 로그아웃되었습니다.')
    # 처음 화면으로 돌아가기
    return redirect('/')

@app.route('/apply', methods=['GET', 'POST'])
def apply():

    # post 방식으로 접근했으면(입력했으면,)
    if request.method == 'POST':
        
        # 전공
        major = request.form['major']

        # 아무것도 선택하지 않았을 시
        if major == "#":
            print('전공을 선택해 주세요.')
            flash('전공을 선택해 주세요.')
            # 다시 apply로
            return redirect('/apply')

        # 통과했으면,
        print('지원 완료', major)
        flash('모의 지원이 성공적으로 완료되었습니다.')
        
        # mail 뽑기
        mail = session.get('user_mail')
        
        # mysql 연결
        db = pymysql.connect(database='sys', host="hufs-apply.cnlazyly7sdf.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", password="alstjr!!98")
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # major 업데이트
        cursor.execute('UPDATE user_info SET user_major=%s WHERE user_mail=%s', (major, mail))

        # name 뽑기
        name = cursor.execute('SELECT user_name from user_info WHERE user_mail=%s',(mail))
        name = cursor.fetchall()
        name = name[0]["user_name"]

        # major_cnt
        major_cnt = cursor.execute('SELECT COUNT(*) from user_info where user_major=%s',(major))
        major_cnt = cursor.fetchall()
        major_cnt = major_cnt[0]['COUNT(*)']
        
        # rank 구하기
        ranking = cursor.execute('SELECT user_mail, rank() over (order by user_GPA desc) as ranking from user_info WHERE user_major=%s',(major))
        ranking = cursor.fetchall()
        
        # 같은 전공에 지원한 지원자 중에서
        for applier in ranking:
            # mail이 같은 회원을 찾으면
            if applier['user_mail'] == mail:
                # rank를 할당
                rank = applier['ranking']

        # db 끄기
        db.commit()
        db.close()

        # Show.html로(name, major, sum, rank 들고)
        return render_template('Show.html', name = name, major = major, sum = major_cnt, rank=rank)
    
    # get방식으로 접근했으면,
    else:
        # mail 세션에서 얻어내기
        mail = session.get('user_mail')
        
        # mysql 연결
        db = pymysql.connect(database='sys', host="hufs-apply.cnlazyly7sdf.ap-northeast-2.rds.amazonaws.com", port=3306, user="admin", password="alstjr!!98")
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # name뽑기
        name = cursor.execute('SELECT user_name from user_info WHERE user_mail=%s',(mail))
        name = cursor.fetchall()
        name = name[0]['user_name']
        
        # db 끄기
        db.commit()
        db.close()

        # Apply 탬플릿으로(name 들고)
        return render_template('Apply.html', name = name)

# 플라스크 실행
if __name__ == "__main__":
    # port, debug 설정
    app.run(host="0.0.0.0", port=80, debug=True)