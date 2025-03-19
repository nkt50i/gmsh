import streamlit as st

st.set_page_config(page_title="👋", layout="wide")

st.markdown("""
    <h1 style="text-align:center; font-size: 50px;">Филиал Московского государственного университета имени М. В. Ломоносова в городе Сарове</h1>
""", unsafe_allow_html=True)
st.markdown("""
    <h1 style="text-align:center; font-size: 40px;">Кафедра математики</h1>
""", unsafe_allow_html=True)
st.markdown("""
    <h1 style="text-align:center; font-size: 35px;">Группа ВМ - 124</h1>
""", unsafe_allow_html=True)

# Дополнительное изображение по центру
st.image("logo.jpg", width=300, use_container_width=True)

st.markdown("""
    <h1 style="text-align:center; font-size: 50px;">Gmsh</h1>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style="text-align:left; font-size: 35px;">Презентацию подготовили:</h1>
""", unsafe_allow_html=True)

# Данные участников
participants = [
    {"name": "Головня Никита", "photo": "0.jpg"},
    {"name": "Александр Романенко", "photo": "1.jpg"},
    {"name": "Гашигуллин Камиль", "photo": "2.jpg"},
    {"name": "Коврижных Анастасия", "photo": "3.jpg"},
    {"name": "Сержантов Артемий", "photo": "4.jpg"},
    {"name": "", "photo": "6.jpg"},
]

# Вывод участников в две строки
row1 = participants[:3]  
row2 = participants[3:]  

cols1 = st.columns(3)
for i, participant in enumerate(row1):
    with cols1[i]:
        st.image(participant["photo"], width=200)
        st.markdown(f"""
            <h3 style="margin: 0; text-align: left;">{participant['name']}</h3>
        """, unsafe_allow_html=True)

cols2 = st.columns(3)
for i, participant in enumerate(row2):
    with cols2[i]:
        st.image(participant["photo"], width=200)
        st.markdown(f"""
            <h3 style="margin: 0; text-align: left;">{participant['name']}</h3>
        """, unsafe_allow_html=True)

st.markdown("""
    <h2 style="text-align:left;">О презентации</h2>
    <p style="text-align:left; font-size: 18px;">
        В данной презентации рассматривается использование Gmsh — мощного инструмента для генерации 
        конечных элементов. Мы обсудим его основные возможности, настройку сеток, работу с файлами 
        форматов .geo и .msh, а также примеры его применения в различных задачах моделирования.
    </p>
    <p style="text-align:left; font-size: 18px;">
        Данный проект можно посмотреть и скачать на 
        <a href="https://github.com/nkt50i/Gmsh" target="_blank" style="font-weight: bold;">
        GitHub</a>.
    </p>
    <p style="text-align:left; font-size: 18px; font-weight: bold;">
        ❗❗❗ Все ссылки в презентации работают только с VPN ❗❗❗
    </p>
""", unsafe_allow_html=True)