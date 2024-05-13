import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

if not firebase_admin._apps:
    cred = credentials.Certificate('orengewebapp-3c92d3f605ed.json')
    #cred = credentials.Certificate('/etc/secrets/orengewebapp.json')

    app = firebase_admin.initialize_app(cred)

db = firestore.client()

def getThreadId(id: str) -> str:
    users_ref = db.collection("user").document(id)
    return users_ref.get().to_dict().get('thread_id', '')
    
def setThreadId(id: str) :
    users_ref = db.collection("user").document(id)
    users_ref.update({'thread_id' : getThreadId(),})
    
def saveChat(username: str, role: str, prompt: str) -> None:
    '''username과 지금 대화의 role과 그의 prompt를 입력하면 시간과 함께 DB에 저장되는 함수'''
    now = datetime.utcnow() + timedelta(hours=9)
    doc_ref = db.collection("user").document(username)
    chat_ref = doc_ref.collection('chat_log').document(now.strftime("%Y-%m-%d"))
    #DocumnetReference객체는 바로 .to_dict() 메소드를 사용할 수 없고 DocumentSnapshot만 가능하다. 그것의 변환과정
    doc_snapshot = chat_ref.get()

    # DocumentSnapshot에서 데이터를 가져온다. 없을 경우 빈 딕셔너리를 사용한다.
    if doc_snapshot.exists:
        updated_chat = doc_snapshot.to_dict()
    else:
        updated_chat = {}

    # 채팅 메시지를 추가한다. 'chat num'을 채팅 메시지의 순번으로 사용한다.
    chat_num = int(updated_chat.get('chat_num', 0))  # 'chat_num'이 없으면 0을 기본값으로 사용
    updated_chat[str(chat_num + 10)] = f'({role}) {prompt}'
    #chat_num을 업데이트한다.
    updated_chat['chat_num'] = chat_num + 1
    # 업데이트된 채팅 데이터로 문서를 설정한다.
    chat_ref.set(updated_chat)



from openai import OpenAI
import time
from api_info import API_KEY

client = OpenAI(api_key = API_KEY)


def createThread()->str:
    '''Thread를 생성하고 thread의 id를 return 하는 함수'''
    empty_thread = client.beta.threads.create()
    return empty_thread.id


def sendMessagetoThread(thread_id : str, user_prompt : str):
    '''user의 prompt를 받고 thread에 추가해주는 함수'''
    thread_message = client.beta.threads.messages.create(
    thread_id,
    role="user",
    content=user_prompt,
    )

def runAndRetrieveData(assistant_id : str, thread_id : str) -> str:
    '''thread를 run하고 status를 확인한후 value를 return 해주는 함수'''
    run = client.beta.threads.runs.create(
    thread_id = thread_id,
    assistant_id = assistant_id
    )
    run_id = run.id

    while True:
        retrieve_run = client.beta.threads.runs.retrieve(
        thread_id = thread_id,
        run_id = run_id
        )
        if(retrieve_run.status == 'completed'):
            thread_messages = client.beta.threads.messages.list(thread_id)
            #print(thread_messages.data)
            return thread_messages.data[0].content[0].text.value
            break
        else:
            time.sleep(2)


