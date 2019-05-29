import media
import edited_fresh_tomatoes
import json

with open("data.json", "r") as file_open:
    movies_data = json.load(file_open)

movies_list = []

for movie in movies_data:
    movies_list.append(media.Movie(movies_data[movie]["title"],
                                   movies_data[movie]["poster"],
                                   movies_data[movie]["trailer"],
                                   movies_data[movie]["year"],
                                   movies_data[movie]["imdb_data_title"]))


edited_fresh_tomatoes.open_movies_page(movies_list)
