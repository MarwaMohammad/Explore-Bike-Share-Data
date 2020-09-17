import pandas as pd
from datetime import datetime as dt
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city, month, day = "","",""
    day_of_week =['0','1','2','3','4','5','6', 'all']
    cities =["new york city", "washington", "chicago"]
    filter_list =['day','month','both','none']
    months = ["all","january","february","march","april","may","june","all"]


    print('Hello! Let\'s explore some US bikeshare data! ')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New york city or Washington ").lower()
    while (city not in cities):
        city = input("Please, Note you should choose one of these cities Chicago, New york city or Washington ").lower()

    filter_type = input("Would you like to filter date by month, day, both or not at at all. Type none for non time filter ").lower()

    while filter_type not in filter_list:
        filter_type = input("please Enter the filter type: day, month, both, none ").lower()
        # get user input for month (all, january, february, ... , june)
    # Here the month = {month or all} 2 cases all day in a month or all days in all months
    if filter_type == 'month':
        month = input("Woud you like to see data for which month January, February, ... , June? or all ").lower()
        while month not in months:
            month = input("Please, Note you should choose which month January, February, ... , June? or all ").lower()
        day = 'all'
    #Here the month = all, day = {all, day}
    #Here 2 cases of (a specific day in all months, all days in a month)
    elif filter_type == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Which day? please enter an integer value (Monday = 0) or all ").lower()
        while day not in day_of_week:
            day = input("Which day? please enter an integer value (Monday = 0) or all ").lower()
        month = "all"
    elif filter_type == 'both':
        #Here month may ={month or all} and day may be {day or all}
        #4  case are {all days in all moths, a day in moth, all days in moth, a day in all month }    elif month_or_day == 'both':
        month = input("Woud you like to see data for which month January, February, ... , June? or all ").lower()
        while month not in months:
            month = input("Please, Note you should choose which month January, February, ... , June? or all ").lower()

        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Which day? please enter an integer value (Monday = 0) or all ").lower()
        while day not in day_of_week:
            day = input("Which day? please enter an integer value (Monday = 0) or all ").lower()

    elif filter_type == 'none':
        month = 'all'
        day = 'all'

    print('-'*40)
    return city, month, day, filter_type


def load_data(city="chicago", mon="march", day='5'):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.DataFrame()
    data_file = pd.DataFrame()

    file_name = CITY_DATA[city]

    try:
        data_file = pd.read_csv(file_name)
    except IOError:
        print("Can't open the file")

    months_options = {"january" : 1, "february" : 2, "march" : 3, "april" : 4, "may" : 5, "june" : 6, "all":7}
    months_options_list = ["january", "february", "march", "april", "may", "june" ]
    dayname_OfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    dayOfWeek = [0,1,2,3,4,5,6]

    # to convert the string into date and time
    data_file['Start Time'] = pd.to_datetime(arg = data_file['Start Time'], format = '%Y-%m-%d %H:%M:%S')

    data_file['date'] = data_file['Start Time'].dt.date
    data_file['month'] = data_file['Start Time'].dt.month
    data_file['weekday'] = data_file['Start Time'].dt.weekday


    if (mon == "all") and (day == "all"):
        print("All days and in all Months")
        df = data_file

    elif (mon == 'all') and (int(day) in dayOfWeek):
        print("All data on {}s".format(dayname_OfWeek[int(day)]))
        df = data_file[data_file['weekday'] == int(day)]

    elif (mon in months_options_list ) and (day == 'all'):
        print()
        print("All Days in {}".format(mon.title()))
        df = data_file[data_file['month'] == months_options[mon]]

    elif (int(day) in dayOfWeek) and (mon in months_options_list):
        print()
        print("ALL {}s in {}".format(dayname_OfWeek[int(day)],mon.title()))
        df = data_file[data_file['month'] == months_options[mon]]
        df = df[df['weekday'] == int(day)]
    else:
        print("Option is not exist")

    return df

def time_stats(df,city,month,day,filter_type):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel based on filter type '+filter_type+'\n')
    start_time = time.time()

    if (month == 'all') and (day == 'all'):
        # display the most common month
        popular_month = df['month'].mode()[0]
        print("The most common Month in the year is {}".format(popular_month))

        # display the most common day of week
        popular_day = df['weekday'].mode()[0]
        print("The most common day in the week is {}".format(popular_day))

        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        print("The most common hour is {}".format(popular_hour))

    elif (month == 'all') and (day != 'all'):
        # display the most common month
        popular_month = df['month'].mode()[0]
        print("The most common Month in the year is {}".format(popular_month))

        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        print("The most common hour is {}".format(popular_hour))

    elif (month != 'all') and (day == 'all'):
        # display the most common day of week
        popular_day = df['weekday'].mode()[0]
        print("The most common day in the week is {}".format(popular_day))

        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        print("The most common hour is {}".format(popular_hour))

    elif (month != 'all') and (day != 'all'):
        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        print("The most common hour is {}".format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip based on \n')
    start_time = time.time()

    # display most commonly used start station
    most_pop_st_station = df['Start Station'].mode()[0]
    print("Most Start Common Station is "+most_pop_st_station+"\n")

    # display most commonly used end station
    most_pop_end_station = df['End Station'].mode()[0]
    print("Most End Common Station is "+most_pop_end_station+"\n")


    # display most frequent combination of start station and end station trip
    most_comb_station = df['Start Station'] + "--" + df['End Station']
    most_comb_station = most_comb_station.value_counts().idxmax()
    print('Most frequent combinations of Start and End Station are:\n{}\n{}'.format(most_comb_station.split('--')[0], most_comb_station.split('--')[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convertSeconds(seconds):
    w = seconds //(7*24*60*60)
    d = (seconds - w*7*24*60*60)//(24*60*60)
    h = (seconds - w*7*24*60*60 - d*24*60*60)//(60*60)
    m = (seconds - w*7*24*60*60 - d*24*60*60 - h*60*60)//60
    s = seconds - (w*7*24*60*60) - (d*24*60*60) - (h*60*60) - (m*60)
    return w, d, h, m, s

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print("Total trip Duration is {} \n".format(total_trip_duration))
    w, d, h, m, s = convertSeconds(total_trip_duration)
    print("Total trip Duration is {} weeks {} days {} hours , {} Minutes, and {} Seconds \n".format(w, d, h, m, s))



    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print("Mean trip Duration is {} \n".format(mean_trip_duration))

    w, d, h, m, s = convertSeconds(mean_trip_duration)
    print("Mean trip Duration is {} weeks {} days {} hours , {} Minutes, and {} Seconds \n".format(w, d, h, m, s))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'User Type' in df.columns:
        # Display counts of user types
        user_types_count = df['User Type'].value_counts()
        print("The count of user type are:\n{} \n".format(user_types_count))

    if 'Gender' in df.columns:
        # Display counts of gender
        user_gender_count = df['Gender'].value_counts()
        print("The count of user gender are: \n{} \n".format(user_gender_count))

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].max()
        most_recent_year = df['Birth Year'].min()
        common_birth_year = df['Birth Year'].mode()[0]
        print("The Earliest year o birth is {}, the most recent year of birth is {}, and the most common year of birth is {}".format(earliest_year, most_recent_year, common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        line_num = 0
        city,month,day,filter_type = get_filters()
        df = load_data(city,month,day)
        time_stats(df, city,month,day,filter_type)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            restart = input('\nWould you like to see more data. Please, answer with yes or no\n').lower()
            if restart == 'yes':
                print(df.iloc[line_num : line_num + 5])
                line_num += 5
            else:
                break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
