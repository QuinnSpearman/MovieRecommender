# MovieRecommender

The Movie Correlations Generator uses the Pandas Data Analysis Library to find movie correlations between movies based on how similar users rated the same movies, as well as movie genre similarities and movie tag similarities. The generator saves these correlations to an excel spreadsheet. The movie recommender takes input in the form of a list of movies from the user (the movie names must be formatted in a very particular manner) and uses the spreadsheet of correlations to produce a Pandas Series of movies that the user will enjoy with 94% accuracy.
