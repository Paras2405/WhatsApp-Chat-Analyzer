from streamlit import columns
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extractor=URLExtract()
def fetch_stats(selected_user, df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    #fetch num of messages
    num_messages=df.shape[0]
    #fetch number of words
    words=[]
    for message in df['messages']:
        words.extend(message.split())
    #fetch number of media send
    num_media_messages=df[df['messages']=='<Media omitted>\n'].shape[0]
    #fetch number of links send
    links=[]
    for message in df['messages']:
        urls=extractor.find_urls(message)
        links.extend(urls)

    return num_messages,len(words),num_media_messages,len(links)

def most_active_users(df):
    x=df['user'].value_counts().head()
    df = (df['user'].value_counts(normalize=True) * 100).round(2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df
def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user,df):
  f=open('stop_hinglish.txt','r')
  stop_words=f.read()
  if selected_user != 'Overall':
      df = df[df['user'] == selected_user]
  temp=df[df['user']!='group_notification']
  updated_df=temp[temp['messages']!='<Media omitted>\n'] #in this df messages with no group_notification and Media omitted
  words=[]
  for message in updated_df['messages']:
    for word in message.lower().split():
        if word not in stop_words:
            words.append(word)
  mcw=pd.DataFrame(Counter(words).most_common(20))
  return mcw
def emoji_count(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['messages']:
        emojis.extend([e for e in message if emoji.is_emoji(e)])
    emo = pd.DataFrame(Counter(emojis).most_common(20), columns=['emoji', 'count'])
    return emo

def monthly_timeline(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-" +str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    daily_time = df.groupby(['only_date']).count()['messages'].reset_index()
    return daily_time

def week_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heat_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    week_heatmap=df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)
    return week_heatmap

