import pyspark
from pyspark.sql import types
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col, date_format

# Replace with your bucket name.
bucket_name = 'gs://zoomcamp-446201-bucket'

# Set up Spark session with GCP connections.
spark = SparkSession.builder \
    .appName('zoomcamp') \
    .config('spark.jars.packages', 'com.google.cloud.spark:spark-3.3-bigquery:0.42.0') \
    .getOrCreate()

# Replace with appropriate reference based on your dataproc cluster.
spark.conf.set('temporaryGcsBucket', 'dataproc-temp-us-central1-388436263568-dwd4zhos')


# Schemas for the dataframes.
games_schema = types.StructType([
    types.StructField("gameId", types.IntegerType(), True),
    types.StructField("season", types.IntegerType(), True),
    types.StructField("week", types.IntegerType(), True),
    types.StructField("gameDate", types.StringType(), True)
])

player_play_schema = types.StructType([
    types.StructField("gameId", types.IntegerType(), True),
    types.StructField("playId", types.IntegerType(), True),
    types.StructField("nflId", types.IntegerType(), True),
    types.StructField("teamAbbr", types.StringType(), True),
    types.StructField("hadRushAttempt", types.IntegerType(), True),
    types.StructField("rushingYards", types.IntegerType(), True),
    types.StructField("hadDropback", types.IntegerType(), True),
    types.StructField("passingYards", types.IntegerType(), True),
    types.StructField("sackYardsAsOffense", types.IntegerType(), True)
])

players_schema = types.StructType([
    types.StructField("nflId", types.IntegerType(), True),
    types.StructField("height", types.StringType(), True),
    types.StructField("weight", types.IntegerType(), True),
    types.StructField("birthDate", types.StringType(), True),
    types.StructField("collegeName", types.StringType(), True),
    types.StructField("position", types.StringType(), True),
    types.StructField("displayName", types.StringType(), True)
])


# Read in the csv files from the GCS bucket to create games dataframe.
df_games = spark.read \
    .option("header", "true") \
    .schema(games_schema) \
    .csv(f'{bucket_name}/games.csv')

# Convert gameDate string to date and adjust format.
spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")
df_games = df_games.withColumn("gameDate", to_date(col("gameDate"), "MM/dd/yyyy"))
df_games = df_games.withColumn("gameDate", date_format(col("gameDate"), "yyyy-MM-dd"))

# Create parquet files in GCS.
df_games.write.parquet(f'{bucket_name}/pq/games/', mode='overwrite')
df_games = spark.read.parquet(f'{bucket_name}/pq/games/')


# Read in the csv files from the GCS bucket to create player_play dataframe.
df_player_play = spark.read \
    .option("header", "true") \
    .schema(player_play_schema) \
    .csv(f'{bucket_name}/player_play.csv')

# Partition data by gameId and playId and create parquet files in GCS.
df_player_play \
    .repartition(8, "gameId", "playId") \
    .write.parquet(f'{bucket_name}/pq/player_play/', mode='overwrite')

df_player_play = spark.read.parquet(f'{bucket_name}/pq/player_play/')


# Read in the csv files from the GCS bucket to create players dataframe.
df_players = spark.read \
    .option("header", "true") \
    .schema(players_schema) \
    .csv(f'{bucket_name}/players.csv')

# Convert birthDate string to date and confirm format.
df_players = df_players.withColumn("birthDate", to_date(col("birthDate"), "yyyy-MM-dd"))
df_players = df_players.withColumn("birthDate", date_format(col("birthDate"), "yyyy-MM-dd"))

# Create parquet files in GCS.
df_players.write.parquet(f'{bucket_name}/pq/players/', mode='overwrite')
df_players = spark.read.parquet(f'{bucket_name}/pq/players/')


# Create temp views of dataframes to run SQL query.
df_games.createOrReplaceTempView("games")
df_player_play.createOrReplaceTempView("player_play")
df_players.createOrReplaceTempView("players")


# SQL query to transform data to final state for visualization.
df_result = spark.sql("""

    WITH qb_stats AS (
        SELECT 
            g.gameId as game_id,
            g.week as game_week,
            p.nflId as player_id,
            q.displayName as player_name,
            CASE WHEN dateadd(year, datediff(year, q.birthDate, g.gameDate), q.birthdate) > g.gameDate
                    THEN datediff (year, q.birthDate, g.gameDate) - 1
                    ELSE datediff (year, q.birthDate, g.gameDate)
                END as player_age,
            SUM(p.rushingYards) as total_rushing_yards,
            SUM(p.passingYards) as total_passing_yards,
            SUM(p.sackYardsAsOffense) as total_sack_yards
        FROM
            games g
        INNER JOIN player_play p ON g.gameId = p.gameId
        INNER JOIN players q on p.nflId = q.nflId
        WHERE
            q.position = 'QB'
        GROUP BY
            1, 2, 3, 4, 5
    )
                      
    SELECT
        game_week,
        player_name,
        player_age,
        (total_rushing_yards + total_passing_yards + total_sack_yards) as total_offensive_yards
    FROM qb_stats
    WHERE player_age IS NOT NULL
    ORDER BY game_week ASC, total_offensive_yards DESC
    
""")


# Write table to BigQuery.
df_result.write \
    .format("bigquery") \
    .option("table", "zoomcamp.total_qb_offense") \
    .mode("overwrite") \
    .save()
