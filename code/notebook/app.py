import pandas as pd
from filtering_matchmaking import *

mentor_availability = pd.read_csv("data_generate/mentor_availability.csv")
mentor_df = pd.read_csv("data_generate/mentor_interest.csv")

# input name
name = str(input("Nama: "))
print("\n")
id = int(input("Masukkan Id: "))
print("\n")

# input interest
print("Pilih ketertarikanmu: ")
is_android = input('Android Development? (y/n): ').lower().strip() == 'y'
is_webdev = input('Web Development? (y/n): ').lower().strip() == 'y'
is_ios = input('IOS Development? (y/n): ').lower().strip() == 'y'
is_flutter = input('Flutter (y/n): ').lower().strip() == 'y'
is_fe = input('Front-End Development? (y/n): ').lower().strip() == 'y'
is_be = input('Back-End Development? (y/n): ').lower().strip() == 'y'
is_cc = input('Computer Cloud (y/n): ').lower().strip() == 'y'

mentee_df = build_mentee_df(id, is_android, is_webdev, is_ios, is_flutter, is_fe, is_be, is_cc)

is_lanjut = True
while is_lanjut:
    # input time availability
    # days
    time_dict = {'Day of Week' : [], 'Start Hour' : []}
    again = True
    num_avail = 0
    while again:
        print("\n")
        print("Masukkan Kesediaan Harimu: ")
        days = str(input("Bisa hari apa?: "))
        days = convert_day(days)
        # times 
        print("\n")
        print("Masukkan Kesediaan Waktumu: ")
        times = str(input("Bisa jam berapa (00/01/02/.../23): "))
        times = convert_time(times)

        time_dict['Day of Week'].append(days)
        time_dict['Start Hour'].append(times)

        num_avail += 1
        print("\n")
        again = input('Tambah lagi? (y/n): ').lower().strip() == 'y'

    # print(time_dict)
    mentee_availability = build_mentee_availability(id, time_dict, num_avail)
    # print(mentee_df)
    # print(mentee_availability)

    # filter based on time availability
    mentor2mentee_df, mentor2mentee_dict = filtering_time(id, mentee_availability, mentor_availability)
    # print(mentor2mentee_df)
    # print("\n")


    # calculate similarity
    if mentor2mentee_df.empty:
        print("Tidak ada mentor yang cocok dengan waktu anda")
        is_lanjut = input('Mau cari mentor lagi? (y/n): ').lower().strip() == 'y'

    else:
        sim_dict = calculate_similarity(mentor2mentee_df, mentee_df, mentor_df)
        sim_df = build_similarity_df(id, mentor2mentee_df, sim_dict)
        print(sim_df)
        print("\n")

        mentor_id = give_mentor(sim_df)
        print("Mentor anda ({}) adalah mentorID {}".format(id, mentor_id))

        is_lanjut = False

    # print(mentor2mentee_df)
    # print("\n")
    # print(sim_dict)
    # print("\n")

