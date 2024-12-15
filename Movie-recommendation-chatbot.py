import pandas as pd
import random

# Load the dataset (replace with the correct path to your dataset)
movies_df = pd.read_excel(r'C:\Users\saran\OneDrive\Desktop\Mini-project\tamil_movie_dataset.xlsx')

# Clean the dataset (remove missing values in critical columns)
movies_df.dropna(subset=['MovieName', 'Genre', 'Rating', 'Director', 'Actor', 'Year'], inplace=True)

# Convert columns to appropriate types
movies_df['Rating'] = pd.to_numeric(movies_df['Rating'], errors='coerce')
movies_df['Year'] = pd.to_numeric(movies_df['Year'], errors='coerce')

# Function to recommend movies based on user input
def recommend_movies(user_input):
    user_input = user_input.lower()

    # If the user asks for a specific movie title
    if user_input in movies_df['MovieName'].str.lower().values:
        movie = movies_df[movies_df['MovieName'].str.lower() == user_input]
        genre = movie['Genre'].values[0]
        print(f"Here are some movies similar to '{movie['MovieName'].values[0]}':")

        # Recommend movies from the same genre
        recommendations = movies_df[movies_df['Genre'].str.lower() == genre.lower()]
        recommendations = recommendations.head(5)
        return recommendations[['MovieName', 'Genre', 'Rating', 'Director', 'Actor', 'Year']]

    # If the user asks for movies by year
    elif 'year' in user_input:
        try:
            year = int(user_input.replace('year', '').strip())
            recommendations = movies_df[movies_df['Year'] == year]
            if not recommendations.empty:
                return recommendations[['MovieName', 'Genre', 'Rating', 'Director', 'Actor', 'Year']]
            else:
                return "Sorry, no movies found for the year " + str(year)
        except ValueError:
            return "Sorry, I couldn't process the year input. Please make sure it's a valid year."

    # If the user asks for movies by genre
    elif 'genre' in user_input:
        genre_name = user_input.replace("genre", "").strip()
        recommendations = movies_df[movies_df['Genre'].str.contains(genre_name, case=False, na=False)]
        if not recommendations.empty:
            return recommendations[['MovieName', 'Genre', 'Rating', 'Director', 'Actor', 'Year']].head(5)
        else:
            return "Sorry, no movies found for the genre " + genre_name

    # If the user asks for movies by actor
    elif 'actor' in user_input:
        actor_name = user_input.replace("actor", "").strip()
        recommendations = movies_df[movies_df['Actor'].str.contains(actor_name, case=False, na=False)]
        if not recommendations.empty:
            return recommendations[['MovieName', 'Genre', 'Rating', 'Director', 'Actor', 'Year']].head(5)
        else:
            return "Sorry, no movies found for the actor " + actor_name

    # If the user asks for movies with a specific rating or higher
    elif 'rating' in user_input:
        # Check if the user is asking for movies with ratings 'below' a certain value
        if 'below' in user_input:
            try:
                rating_value = float(user_input.split()[-1])
                recommendations = movies_df[movies_df['Rating'] < rating_value]
                if not recommendations.empty:
                    return recommendations[['MovieName', 'Genre', 'Rating', 'Director', 'Actor', 'Year']].head(5)
                else:
                    return f"Sorry, no movies found with a rating below {rating_value}."
            except ValueError:
                return "Sorry, I couldn't process the rating input. Please provide a valid rating."

        # If the user asks for movies with a specific rating or higher
        else:
            try:
                rating_value = float(user_input.split()[-1])
                recommendations = movies_df[movies_df['Rating'] >= rating_value]
                if not recommendations.empty:
                    return recommendations[['MovieName', 'Genre', 'Rating', 'Director', 'Actor', 'Year']].head(5)
                else:
                    return f"Sorry, no movies found with a rating of {rating_value} or higher."
            except ValueError:
                return "Sorry, I couldn't process the rating input. Please provide a valid rating."

    # If the user provides random or invalid input
    else:
        return "Sorry, I couldn't find any recommendations for your input."

# Chatbot function to interact with the user
def chatbot():
    print("Hello! I am your Tamil Movie Recommendation Bot.")
    print("You can ask me for movie recommendations based on genre, actor, rating, year, or a specific movie!")
    print("Type 'exit' to quit the chatbot.")

    while True:
        user_input = input("You: ").strip().lower()

        if user_input == "exit":
            print("Goodbye! Have a great day!")
            break

        # Get recommendations
        recommendations = recommend_movies(user_input)

        # Display results
        if isinstance(recommendations, pd.DataFrame):
            print("\nRecommended Movies:")
            print(recommendations.to_string(index=False))
        else:
            print(recommendations)

# Run the chatbot
if __name__ == "__main__":
    chatbot()
