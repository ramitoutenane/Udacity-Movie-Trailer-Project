import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Movie Trailers</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">

     <!-- Import fonts from Google -->
    <link href="https://fonts.googleapis.com/css?family=Lobster|Oswald" rel="stylesheet">

     <!-- Import Css file  -->
    <link rel="stylesheet" media="screen" href="style.css">

    <!--javascript-->
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.trailer_boundary', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">

            <a class="navbar-brand" href="#">Movie Trailers</a>
            <a class="navbar-brand" href="readme.html">README</a>

          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center">
    <div class="trailer_boundary" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
        <img src="{poster_url}" alt="{movie_title}" width="220" height="342" class="poster-image">
        <h2 class="m_title">{movie_title}</h2>
        <h3 class="m_year">({release_year})</h3>
    </div>

    <span class="imdbRatingPlugin" data-user="ur93034947" data-title="{imdb_data_title}" data-style="p2">
        <a href="https://www.imdb.com/title/{imdb_data_title}/?ref_=plg_rt_1"><img src="https://ia.media-imdb.com/images/G/01/imdb/plugins/rating/images/imdb_38x18.png" alt=" {movie_title} ({release_year}) on IMDb" /></a>
    </span>
    <script>
        (function(d,s,id){{var js,stags=d.getElementsByTagName(s)[0];if(d.getElementById(id)){{return;}}js=d.createElement(s);js.id=id;js.src="https://ia.media-imdb.com/images/G/01/imdb/plugins/rating/js/rating.js";stags.parentNode.insertBefore(js,stags);}})(document,"script","imdb-rating-api");
    </script>


</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in

        content += movie_tile_content.format(
            movie_title=movie.movie_title,
            poster_url=movie.poster_url,
            trailer_youtube_id=trailer_youtube_id,
            release_year=movie.release_year,
            imdb_data_title=movie.imdb_data_title
        )
    return content

# readme.html content
readme_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>README</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">

  <!-- Import Css file  -->
  <link rel="stylesheet" media="screen" href="style.css">


</head>

  <body>

    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">

            <a class="navbar-brand" href="movie_trailers.html">Movie Trailers</a>
            <a class="navbar-brand" href="#">README</a>

          </div>
        </div>
      </div>
    </div>

   <!-- a converted copy of README.MD -->
    <div class="readme">

        <h1 id="project-1--movie-trailer-website.">Project #1 : Movie Trailer Website.</h1>
            <p>This project is intended to be delivered as part of <a href="https://mena.udacity.com/course/full-stack-web-developer-nanodegree--nd004">Udacity's Full Stack Developer Nanodegree Program</a> graduation requirements.</p>
            <p><strong>By : "Mohamed Rami" Toutenane</strong></p>

        <h2 id="project-overview">Project Overview</h2>
            <p>Website that allows visitors to browse movies and watch trailers generated using a python code which stores a list of movies, including it's <strong>poster , trailer URL , release year and imdb rating code.</strong></p>

        <h2 id="requirements">Requirements</h2>
            <p>Python  version 2.7.9 or higher.</p>

        <h2 id="download">Download</h2>
            <p>This project will be only available for project reviewing team,  through their submission page.</p>

        <h2 id="running-the-code-on-windows-os">Running the code on Windows OS</h2>
            <h3 id="using-python-shell">Using Python shell:</h3>
                <ul>
                    <li>Open your python shell</li>
                    <li>Select "Open" from "File" menu
                        <ul>
                            <li>you can also use the shortcut (Ctrl+O)</li>
                        </ul>
                    </li>
                    <li>Navigate to <strong>Project</strong> folder.</li>
                    <li>Select "entertainment_center.py"</li>
                    <li>Click on "open" button.
                        <ul>
                            <li>"entertainment_center.py" will open to you on the editor</li>
                        </ul>
                    </li>
                    <li>Select "Run Module" from "Run" menu
                        <ul>
                            <li>you can use the shortcut (Ctrl+O) (F5)</li>
                        </ul>
                    </li>
                    <li>Movie_trailers.html will be opened by your default web browser</li>
                    <li>Click on your favorite movie to watch it's trailer.</li>
                    <li>Click on <a href="https://www.imdb.com">IMDb</a> icon to open movie's page on imdb</li>
                    <li>Use the README button to visit readme.html</li>
                    <li>Use Movie Trailer button to go back to movie_trailers.html</li>
                </ul>
            <p><strong>Next time you can open the web-page only by double clicking on  (movie_trailers.html)</strong></p>

        <h2 id="extra-work">Extra Work</h2>
            <p><strong>Some of the work i have done above the minimal requirements:</strong></p>
            <ul>
                <li>
                    <p><strong>ratings.json:</strong></p>
                    <ul>
                        <li>created json file to store movie ratings html code from imdb because if it was added directly it would affect the readability of the code.</li>
                        <li>added all movie data to json file. (Udacity reviewer Note)</li>
                    </ul>
                </li>
                <li>
                    <p><strong>media.py:</strong></p>
                    <ul>
                        <li>added <strong>rerelease_year</strong> and <strong>imdb_data_title</strong> to be stored in the object</li>
                    </ul>
                </li>
                <li>
                    <p><strong>entertainment_center.py</strong>:</p>
                    <ul>
                        <li>read the data from json file to create Movie instances and store them in array using a for loop</li>
                    </ul>
                </li>

                <li>
                    <p><strong>edited_fresh_tomatoes.py:</strong></p>
                    <ul>
                        <li>edited the code to include the new data (year and rating)</li>
                        <li>edited the code to change html and css code</li>
                        <li>edited the code to create 2 extra files (readme.html , style.css)</li>
                    </ul>
                </li>
                <li>
                    <p><strong>HTML &amp; Css:</strong></p>
                    <ul>
                        <li>moved style to separate file (style.css) to improve the readability and to make it work with both pages</li>
                        <li>changed the original page style and look</li>
                        <li>included year and rating into page</li>
                        <li>created README page (the first page came to my mind)</li>
                        <li>linked two pages (Movie trailer and README)</li>
                    </ul>
                </li>
            </ul>

        <h2 id="references">References</h2>
            <ul>
                <li>
                    <p><strong>Python :</strong></p>
                    <ul>
                        <li><a href="https://classroom.udacity.com/nanodegrees/nd004-mena/parts/5d463571-1999-4e1d-adbb-dec1b3aa97e7">Udacity : Full Stack</a></li>
                        <li><a href="https://docs.python.org/2/index.html">Python 2.7.15 documentation</a></li>
                        <li><a href="https://github.com/udacity/ud036_StarterCode">fresh_tomatoes.py starter code</a></li>
                    </ul>
                </li>
                <li>
                    <p><strong>HTML &amp; Css:</strong></p>
                    <ul>
                        <li><a href="https://classroom.udacity.com/courses/ud001-track-1mac">Udacity : Front End</a></li>
                        <li><a href="https://github.com/udacity/ud036_StarterCode">fresh_tomatoes.py starter code </a></li>
                        <li><a href="https://www.w3schools.com/Css/">w3schools Css</a></li>
                        <li><a href="http://paletton.com/">Paletton color select</a></li>
                        <li><a href="https://mycolor.space/gradient">Gradient color generate</a></li>
                        <li><a href="https://fonts.google.com/">Google Fonts</a></li>
                    </ul>
                </li>
                <li>
                    <p><strong>JSON:</strong></p>
                    <ul>
                        <li><a href="http://www.json.org/">JSON</a></li>
                        <li><a href="https://docs.python.org/2/library/json.html">Python json</a></li>
                    </ul>
                </li>
                <li>
                    <p><strong>README:</strong></p>
                    <ul>
                        <li><a href="https://classroom.udacity.com/courses/ud777">Udacity : Writing READMEs</a></li>
                        <li><a href="https://stackedit.io/app#">Stackdit MD Editor and Convertor</a></li>
                    </ul>
                </li>
                <li>
                    <p><strong>Softwares:</strong></p>
                    <ul>
                        <li><a href="https://www.python.org/downloads/release/python-279/">Pyhton 2.7.9</a></li>
                        <li><a href="https://www.jetbrains.com/pycharm/download/#section=windows">JetBrains PyCharm </a></li>
                        <li><a href="https://www.sublimetext.com/3">Sublime Text 3</a></li>
                    </ul>
                </li>
                <li>
                    <p><strong>code style and check:</strong></p>
                    <ul>
                        <li><a href="https://google.github.io/styleguide/pyguide.html">Google Python Style Guide</a></li>
                        <li><a href="http://pep8online.com/">PEP8 Code Checker</a></li>
                        <li><a href="https://validator.w3.org/">HTML Validator</a></li>
                        <li><a href="https://jigsaw.w3.org/css-validator/">Css Validator</a></li>
                    </ul>
                </li>
                <li>
                    <p><strong>Movies :</strong></p>
                    <ul>
                        <li><a href="https://www.marvel.com/movies">Marvel Movies</a></li>
                        <li><a href="https://www.imdb.com/plugins">IMDb Ratings</a></li>
                        <li><a href="http://www.impawards.com/">IMP Awards Movie Posters</a></li>
                    </ul>
                </li>
                <li>
                    <p><strong>Udacity Reviewing Team</strong></p>
                </li>
            </ul>

        <h2 id="contact-information">Contact Information</h2>
            <p><strong>"Mohamed Rami" Toutenane<br>
            Email: <a href="mailto:Mhtoutenane119@cit.just.edu.jo">Mhtoutenane119@cit.just.edu.jo</a></strong></p>
    </div>
  </body>
</html>
  '''

# readme.html content
style_css_content = '''
        body {
            padding-top: 80px;
            padding-left: 20px;
            background-color: #0d0923;
        }

        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }

        #trailer-video {
            width: 100%;
            height: 100%;
        }

        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }

        .movie-tile {
            margin-bottom: 30px;
            padding-top: 30px;
        }

        .movie-tile:hover {
            background-image: linear-gradient(to bottom, #070f3f, #071043, #081147, #08124b, #09134f);
            cursor: pointer;
            border-radius: 40px;
        }

        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }

        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }

        .poster-image {
            border: 3px solid lightblue ;
            border-radius: 150px;
            box-shadow: -0.5em -0.5em 1em 1px black;
            transition : 1s;
        }

        .poster-image:hover {
            transform: scale(1.05);
            border-color: darkblue;
        }

        .navbar-brand {
            margin: 20px;
            border: 2px solid dodgerblue;
            box-shadow: 2px 2px 0 black;
            border-radius: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .navbar-brand:hover    {

            background-image: radial-gradient(circle, #291276, #291179, #2a107c, #2a0e7e, #2b0d81);
            border:3px solid #8A458A;
        }

        .navbar-inverse    {
            background-image: linear-gradient(to bottom, #070f3f, #071043, #081147, #08124b, #09134f);
        }

        .navbar-inverse .navbar-brand{
            color: white;
            text-shadow: 2px 2px 1px darkblue;
        }

        .m_title {
            color: white;
            font-style: italic;
        }

        .m_year    {
            color:#c0c0c0;
            margin-top: unset;
        }

        .m_title, .m_year {
            text-shadow: 2px 2px 2px #945764, -1px -1px 6px black;
            font-family: 'Lobster', 'Oswald', cursive;
        }

        .readme	{

            color: white;
        }

        .imdbRatingPlugin:hover	{
            cursor: default;
        }
'''


def open_movies_page(movies):
    # Create or overwrite the output files
    movie_trailers_page = open('movie_trailers.html', 'w')
    readme_page = open('readme.html', 'w')
    style_css_file = open('style.css', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    movie_trailers_page.write(main_page_head + rendered_content)
    movie_trailers_page.close()

    readme_page.write(readme_content)
    readme_page.close()

    style_css_file.write(style_css_content)
    style_css_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(movie_trailers_page.name)
    webbrowser.open('file://' + url, new=2)
