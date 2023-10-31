import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.title('Streamlit Hello World')

df = pd.DataFrame({
    "1列目":[1,2,3,4],
    "2列目":[10,20,30,40]
})

st.write(df)  # データフレームの表示
st.dataframe(df.style.highlight_max(axis=0),width=100, height=100)

df2 = pd.DataFrame(np.random.randn(10, 20), columns=("col %d" % i for i in range(20)))

st.dataframe(df2.style.highlight_max(axis=0))

st.table(df.style.highlight_max(axis=0)) # データフレームの表示（スタイル付き）


df3 = pd.DataFrame(
    np.random.rand(20, 3),
    columns=['a', 'b', 'c']
)   # データフレームの作成

st.line_chart(df3) # 折れ線グラフの表示
st.area_chart(df3) # エリアグラフの表示

df3 = pd.DataFrame(
    np.random.rand(100, 2)/[50, 50] + [35.69, 139.70],
    columns=['lat', 'lon']
)

st.write(df3)

st.map(df3) # 地図の表示

st.write('Display Image on Wednesday') #画像の表示

img = Image.open('../../pic/img031.jpg') # 画像の読み込み
st.image(img, caption='sample', use_column_width=True) # 画像の表示

st.write('Interactive Widgets') # ウィジェットの表示

text = st.sidebar.text_input('あなたの趣味を教えてください。') # テキスト入力
'あなたの趣味は', text, 'です。' # テキスト表示

condition = st.sidebar.slider('あなたの今の調子は？', 0, 100, 50) # スライダー
'コンディション：', condition # テキスト表示

