import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    while True:
        city = input("Please Enter a city to analyse(Chicago, new york, Washington): ").lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("Invalid city name. Select from: --> Chicago, New York or Washington")


    # get user input for month (all, january, february, ... , june)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    while True:
        month = input("Please pick a month of interest(January,February,March,April,May,June,All): ").title()
        if month in months:
            break
        else:
            print("Invalid input. Select from: --> (January,February,March,April,May,June,All)")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "All"]
    while True:
        day = input("Please pick a day of interest: ").title()
        if day in days:
            break
        else:
            print("Invalid input. Kindly input a valid day of the week(sunday, monday, etc..)")

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
    # Load data as a dataframe of specified city
    df = pd.read_csv(CITY_DATA[city])

    # Convert 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week and hour from 'Start Time'
    df['month'] = df['Start Time'].dt.strftime('%B').str.title()
    df['day'] = df['Start Time'].dt.strftime('%A').str.title()
    df['hour'] = df['Start Time'].dt.hour
    
    #  Filter by month and create new DataFrame
    if month != 'All':           
        df = df[df['month'] == month]

    # Filter by day of week and create new DataFrame
    if day != 'All':
        df = df[df['day'] == day]

    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()   
       
    # display the most common month    
    popular_month =  df['month'].mode()[0]
    print("The most common month is:\n ", popular_month)   
    

    # display the most common day of week
    popular_day = df['day'].mode()[0]
    print("The most common day of the week is:\n ", popular_day)

    # display the most common start hour    
    popular_hour = df['hour'].mode()[0]
    print("The most common start hour is:\n ", popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_startS = df['Start Station'].mode()[0]
    print('The most commonly used start station is:\n ',popular_startS )

    # display most commonly used end station
    popular_endS = df['End Station'].mode()[0]
    print('The most commonly used end station is:\n ', popular_endS )

    # display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most frequent combination of start and end station is:\n ',popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time is:\n ", total_travel_time)

    # display mean travel time
    mean_tt = df['Trip Duration'].mean()
    print("The mean travel time is:\n ", mean_tt)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print('Here\'s the breakdown of user types available:\n ', user_types)

    # Display counts of gender
    try:
        gender = df["Gender"].value_counts()
        print("Here's the gender distribution:\n ", gender)
    except:
        print("This city does not have a Gender column")

    # Display earliest, most recent, and most common year of birth

    try:
        print("The earliest year of birth is:\n :", df['Birth Year'].min())
        print("The most recent year of birth is:\n :", df['Birth Year'].max())
        print("The most common year of birth is:\n :", df['Birth Year'].mode()[0])
        
    except:
        print("This city does not have a Birth Year column")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



    # Ask user if they want to see a preview of the data
def preview_data(df):
    
    i = 0
    
    data = input("Would you like to view first five rows of data?(Y/N):\n ").upper()
    while True:      
        i += 1            
        print(df.iloc[(i-1)*5 : i*5])
        
        data = input("Would you like to view the next five rows?(Y/N):\n ").upper()
        if  (data != 'Y') or ((i-1) >= df.shape[0]):
            return 

        
               
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        preview_data(df)

                

        restart = input('\nWould you like to restart? Enter Y/N .\n')
        if restart.upper() != 'Y':
            break
    


if __name__ == "__main__":
	main()
