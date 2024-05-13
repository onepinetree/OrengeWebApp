import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import warnings
import datetime
warnings.filterwarnings("ignore", category=UserWarning)

if not firebase_admin._apps:
    cred = credentials.Certificate('/etc/secrets/orengewebapp.json')
    #cred = credentials.Certificate('orengewebapp-3c92d3f605ed.json')
    app = firebase_admin.initialize_app(cred)

db = firestore.client()


def getUsername() -> str:
    #return '손아무'
    return st.session_state.username

def getBuddyUsername() -> str:
    st.session_state.back_to_me = getUsername()
    users_ref = db.collection("user").document(getUsername())
    return users_ref.get().to_dict().get('buddy_username', '')

def returnToMe():
    if 'back_to_me' in st.session_state:
        st.session_state.username = st.session_state.back_to_me
    #st.session_state.messages = []

def checkSignIn(inputUsername: str) -> bool:
    # 효율성을 위해 limit을 사용해서 한개의 문서까지만을 찾음,get은 그냥 부분의 스냡샷을 가지고 오는 용도
    # 'users' 컬렉션에서 'nickname' 필드가 inputUsername와과 일치하는 문서 검색
    # where을 사용해서 계산을 firebase측에서 하도록 해 가져와야하는 정보의 양이 적음
    users_ref = db.collection('user')
    query = users_ref.where('username', '==', inputUsername).limit(1).get()
    return len(query) > 0  # 문서가 존재하면 True, 아니면 False 반환


def getOrenge() -> str :
    '''그 사람의 꿈을 가지고 오는 함수'''
    users_ref = db.collection("user").document(getUsername())
    return users_ref.get().to_dict().get('orenge', '')

#print(getDream())


def setOrenge(new_orenge: str) -> None:
    '''오랜지 설정함수'''
    users_ref = db.collection('user').document(getUsername())
    users_ref.update({'orenge' : new_orenge,})


def getGoal(week: int) -> str:
    users_ref = db.collection("user").document(getUsername())
    goal_ref = users_ref.collection('goal_info').document(f'{str(week)}_goal').get()
    return goal_ref.to_dict().get('goal', '')

#print(getGoal(1))

def getSlice(week:int, slice:int) -> str:
    users_ref = db.collection("user").document(getUsername())
    goal_ref = users_ref.collection('goal_info').document(f'{str(week)}_goal').get()
    return goal_ref.to_dict()['slice_info'][slice-1]

#print(getSlice(1,1))

def getSliceNum(week:int) -> int:
    users_ref = db.collection("user").document(getUsername())
    goal_ref = users_ref.collection('goal_info').document(f'{str(week)}_goal').get()
    return goal_ref.to_dict()['slice_num']

#print(getSliceNum(2))


def getCurrentGoalNum()-> int:
    '''그 사람의 현재 도전하고 있는 목표의 번호를 가지고 오는 함수'''
    users_ref = db.collection("user").document(getUsername())
    return users_ref.get().to_dict().get('current_goal_num', '')

#print(getCurrentGoalNum())


def getTotalGoalNum()-> int:
    '''그 사람의 현재 만들어놓은 목표 전부의 개수'''
    users_ref = db.collection("user").document(getUsername())
    return users_ref.get().to_dict().get('total_goal_num', '')
    
#print(getTotalGoalNum())


def getCurrentGoalField() -> dict:
    '''도전하고 있는 그 주의 field에 대한 딕셔너리를 return하는 함수, 없으면 None'''
    users_ref = db.collection("user").document(getUsername())
    goal_ref = users_ref.collection('goal_info').document(f'{str(getCurrentGoalNum())}_goal').get()
    return goal_ref.to_dict()

#print(getCurrentGoalField()['slice_info'][0])


def getCurrentGoal()-> str:
    '''도전하고 있는 그 주의 목표에 대한 정보를 return 하는 함수'''
    return getCurrentGoalField().get('goal','')

#print(getCurrentGoal())


def getCurrentSliceNum()-> int:
    '''도전하고 있는 날의 조각의 원래 순서를 return하는 함수'''
    return getCurrentGoalField().get('current_slice', '')
 
#print(getCurrentSliceNum())


def getCurrentSlice()-> str:
    '''도전하고 있는 날의 조각에 대한 정보를 return하는 함수, 무조건 순서대로 다 해야함'''
    return getCurrentGoalField().get('slice_info', '')[getCurrentSliceNum()-1]
    
#print(getCurrentSlice())


def getCurrentSuccessRate()-> int:
    users_ref = db.collection("user").document(getUsername())
    goal_ref = users_ref.collection('goal_info').document(f'{str(getCurrentGoalNum())}_goal').get()
    return round((sum(goal_ref.to_dict()['slice_bool'])/getSliceNum(week=getCurrentGoalNum()))*100,1)

#print(getCurrentSuccessRate())

def getCurrentSliceBoolList()-> int:
    users_ref = db.collection("user").document(getUsername())
    goal_ref = users_ref.collection('goal_info').document(f'{str(getCurrentGoalNum())}_goal').get()
    return goal_ref.to_dict()['slice_bool']

def getComboRecord():
    users_ref = db.collection("user").document(getUsername())
    return users_ref.get().to_dict().get('date_record', []), users_ref.get().to_dict().get('combo_record', [])


def getCurrentCombo():
    users_ref = db.collection("user").document(getUsername())
    return users_ref.get().to_dict().get('combo', 0)


def successRecord(week:int) -> None:
    '''오늘의 조각을 인증하는 함수'''

    if not getCurrentSliceBoolList()[-1] == True:
        st.session_state.nowGoal = getCurrentSlice()

        new_field = getCurrentGoalField()
        new_field['slice_bool'][getCurrentSliceNum()-1] = True
        if getSliceNum(week=week) > getCurrentSliceNum():
            new_field['current_slice'] += 1

        users_ref = db.collection("user").document(getUsername())
        goal_ref = users_ref.collection('goal_info').document(f'{getCurrentGoalNum()}_goal')

        goal_ref.set(new_field)

        recordCombo()
        recordComboToGraph()
    else:
        pass

#successRecord()


def skipRecord() -> None:
    '''조각을 스킵하는 함수'''
    new_field = getCurrentGoalField()

    if getSliceNum(week=getCurrentGoalNum()) > getCurrentSliceNum():
        new_field['current_slice']+=1

        users_ref = db.collection("user").document(getUsername())
        goal_ref = users_ref.collection('goal_info').document(f'{getCurrentGoalNum()}_goal')

        goal_ref.set(new_field)
    
#skipRecord()

def passWeek() -> None:
    '''다음주로 넘어가는 함수'''
    new_field = db.collection("user").document(getUsername()).get().to_dict()
    if getTotalGoalNum() > getCurrentGoalNum():
        new_field['current_goal_num'] += 1

        users_ref = db.collection("user").document(getUsername())
        users_ref.set(new_field)
    else:
        st.toast('넘어갈 조각이 없어요. 조각하기 페이지에서 다음 조각을 추가해주세요')

#passWeek()

def fixGoal(goalNum: int, newGoal: str) -> None:
    '''몇번째 목표인지와 어떤 목표로 적용할것인지를 적으면 적용해주는 함수'''
    users_ref = db.collection('user').document(getUsername())
    goal_ref = users_ref.collection('goal_info').document(f'{goalNum}_goal')

    new_field = goal_ref.get().to_dict()
    new_field['goal'] = newGoal

    goal_ref.set(new_field)

#fixGoal(1, '아침에 일어나서 물 한잔 마시기')

def fixSlice(goalNum: int, sliceNum: int, newSlice: str)-> None:
    '''몇번째 목표인지와 몇번째 조각을 어떤 조각으로 적용할것인지를 적으면 적용해주는 함수'''
    users_ref = db.collection('user').document(getUsername())
    goal_ref = users_ref.collection('goal_info').document(f'{goalNum}_goal')

    new_field = goal_ref.get().to_dict()

    current_week_delete_condition = (getCurrentGoalNum() == goalNum) and (getCurrentSliceNum() <= sliceNum)
    next_week_delete_condition = (getCurrentGoalNum() < goalNum)

    if current_week_delete_condition or next_week_delete_condition: 
        new_field['slice_info'][sliceNum-1] = newSlice
        goal_ref.set(new_field)

#fixSlice(1,1,'자기전에 물 옆에다 두기')

def addGoalObject() -> str:
    users_ref = db.collection('user').document(getUsername())
    goal_ref = users_ref.collection('goal_info').document(f'{getTotalGoalNum() + 1}_goal')
    goal_ref.set({
        'current_slice' : 1,
        'goal' : '',
        'slice_bool' : [False for i in range(7)],
        'slice_info' : ['' for i in range(7)],
        'slice_num' : 7,
    })
    new_field = users_ref.get().to_dict()
    new_field['total_goal_num'] += 1
    users_ref.set(new_field)

    return '목표가 추가가 완료되었어요! 대단해요😊'

#addGoalObject()


def deleteGoalObject():
    '''전체 목표의 개수를 줄여주는 함수'''
    users_ref = db.collection('user').document(getUsername())
    goal_ref = users_ref.collection('goal_info').document(f'{getTotalGoalNum()}_goal')
    if getTotalGoalNum() > 1 and (getTotalGoalNum() > getCurrentGoalNum()):
        goal_ref.delete()
        new_field = users_ref.get().to_dict()
        new_field['total_goal_num'] -= 1

        users_ref.set(new_field)
    
#deleteGoalObject()

def addSlice(goalNum:int):
    '''컨테이너에 조각 객체를 더해주는 함수'''
    users_ref = db.collection('user').document(getUsername())
    goal_ref = users_ref.collection('goal_info').document(f'{goalNum}_goal')

    new_field = goal_ref.get().to_dict()
    new_field['slice_info'].append('')
    new_field['slice_bool'].append(False)
    new_field['slice_num'] += 1

    goal_ref.set(new_field)

#addSlice(1)

def deleteSlice(goalNum:int):
    '''컨테이너에서 가장 마지막 조각을 빼주는 함수'''
    users_ref = db.collection('user').document(getUsername())
    goal_ref = users_ref.collection('goal_info').document(f'{goalNum}_goal')
    new_field = goal_ref.get().to_dict()

    current_week_delete_condition = (getCurrentGoalNum() == goalNum) and (getCurrentSliceNum() != getSliceNum(week=goalNum))
    next_week_delete_condition = (getCurrentGoalNum() < goalNum) and getSliceNum(week=goalNum) > 1

    if current_week_delete_condition or next_week_delete_condition: 
        try:
            new_field['slice_info'].pop()
            new_field['slice_bool'].pop()
            if new_field['slice_num'] > 0:
                new_field['slice_num'] -= 1
        except:
            pass

    goal_ref.set(new_field)

#deleteSlice(1)



def updateComboOnLogin() -> None:
    '''로그인 시 목표 인증 콤보 상태를 확인하고 필요한 경우 업데이트하는 함수'''
    print('업데이트 콤보 로그인')
    users_ref = db.collection('user').document(getUsername())
    user_data = users_ref.get().to_dict()

    last_verified = user_data.get('last_verified')
    combo_record = user_data.get('combo_record', [])
    date_record = user_data.get('date_record', [])

    today = datetime.date.today()
    #today = datetime.date.today() + datetime.timedelta(days=5)

    if last_verified:
        last_verified_date = datetime.datetime.strptime(last_verified, '%Y-%m-%d').date()
        days_missed = (today - last_verified_date).days - 1

        if days_missed > 0:
            # 연속 인증이 끊어졌을 경우, 콤보에서 끊긴 일수만큼 감소
            combo = user_data.get('combo', 0)
            for i in range(days_missed):
                new_combo = max(0, combo - 1)
                combo = new_combo  # 감소한 콤보를 계속 업데이트

                record_combo = new_combo + combo_record[-1]
                combo_record.append(record_combo)
                date_record.append((last_verified_date + datetime.timedelta(days=i+1)).strftime('%Y-%m-%d'))

            # 루프 종료 후 한 번만 DB 업데이트
            users_ref.update({
                'combo': new_combo,
                'last_verified': (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # 최신 인증 날짜 유지
                'combo_record': combo_record,
                'date_record' : date_record
            })
            #print(f"콤보가 업데이트되었습니다. 새로운 콤보: {new_combo}")
        else:
            #print("콤보에 변동이 없습니다.")
            pass
    else:
        # 사용자가 아직 목표 인증을 한 적이 없는 경우
        print("목표 인증 기록이 없습니다.")
        users_ref.update({
        'combo' : 0, 
        })
        recordComboToGraph()


#updateComboOnLogin()


def recordCombo() -> None:
    print('레코드 콤보')
    '''사용자의 목표 인증 콤보를 기록하고 업데이트하는 함수'''
    users_ref = db.collection('user').document(getUsername())
    user_data = users_ref.get().to_dict()
    last_verified = user_data.get('last_verified')
    combo = user_data.get('combo', 0)
    #today = datetime.date.today()


    if combo < 5:
        if st.session_state.twicecheck == 1:
            st.session_state.twicecheck = 0

        if last_verified:
            combo += 1
        else:
            combo = 1

        # Firestore에 업데이트
        users_ref.update({
            'combo': combo,
        }
        )
        recordComboToGraph()
#recordCombo()


def recordComboToGraph() -> None:
    '''콤보 기록을 DB에 축적하여 저장하는 함수'''
    users_ref = db.collection('user').document(getUsername())
    user_data = users_ref.get().to_dict()

    combo = user_data.get('combo', 0)
    combo_record = user_data.get('combo_record', [0])
    date_record = user_data.get('date_record', [""])
    last_verified = user_data.get('last_verified')
    last_verified_date = datetime.datetime.strptime(last_verified, '%Y-%m-%d').date() if last_verified else None

    new_total = (combo_record[-1] + combo) if last_verified else combo
    today = datetime.date.today()

    if (today == last_verified_date):
        #중복인증할때
        if st.session_state.twicecheck != 1:
            print('중복인증할떄')

            combo_record[-1] +=1
            users_ref.update({
                'combo_record': combo_record,
            })
            st.session_state.twicecheck = 1

    elif not last_verified and combo == 1:
        #처음 인증할때
        combo_record[-1] +=1
        st.session_state.twicecheck = 1

        print('처음 인증할때')
        users_ref.update({
        'combo_record': combo_record,
        'last_verified': today.strftime('%Y-%m-%d')
        })

    elif not last_verified and combo == 0:
        #처음 들어왔을때
        print('처음 들어왔을때')
        combo_record.append(new_total)  # 축적된 콤보 리스트 업데이트
        date_record.append(today.strftime('%Y-%m-%d'))

        users_ref.update({
            'combo_record': combo_record,
            'date_record' : date_record,
        })

    else:
        #하루에 첫 인증
        print('일반인증할때')
        st.session_state.twicecheck = 1

        combo_record.append(new_total)  # 축적된 콤보 리스트 업데이트
        date_record.append(today.strftime('%Y-%m-%d'))

        users_ref.update({
            'combo_record': combo_record,
            'date_record' : date_record,
            'last_verified': today.strftime('%Y-%m-%d')

        })

