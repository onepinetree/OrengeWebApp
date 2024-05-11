import matplotlib.pyplot as plt
import plotly.graph_objects as go


def draw_progress_bar(percentage, title="진행 상태"):
    # 이미지 로드
    #image = imread('assests/graph_background.png')
    
    # 백그라운드 설정
    fig, ax = plt.subplots(figsize=(15, 1))  # y 축의 크기 조정 필요시 변경 가능
    
    # 배경 이미지 설정
    #ax.imshow(image, aspect='auto', extent=[0, 100, -1, 1])  # y 축 범위 조정
    
    fig.patch.set_facecolor('black')  # 전체 배경색 설정
    ax.set_facecolor('black')  # 축 배경색 설정
    ax.set_xlim(0, 100)  # x축 범위 설정
    ax.set_xticks(range(0, 101, 10))  # x축 눈금 설정
    ax.set_yticks([])  # y축 눈금 숨기기

    # 진행 바 그리기
    bars = ax.barh(0, percentage, height=2, color='orange', alpha=0.8)  # 투명도 조정 및 y 위치 조정
    for bar in bars:
        ax.text(bar.get_width() - 5, bar.get_y() + bar.get_height()/2, f'{percentage}%',
                va='center', ha='right', color='white', fontweight='bold')  # 진행률 표시

    return fig  # fig 객체 반환


# 게이지 차트를 그리는 함수
def create_gauge_chart(value):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",  # 게이지와 숫자 표시
        value = value,
        number={'suffix': "%"},  # 숫자 뒤에 퍼센트 기호 추가
        domain = {'x': [0, 1], 'y': [0, 1]},
        #title = {'text': "Progress Gauge"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "orange"},  # 게이지 바의 색상을 오렌지로 설정
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, value], 'color': 'orange'},
            ],
           }))
    return fig
