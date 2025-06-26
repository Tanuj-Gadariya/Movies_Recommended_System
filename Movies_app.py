import streamlit as st
import pickle
import pandas as pd
import requests





def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster=[]
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

similarity=pickle.load(open('similarity.pkl', 'rb'))

movies_dict1=pickle.load(open('movies_dict1.pkl', 'rb'))
movies=pd.DataFrame(movies_dict1)

st.title('Movie Recommender System')


Selected_movie_Name = st.selectbox(
'Would you like to see a movie recommendation?',
movies['title'].values)

if st.button('Get Movie Recommendation'):
    Names,Posters=recommend(Selected_movie_Name)

    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(Names[0])
        st.image(Posters[0])
    with col2:
        st.text(Names[1])
        st.image(Posters[1])
    with col3:
        st.text(Names[2])
        st.image(Posters[2])
    with col4:
        st.text(Names[3])
        st.image(Posters[3])
    with col5:
        st.text(Names[4])
        st.image(Posters[4])