import streamlit as st
import gspread
import json
import pandas as pd
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
json_path = 'daiet-364301-29624efefdd3.json'
#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)
# １．ファイル名を指定してワークブックを選択
workbook = gc.open('ダイエット')
worksheet = workbook.worksheet('記録')
df = pd.DataFrame(worksheet.get_all_values()[1:], columns=worksheet.get_all_values()[0])

st.title('過去の記録')

chart_data = df[['日時','体重','体脂肪率','期待体重']].set_index('日時')

st.line_chart(chart_data)

st.dataframe(df)