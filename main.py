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

st.write('目標：体重６２ｋｇ体脂肪率１５％')


with st.form(key='sokutei_form'):
    st.write('測定結果入力')
    left,right=st.columns(2)
    weight = float(left.number_input('体重'))
    TaishibouRitsu = float(right.number_input('体脂肪率'))
    
    touroku_buton = st.form_submit_button('登録')
    
    if touroku_buton:

        # １．ファイル名を指定してワークブックを選択
        worksheet = workbook.worksheet('記録')
        df = pd.DataFrame(worksheet.get_all_values()[1:], columns=worksheet.get_all_values()[0])
        
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        
        todo = '測定'
        
        kitaiweight = float(list(df['期待体重'])[-1])
        
        kari_li = [[now,todo,0,weight,TaishibouRitsu,kitaiweight]]
        
        kari_df = pd.DataFrame(data = kari_li, columns=['日時','やったこと','カロリー','体重','体脂肪率','期待体重'])
        
        df = df.append(kari_df, ignore_index = True, sort=False)
        
        set_with_dataframe(worksheet, df,include_index = False)
        
        st.dataframe(df.tail(5))
        st.text('登録完了')


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
        
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        todo = syokuzi
        weight = float(list(df['体重'])[-1])
        TaishibouRitsu = float(list(df['体脂肪率'])[-1])
        kitaiweight = float(list(df['期待体重'])[-1]) + round(syokuzi_calory/7200,4)
        
        kari_li = [[now,todo,syokuzi_calory,weight,TaishibouRitsu,kitaiweight]]
        
        kari_df = pd.DataFrame(data = kari_li, columns=['日時','やったこと','カロリー','体重','体脂肪率','期待体重'])
        
        df = df.append(kari_df, ignore_index = True, sort=False)
        
        set_with_dataframe(worksheet,df,include_index = False)
        
        st.dataframe(df.tail(5))
        
        st.text('登録完了')


with st.form(key='traning_form'):
    st.write('トレーニング入力')
    mets_worksheet = workbook.worksheet('METs')
    undou_list_df = pd.DataFrame(mets_worksheet.get_all_values()[1:], columns=mets_worksheet.get_all_values()[0])
    
    undou = st.selectbox('運動',tuple(undou_list_df['運動']))
    
    for i in range(len(list(undou_list_df['運動']))+1):
        if undou == list(undou_list_df['運動'])[i]:
            mets = float(list(undou_list_df['METs'])[i])
            break
        
    syohi_calory = st.number_input('カロリー')
    
    undou_time = st.number_input('運動時間（分）')
    
    touroku_buton = st.form_submit_button('登録')
    
    if touroku_buton:

        # １．ファイル名を指定してワークブックを選択
        worksheet = workbook.worksheet('記録')
        df = pd.DataFrame(worksheet.get_all_values()[1:], columns=worksheet.get_all_values()[0])
        
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        todo = undou
        weight = float(list(df['体重'])[-1])
        TaishibouRitsu = float(list(df['体脂肪率'])[-1])
        
        if syohi_calory==0:
            undou_caloly = mets*weight*(undou_time/60)*1.05
        else:
            undou_caloly = syohi_calory
            
        kitaiweight = float(list(df['期待体重'])[-1]) -  round(undou_caloly/7200,4)
        
        kari_li = [[now,todo,undou_caloly,weight,TaishibouRitsu,kitaiweight]]
        
        kari_df = pd.DataFrame(data = kari_li, columns=['日時','やったこと','カロリー','体重','体脂肪率','期待体重'])
        
        df = df.append(kari_df, ignore_index = True, sort=False)
        
        set_with_dataframe(worksheet, df,include_index = False)
        
        st.dataframe(df.tail(5))
        
        st.text('登録完了')