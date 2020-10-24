import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read_file(open('dl.cfg'))


os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    
    """ 
    This function loads song_data from S3 and processes it by extracting the songs and artist tables and then again loaded back to S3
    """
    # get filepath to song data file...
    song_data = input_data + 'song_data/*/*/*/*.json'
      
    # read song data file..
    df = spark.read.json(song_data)

    # extract columns to create songs table..
    songs_table = df['song_id', 'title', 'artist_id', 'year', 'duration']
    songs_table = songs_table.dropDuplicates(['song_id'])
    
    # songs table to parquet files partitioned by year and artist..
    songs_table.write.partitionBy('year', 'artist_id').parquet(os.path.join(output_data, 'songs.parquet'), 'overwrite')

    # extract columns to create artists table..
    artists_table = df['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']
    artists_table = artists_table.dropDuplicates(['artist_id'])
    
    
    # write artists table to parquet files..
    artists_table.write.parquet(os.path.join(output_data, 'artists.parquet'), 'overwrite')


def process_log_data(spark, input_data, output_data):
    
    """
    This function loads log_data from S3 and processes it by extracting the songs and artist tables and then again loaded back to S3. 
    """ 
     
    # getting filepath to log data file
    log_data = input_data + 'log_data/*/*/*.json'
    
    # reading log data file
    df = spark.read.json(log_data)
    
    # filtering by actions for song plays
    songplays_table = df['ts', 'userId', 'level','sessionId', 'location', 'userAgent']
    
    # extracting columns for users table    
    users_table = df['userId', 'firstName', 'lastName', 'gender', 'level']
    users_table = users_table.dropDuplicates(['userId'])
    
    # users table to parquet files
    users_table.write.parquet(os.path.join(output_data, 'users.parquet'), 'overwrite')
    

    # creating timestamp column from original timestamp column
    get_timestamp = udf(lambda x: str(int(int(x)/1000)))
    df = df.withColumn('timestamp', get_timestamp(df.ts))
    
    # creating datetime column from original timestamp column
    get_datetime = udf(lambda x: str(datetime.fromtimestamp(int(x) / 1000.0)))
    df = df.withColumn("datetime", get_datetime(df.ts))
    
    # extracting columns to create time table
    time_table = df.select(
        col('datetime').alias('start_time'),
        hour('datetime').alias('hour'),
        dayofmonth('datetime').alias('day'),
        weekofyear('datetime').alias('week'),
        month('datetime').alias('month'),
        year('datetime').alias('year') 
   )
    time_table = time_table.dropDuplicates(['start_time'])
    
    # time table to parquet files partitioned by year and month
    time_table.write.partitionBy('year', 'month').parquet(os.path.join(output_data, 'time.parquet'), 'overwrite')
    

    # reading in song data to use for songplays table
    #song_data = os.path.join(input_data, "song_data/*/*/*/*.json")
    song_data = input_data + 'song_data/*/*/*/*.json'
    #song_data = os.path.join("/home/workspace/","data/song_data/A/A/A/*.json")
    song_df = spark.read.json(song_data)
    
    # extract columns from joined song and log datasets to create songplays table 
    df = df.join(song_df, song_df.title == df.song)
    
    songplays_table = df.select(
        col('ts').alias('ts'),
        col('userId').alias('user_id'),
        col('level').alias('level'),
        col('song_id').alias('song_id'),
        col('artist_id').alias('artist_id'),
        col('ssessionId').alias('session_id'),
        col('location').alias('location'),
        col('userAgent').alias('user_agent'),
        col('year').alias('year'),
        month('datetime').alias('month')
    )
    
    songplays_table = songplays_table.selectExpr("ts as start_time")
    songplays_table.select(monotonically_increasing_id().alias('songplay_id')).collect()
    
    # songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy('year', 'month').parquet(os.path.join(output_data, 'songplays.parquet'), 'overwrite')


def main():
   
    # Extracting songs and events data from S3, Transform it into thedimensional table
    # Load it back to S3 in Parquet format
   
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-dend/"
    #First Function
    process_song_data(spark, input_data, output_data)  
    #Second Function
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()