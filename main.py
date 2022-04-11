from flask import Flask, jsonify, request

from storage import all_movies, liked_movies, not_liked_movies, did_not_watch
from demographic_filtering import output
from content_filtering import get_recommendations

_d = {
        "title": all_movies.iloc[0,19],
        "poster_link": all_movies.iloc[0,27],
        "release_date": all_movies.iloc[0,13] or "N/A",
        "duration": all_movies.iloc[0,15],
        "rating": int(all_movies.iloc[0,20]/2)
}
app = Flask(__name__)

@app.route("/movies")
def get_movie():
    global _d,all_movies
    return jsonify({
        "data": _d,
        "status": "success"
    })

@app.route("/like", methods=["POST"])
def liked_movie():
    global all_movies
    global liked_movies
    global _d
    liked_movies.append(_d)
    print(liked_movies)
    print(all_movies)
    all_movies=all_movies.iloc[1: , :]
    all_movies=all_movies.reset_index()
    print(all_movies)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/dislike", methods=["POST"])
def unliked_movie():
    global all_movies
    global _d
    not_liked_movies.append(_d)
    all_movies=all_movies.iloc[1: , :]
    return jsonify({
        "status": "success"
    }), 201

@app.route('/liked' , methods = ['GET'])
def liked():
    global liked_movies
    response = {'data' : liked_movies , 'status' : 'success'}
    return jsonify(response) , 201
  


# @app.route("/did_not_watch", methods=["POST"])
# def did_not_watch_view():
#     movie = all_movies[0]
#     did_not_watch.append(movie)
#     all_movies.pop(0)
#     return jsonify({
#         "status": "success"
#     }), 201

@app.route("/popular_movies")
def popular_movies():
    movie_data = []
    for movie in output:
        _p = {
            "title": movie[0],
            "poster_link": movie[1],
            "release_date": movie[2] or "N/A",
            "duration": movie[3],
            "rating": movie[4]
        }
        movie_data.append(_p)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200

@app.route("/recommended_movies")
def recommended_movies():
    global liked_movies
    all_recommended = []
    print(liked_movies)
    for liked_movie in liked_movies:
        output = get_recommendations(liked_movie[8])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    movie_data = []
    for recommended in all_recommended:
        _p = {
            "title": recommended[0],
            "poster_link": recommended[1],
            "release_date": recommended[2] or "N/A",
            "duration": recommended[3],
            "rating": recommended[4]
        }
        movie_data.append(_p)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200

if __name__ == "__main__":
  app.run()