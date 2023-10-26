
import pickle            #for loading saved data
import streamlit as st   #create user interfaces /building web applications
import requests          #for making HTTP requests to fetch data 



# Store user credentials in a dictionary (for demonstration purposes)
user_credentials = {
    "Himasha": {"password": "1234"},
    "Nethmini": {"password": "9999"},
    "Ruvini": {"password": "7899"},
    "Udara": {"password": "5678"},
}


# fetch movie poster images for specific movies using their ID
# Store user credentials in a dictionary (for demonstration purposes)
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie, movies, similarity):
    # Find the index of the selected movie in the movies DataFrame
    index = movies[movies['title'] == movie].index[0]
    
    # Calculate the similarity scores between the selected movie and all other movies
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    # Initialize lists to store recommended movie names and posters
    recommended_movies_name = []
    recommended_movies_poster = []
    
    # Iterate through the sorted similarity scores to get recommendations
    for i in distance[1:6]:
        # Get the movie_id of the recommended movie
        movie_id = movies.iloc[i[0]].movie_id
        
        # Append the recommended movie name to the list
        recommended_movies_name.append(movies.iloc[i[0]].title)
        
        # Fetch the poster for the recommended movie using the fetch_poster function
        recommended_movies_poster.append(fetch_poster(movie_id))
    
    # Return the lists of recommended movie names and posters
    return recommended_movies_name, recommended_movies_poster



# Placeholder for the authenticate function
def authenticate(username, password):
    # Implement your authentication logic here
    # For example, check if the username and password match the stored credentials
    if username in user_credentials and user_credentials[username]["password"] == password:
        return True
    else:
        return False


# css for heading
st.markdown(
    """
    <style>
    .movie-header {
        font-size: 34px;
        color: #FF5733;  /* Change the color to your preference */
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background-color: #333333;  /* Change the background color to your preference */
        border-radius: 10px;
        margin-bottom: 20px;
        
    }
    </style>
    """,
    unsafe_allow_html=True
)

#Display the styled header
st.markdown("<h1 class='movie-header'>Movie Recommendation System</h1>", unsafe_allow_html=True)

# Load pickled artifacts
movies = pickle.load(open('artificats/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artificats/similarity.pkl', 'rb'))

#pickle = converting a Python object into a byte stream

#Simple login mechanism
def login():
    username = st.text_input("Username:", key="login_username")
    password = st.text_input("Password:", type="password", key="login_password")
    return username, password


# User registration function
def register(new_username, new_password):
    if new_username not in user_credentials:
        user_credentials[new_username] = {"password": new_password}
        st.success("Registration successful! You can now log in.")
    else:
        st.warning("Username already exists. Please choose a different username.")


#Main App
def main():
    st.header("Movie Recommendation System Using ML")
   
    #Display recommendations in columns
    for i in range(5):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(recommended_movie_posters[i], width=100)
        with col2:
            st.write(f"**<span style='font-size: 20px;'>{recommended_movie_names[i]}</span>**", unsafe_allow_html=True)



# App pages
def home():
    st.header("Welcome to the Movie Recommendation System")

if 'username' not in st.session_state:
    st.session_state.username = None

if st.session_state.username is None:
    username, password = login()
    
    if st.button("Login"):
        if authenticate(username, password):  # Assuming you have the authenticate function
            st.success("Login successful!")
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.warning("Invalid Login")

    if st.button("Register"):
        new_username, new_password = register()
        if st.button("Register"):
            register(new_username, new_password)
#This section handles session state and displays either 
#the login page or the recommendation page based on the user's login status.


else:
    # Recommendation page
    st.header(f"Welcome, {st.session_state.username}!")
    movie_list = movies['title'].values
    selected_movie = st.selectbox('Type or select a movie to get recommendations', movie_list)

    if st.button('Show Recommendations' , key='show_button'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)
        main()

    if st.button("Refresh"):
        st.session_state.logged_in = False

#These buttons trigger the display of movie recommendations and a refresh button to refresh the recommendations.
#The code has placeholders and assumptions (like the authenticate function) that need to be filled 
#in for a complete functioning app. You would need to implement the missing parts and customize 
# the app based on your requirements.


 