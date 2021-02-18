# refactoring the code

import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city=input("Please enter a City name: ").strip().lower()
    while(city not in CITY_DATA.keys()):
        city=input("Please enter a City name: ").strip().lower()

    # get user input for month (all, january, february, ... , june)

    valid_input=["all" , "january" , "february" , "march" , "april" , "may" , "june" , "july" , "august" , "september" , "october" , "november" , "december"]
    month=input("Please enter a month: ").strip().lower()
    while(month not in valid_input):
       month=input("Please enter a month: ").strip().lower()
          
    # get user input for day of week (all, monday, tuesday, ... sunday)

    valid_days=["all" , "sunday" , "monday" , "tuesday" , "wednesday" , "thursday" , "friday" , "saturday"]
    day=input("Please enter a day: ").strip().lower()
    while(day not in valid_days):
        day=input("Please enter a day: ").strip().lower()
        
    print('-'*40)
    
    return city, month, day


def load_data(city, month, day):


    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df= pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
                months = ['january', 'february', 'march', 'april', 'may', 'june', "july", "august", "september", "october", "november", "december"]
                month = months.index(month) + 1

                df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month) 
    
    
    #////def[count]= def[start] + def[end]
    # display the most common day of week

    df['day'] = df['Start Time'].dt.day
    common_day = df['day'].mode()[0]
    print('Most Common Day Of Week:', common_day)

    # display the most common start hour


    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common_Start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', common_Start_station)
    
    # display most commonly used end station

    common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', common_end_station)

    # display most frequent combination of start station and end station trip

    freq_combination = df.groupby(['Start Station', 'End Station']).count()
    print('Most Frequent Combination Of Start & End Station: ', freq_combination)
    df['combination_start_end'] = (df['Start Station'] + ' - ' + df['End Station'])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel = df['Trip Duration'].sum()
    print ('Total Travel Time: ',(total_travel))
    
    # display mean travel time

    mean_travel = df['Trip Duration'].mean()
    print ('Mean Travel Time: ',(mean_travel))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print ("The count of user types is: ", (user_types))
    
    # Display counts of gender
    try:
        gender_count = df["Gender"].value_counts()
        print(' ' * 40)
        print ("The count of gender is: ", (gender_count))
    except:
        print('Counts of Each User Gender:\nSorry, no gender data available for {} City'.format(city.title()))
      
    # Display earliest, most recent, and most common year of birth
    try:
        m=df['Birth Year'].min()
        r=df['Birth Year'].max()
        c=df["Birth Year"].mode()
    
        print ("earliest year of birth: ",(m))
        print ("most recent year of birth: ", (r))
        print ("most common yesr of birth: ", (c))
    except:
        print('Counts of User Birth Year:\nSorry, no birth year data available for {} City'.format(city.title()))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    # Ask user if they want to see more lines.
    start_data = 0
    end_data = 5
    df_length = len(df.index)
    
    while start_data < df_length:
        raw_data = input("\nDo You Want to See Raw Data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':
            
            print("\nDisplaying only 5 rows of data.\n")
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break
                    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
