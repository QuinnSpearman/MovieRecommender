#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


def generate_recommendations(inputedRatings):
    
    recommendations = pd.Series()
    
    # Loops through all inputed ratings
    for i in inputedRatings.index:

        
        candidates = correlatedMatrix[i].dropna()
        
        # Sets the currRating to the rating being checked to the 49th power
        currRating = (float(inputedRatings.at[i, 'rating']))**49
        # Multiplies all of the candidate movie's correlations by the currRating
        candidates = candidates.map(lambda x: x * currRating)
        # Appends the new candidate ratings to the recommendations series
        recommendations = recommendations.append(candidates)
        
     
    # Sorts the recommendations series
    recommendations.sort_values(inplace = True, ascending = False)
    # Groups all ratings of every movie and sums them up
    recommendations = recommendations.groupby(recommendations.index).sum()
    # Sorts the values into ascending order
    recommendations.sort_values(inplace = True, ascending = False)

    # Removes movies that have already been rated by the user
    for i in inputedRatings.index:
        if i in recommendations:
            recommendations.drop(i, inplace = True) 
            
    
    minRating = recommendations.min()
    
    maxRating = recommendations.max()

    # Normalizes movie ratings 
    for i in range(len(recommendations)):
        recommendations[i] = (recommendations[i] / (maxRating) * 4.5) + 0.5
        
    return recommendations;


# In[2]:


# Retrieves correlations from csv file
correlatedMatrix = pd.read_csv("MovieData/CorrelatedMatrix.csv")
correlatedMatrix.index = correlatedMatrix['title']
correlatedMatrix.drop('title', axis = 1, inplace = True)


# In[ ]:


# Dataframe for storing the inputed ratings
inputedRatings = pd.DataFrame(columns = ['title', 'rating'])
    
print("Enter as many movies as you would like: ")
movieName = ""
movieRating = 0.0
while movieName != 'q':
    movieName = input("\nEnter Movie Name: ")
    if movieName == 'q':
        break
    movieRating = input("Enter a rating for " + movieName + ": ")

    newRow = {'title': movieName, 'rating': float(movieRating)}

    inputedRatings = inputedRatings.append(newRow, ignore_index = True)

inputedRatings.index = inputedRatings['title']
inputedRatings.drop('title', axis = 1, inplace = True)

movieRecommendations = generate_recommendations(inputedRatings)

quantRatedGoodOrHigher = 0
for k in movieRecommendations:
    if k >= 3.5:
        quantRatedGoodOrHigher += 1

#movieRecommendations = movieRecommendations.head(quantRatedGoodOrHigher)
if quantRatedGoodOrHigher < 5:
    topRatings = 5
elif quantRatedGoodOrHigher > 35:
    topRatings = 35
else:
    topRatings = quantRatedGoodOrHigher        
        
print(movieRecommendations.head(topRatings))


# In[ ]:




