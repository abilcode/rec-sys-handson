import numpy as np
import pandas as pd

def convert_day(day):
    if day.lower() == 'senin':
        day_converted = 'Monday'
    elif day.lower() == 'selasa':
        day_converted = 'Tuesday'
    elif day.lower() == 'rabu':
        day_converted = 'Wednesday'
    elif day.lower() == 'kamis':
        day_converted = 'Thursday'
    elif day.lower() == 'jumat':
        day_converted = 'Friday'
    elif day.lower() == 'sabtu':
        day_converted = 'Saturday'
    elif day.lower() == 'minggu':
        day_converted = 'Sunday'
    
    return day_converted

def convert_time(times):
    times = times + ':00:00'
    return times

def build_mentee_df(id, is_android, is_webdev, is_ios, is_flutter, is_fe, is_be, is_cc):
    mentee_dict = {}
    cols = [f"interest_{i+1}" for i in range(7)]
    interests = [is_android, is_webdev, is_ios, is_flutter, is_fe, is_be, is_cc]

    for col, interest in zip(cols, interests):
        mentee_dict[col] = [int(interest)]
    df = pd.DataFrame({"id": [id], **mentee_dict})
    return df

def build_mentee_availability(id, time_dict, num_avail):
    ids = [id for i in range(num_avail)]
    time_dict['User ID'] = ids
    df = pd.DataFrame(time_dict)
    return df 
    

def filtering_time(id, mentee_availability, mentor_availability):
    mentor2mentee_time = {}
    list_menteeId = [id]
    for menteeId in list_menteeId:
        mentee_id_curr = mentee_availability.loc[mentee_availability['User ID'] == menteeId,]
        
        matched = mentee_id_curr.merge(mentor_availability, on=['Day of Week', 'Start Hour'], how='inner')
        list_matched_mentors = sorted(list(matched['User ID_y'].unique()))
        mentor2mentee_time[menteeId] = list_matched_mentors
    df = pd.DataFrame([(k, v) for k, values in mentor2mentee_time.items() for v in values], columns=['user_id', 'mentor_id'])

    return df, mentor2mentee_time

def cosine_similarity(mentee, mentor):
    vec1 = mentee
    vec2 = mentor
    cosine = np.dot(vec1,vec2)/((np.dot(vec1,vec1)*np.dot(vec2,vec2))**0.5) 
    return cosine

def calculate_similarity(mentor2mentee_df, df_mentee, df_mentor):
    sim_mentee = {}
    con = []
    var = [f"interest_{i+1}" for i in range(7)]
    menteeId = list(mentor2mentee_df['user_id'].unique())
    mentorId = list(mentor2mentee_df['mentor_id'].unique())

    for mentee in menteeId:
        mentee_interest = df_mentee.loc[df_mentee.id==mentee,var].values.reshape(1,-1)
        mentee_interest = np.squeeze(np.asarray(mentee_interest))
        for mentor in mentorId:
            mentor_interest = df_mentor.loc[df_mentor.id==mentor,var].values.reshape(1,-1)
            mentor_interest = np.squeeze(np.asarray(mentor_interest))
            sim = cosine_similarity(mentee_interest, mentor_interest)
            con.append(sim)
        
        sim_mentee[mentee] = con
        con = []

    return sim_mentee

def build_similarity_df(id, df, sim_mentee):
    df['similarity'] = df['user_id'].copy()
    for row in range(df.shape[0]):
        #print(row)
        # mentee = df.iloc[row,0]
        # mentor = df.iloc[row,1]
        #print(user,mentor)
        df.loc[row, 'similarity'] = sim_mentee[id][row]

    df_sorted_rating = df.sort_values(by=['user_id','similarity'],ascending=[True,False]).copy()
    
    return df_sorted_rating

def give_mentor(sim_df):
    mentor_id = list(sim_df['mentor_id'].unique())
    return mentor_id[0]


    # df_ = df.copy()
    # df_['rating'] = df_['similarity'].copy()
    # df_['rating'] = df_.rating.apply(lambda row: np.random.randint(1, 6))
    # df_sorted_rating = df_.sort_values(by=['user_id','similarity','rating'],ascending=[True,False,False]).copy()
    # df_sorted_rating.fillna(0,inplace=True)
    
    # return df_sorted_rating
