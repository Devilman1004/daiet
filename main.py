import streamlit as st
import gspread
import json
import pandas as pd
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from gspread_dataframe import set_with_dataframe

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
json_path = 'daiet-364301-29624efefdd3.json'
#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)
workbook = gc.open('ダイエット')

st.title('ダイエット記録')

st.header('目標：体重６２ｋｇ　体脂肪率１５％')

sokutei_bt = st.button('測定結果入力')
if sokutei_bt:
    with st.form(key='sokutei_form'):
        st.write('測定結果入力')
        left,right=st.columns(2)
        weight = left.number_input('体重')
        TaishibouRitsu = right.number_input('体脂肪率')
        
        touroku_buton = st.form_submit_button('登録')
        
        if touroku_buton:

            # １．ファイル名を指定してワークブックを選択
            worksheet = workbook.worksheet('記録')
            df = pd.DataFrame(worksheet.get_all_values()[1:], columns=worksheet.get_all_values()[0])
            
            today = datetime.date.today()
            gentime = datetime.datetime.now().time()
            todo = '測定'
            
            kari_li = [[today,gentime,todo,0,weight,TaishibouRitsu,weight]]
            
            kari_df = pd.DataFrame(data = kari_li, columns=['年月日','時間','やったこと','カロリー','体重','体脂肪率','期待体重'])
            
            df = df.append(kari_df, ignore_index = True, sort=False)
            
            set_with_dataframe(worksheet, df,include_index = False)
            
            st.text('登録完了')

syokuzi_bt = st.button('食事入力')
if syokuzi_bt:       
    with st.form(key='syokuzi_form'):
        st.write('食事入力')
        left,right=st.columns(2)
        syokuzi = left.selectbox(
        '食事',
        ('朝食', '昼食', '夕食','間食'))
        syokuzi_calory = right.number_input('カロリー')
        touroku_buton = st.form_submit_button('登録')
        
        if touroku_buton:

            # １．ファイル名を指定してワークブックを選択
            worksheet = workbook.worksheet('記録')
            df = pd.DataFrame(worksheet.get_all_values()[1:], columns=worksheet.get_all_values()[0])
            
            today = datetime.date.today()
            gentime = datetime.datetime.now().time()
            todo = syokuzi
            weight = int(list(df['体重'])[-1])
            TaishibouRitsu = int(list(df['体脂肪率'])[-1])
            kitaiweight = float(list(df['期待体重'])[-1]) + round(syokuzi_calory/7200,4)
            
            kari_li = [[today,gentime,todo,syokuzi_calory,weight,TaishibouRitsu,kitaiweight]]
            
            kari_df = pd.DataFrame(data = kari_li, columns=['年月日','時間','やったこと','カロリー','体重','体脂肪率','期待体重'])
            
            df = df.append(kari_df, ignore_index = True, sort=False)
            
            set_with_dataframe(worksheet, df,include_index = False)
            
            st.text('登録完了')

traning_bt = st.button('トレーニング入力')
if traning_bt:        
    with st.form(key='traning_form'):
        st.write('トレーニング入力')
        worksheet = workbook.worksheet('METs')
        df = pd.DataFrame(worksheet.get_all_values()[1:], columns=worksheet.get_all_values()[0])
        
        undou = st.selectbox('運動',tuple(df['運動']))
        
        for i in range(len(list(df['運動']))+1):
            if undou == list(df['運動'])[i]:
                mets = float(list(df['METs'])[i])
                break
        
        undou_time = st.number_input('運動時間（分）')
        touroku_buton = st.form_submit_button('登録')
        
        if touroku_buton:

            # １．ファイル名を指定してワークブックを選択
            worksheet = workbook.worksheet('記録')
            df = pd.DataFrame(worksheet.get_all_values()[1:], columns=worksheet.get_all_values()[0])
            
            today = datetime.date.today()
            gentime = datetime.datetime.now().time()
            todo = undou
            weight = int(list(df['体重'])[-1])
            TaishibouRitsu = int(list(df['体脂肪率'])[-1])
            undou_caloly = mets*weight*(undou_time/60)*1.05
            kitaiweight = float(list(df['期待体重'])[-1]) -  round(undou_caloly/7200,4)
            
            kari_li = [[today,gentime,todo,undou_caloly,weight,TaishibouRitsu,kitaiweight]]
            
            kari_df = pd.DataFrame(data = kari_li, columns=['年月日','時間','やったこと','カロリー','体重','体脂肪率','期待体重'])
            
            df = df.append(kari_df, ignore_index = True, sort=False)
            
            set_with_dataframe(worksheet, df,include_index = False)
            
            st.text('登録完了')