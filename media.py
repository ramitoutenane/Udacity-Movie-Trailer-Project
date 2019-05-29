class Movie():
    """class to save movie information

        Attributes:
            title: string of movie title
            poster: string of movie poster image url
            trailer: string of movie trailer youtube url
            year: string of release year
            imdb_id: string of imdb id for rating html code
    """

    def __init__(self, title, poster, trailer, year, imdb_id):
        self.movie_title = title
        self.poster_url = poster
        self.trailer_url = trailer
        self.release_year = year
        self.imdb_data_title = imdb_id
