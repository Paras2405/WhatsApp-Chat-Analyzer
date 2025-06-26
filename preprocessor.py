'''import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'dates': dates})
    # convert dates string to actual date
    df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%y, %H:%M - ')
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group-notification')
            messages.append(entry[0])
    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['month_num']=df['dates'].dt.month
    df['minute'] = df['dates'].dt.minute
    df['day_name']=df['dates'].dt.day_name()
    df['only_date'] = df['dates'].dt.date

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour) +"-"+str('00'))
        elif hour==0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period']=period




    return df
'''

import re
import pandas as pd
from datetime import datetime


def parse_datetime(date_str):
    # Normalize weird spaces (e.g., narrow non-breaking space, non-breaking space)
    date_str = date_str.replace('\u202f', ' ').replace('\u00a0', ' ').strip()

    # Try multiple datetime formats
    formats = [
        '%d/%m/%Y, %I:%M %p',
        '%d/%m/%y, %I:%M %p',
        '%d/%m/%Y, %H:%M',
        '%d/%m/%y, %H:%M'
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {date_str}")


def preprocess(data):
    # Pattern to match both 12-hour and 24-hour time
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[APMapm]{2})?\s-\s'

    # Split messages and dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Clean and parse dates
    cleaned_dates = [date.strip(" -") for date in dates]
    parsed_dates = [parse_datetime(date) for date in cleaned_dates]

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'dates': parsed_dates})

    # Split user and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group-notification')
            messages.append(entry[0])
    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Add date-related columns
    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['month_num'] = df['dates'].dt.month
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute
    df['day_name'] = df['dates'].dt.day_name()
    df['only_date'] = df['dates'].dt.date

    # Create time periods (hour ranges)
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour + 1}")
    df['period'] = period

    return df
