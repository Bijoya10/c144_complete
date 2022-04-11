import ast
import pandas as pd



movies_data = pd.read_csv('final.csv')
all_movies = movies_data[1:]
#all_movies =all_movies.iloc[1: , :]
print(all_movies.iloc[0,27])

liked_movies = []
not_liked_movies = []
did_not_watch = []