import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.title('Streamlit Hello World')  # タイトル

st.write('Display Image')  # 画像の表示

img = Image.open('img031.jpg')  # 画像の読み込み
st.image(img, caption='sample', use_column_width=True)  # 画像の表示
