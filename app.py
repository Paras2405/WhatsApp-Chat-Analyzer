import streamlit as st
import matplotlib.pyplot as plt
from seaborn import heatmap

import preprocessor
import seaborn as sns

import helper
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    #st.dataframe(df)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    if 'group-notification' in user_list:
      user_list.remove('group-notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,links= helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(num_media_messages)
        with col4:
            st.header("Total Links")
            st.title(links)



        #Timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['messages'],color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")
        daily_time= helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_time['only_date'], daily_time['messages'], color="red")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity Map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most active day")
            active_day=helper.week_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(active_day.index,active_day.values)
            st.pyplot(fig)
        with col2:
            st.header("Most active month")
            active_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(active_month.index, active_month.values,color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        #finding most active users in the group
        if selected_user=="Overall":
            st.title("Most Active users in the group")
            x,new_df=helper.most_active_users(df)
            fig,ax=plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #WordCloud
        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user, df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        mcw=helper.most_common_words(selected_user, df)
        st.title("Most Common words")
        fig,ax=plt.subplots()
        ax.barh(mcw[0],mcw[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #Emoji count
        emo=helper.emoji_count(selected_user, df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emo)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emo['count'].head(), labels=emo['emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)


        #heatmap
        st.title(" Weekly Activity Heatmap")
        week_heatmap=helper.activity_heat_map(selected_user, df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(week_heatmap)
        st.pyplot(fig)







