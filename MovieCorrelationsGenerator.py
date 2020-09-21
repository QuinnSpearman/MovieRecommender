#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import math

print("Starting...")

# Reads user ratings from a csv and stores in a dataframe
ratings = pd.read_csv("MovieData/ratings.csv")
# Drops the timestamp column
ratings.drop('timestamp', axis = 1, inplace = True)
# Reads movie data from a csv and stores in a dataframe
movies = pd.read_csv("MovieData/movies.csv")

# Reads user given tags from a csv and stores in a dataframe
tags = pd.read_csv("MovieData/tags.csv")
# Drops the timestamp and userId columns from the tags dataframe
tags.drop(columns = ['timestamp', 'userId'], inplace = True)
# Merges the movies and tags dataframes and stores in tags
tags = pd.merge(movies, tags)
# Index is set to the movie titles
tags.index = tags['title']
# Drops unnecessary columns from the tags dataframe
tags.drop(columns = ['movieId', 'genres', 'title'], inplace = True)
# Groups all of the tags together and stores in a groups dataframe
tagGroups = tags.groupby(tags.index)

# Merges the movies csv with the ratings csv
ratings = pd.merge(movies, ratings)
# Sets the index of the movies dataframe to the movie titles
movies.index = movies['title'] 
# drops the title and movieId columns from the movies dataframe
movies.drop('title', axis = 1, inplace = True)
movies.drop('movieId', axis = 1, inplace = True)

# Creates a new movieGenres dataframe with the columns title and genre
movieGenres = pd.DataFrame(columns = ['title', 'genres'])

print("Cleaning genre data")

# Loops through all of the movies and fill in the genre column with a list of each movie's genres
for movie in movies.index:
    genres = movies.at[movie, 'genres']
    
    genres = str(genres)

    genres = genres.split("|")

    movieGenres = movieGenres.append({'title': movie, 'genres': genres}, ignore_index = True)

# Sets the index of the movieGenres dataframe to the movie titles
movieGenres.index = movieGenres['title']
# Drops the movie title column
movieGenres.drop(columns = 'title', axis = 1, inplace = True)

# Creates a new table so that the userId is the index, the columns are the movies, and the values are the users' ratings
userRatings = ratings.pivot_table(index=['userId'], columns=['title'], values = 'rating')
userRatings

# Removes movies that don't have any tags from the userRatings dataframe
for movie in userRatings.columns:
    if movie not in tags.index:
        userRatings.drop(columns = [movie], inplace = True)
        
# Splits the data into a training set and a test set
train = userRatings[:int(.8 * len(userRatings))]
test = userRatings[int(.8 * len(userRatings)):]

print("Correlating matrix")

# Creates a correlated matrix with correlations between how users rated the same movies
correlatedMatrix = train.corr(method = 'spearman', min_periods = 10)
correlatedMatrix

print("Finished correlating matrix")

import math

print("Started loop")

# Loops through all movies in the correlated matrix
for i in correlatedMatrix.index:
    
    
    iTagList = []
    
    # Stores all tags for movie i in a list
    for tag in tagGroups.get_group(i)['tag']:
        iTagList.append(str(tag).lower())     
    
    # Loops through all movies in the correlated matrix
    for j in correlatedMatrix.index:
        
        # If movie i and movie j are the same movie, continue
        if i == j:
            continue
            
        # If the value at the indicated cell of the dataframe is NaN, continue
        if math.isnan(correlatedMatrix.at[i, j]):
            continue
            
        # Stores all tags for movie j in a list
        jTagList = []
        for tag in tagGroups.get_group(j)['tag']:
            jTagList.append(str(tag).lower())
            
        # Tracks how many of the tags in iTagList are also in jTagList
        similarTagCount1 = 0
        for tag in iTagList:
            if tag in jTagList:
                similarTagCount1 += 1
                
        # Tracks how many of the tags in jTagList are also in iTagList
        similarTagCount2 = 0
        for tag in jTagList:
            if tag in iTagList:
                similarTagCount2 += 1
                
        # Calculates the average similarity of the tags
        tagSimilarity1 = similarTagCount1 / max(len(iTagList), len(jTagList))
        tagSimilarity2 = similarTagCount2 / max(len(iTagList), len(jTagList))
        avgTagSimilarity = (tagSimilarity1 + tagSimilarity2) / 2
        
        # Calculates the genre correlation of two movies
        similarGenres = 0
        for iGenre in movieGenres.at[i, 'genres']:
            for jGenre in movieGenres.at[j, 'genres']:
                if iGenre == jGenre:
                    similarGenres += 1
        genreSimilarity = similarGenres / max(len(movieGenres.at[i, 'genres']), len(movieGenres.at[j, 'genres']))      
        
        # Calculates total similarity correlation
        totalSimilarity = (avgTagSimilarity + genreSimilarity) / 1.75
            
        # Multiplies the cell by the correlation rating calculated above
        correlatedMatrix.at[i, j] = totalSimilarity * correlatedMatrix.at[i, j]
        
# Copies correlation table into a csv
correlatedMatrix.to_csv('MovieData/CorrelatedMatrix.csv')


# In[ ]:




