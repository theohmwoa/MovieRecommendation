import React, { useEffect, useState } from 'react';
import styled from '@emotion/styled';
import { useNavigate, useLocation } from 'react-router-dom';

const RecommendationContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #282c34;
`;

const RecommendationTitle = styled.h1`
  color: white;
  margin-bottom: 20px;
`;

const MoviePoster = styled.img`
  max-width: 300px;
  margin: 20px 0;
`;

const fetchRecommendation = async (selectedGenres, yearLimit, ratingList, setRecommendedMovie) => {
    const data = {
        genres: selectedGenres,
        start_date: yearLimit,
        user_rated_movies: ratingList
    };

    try {
        const response = await fetch("http://localhost:5000/recommend_movie", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        console.log(result);
        setRecommendedMovie(result);
    } catch (error) {
        console.error("Error fetching recommendation:", error);
    }
};

const MovieRecommendation = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const [recommendedMovie, setRecommendedMovie] = useState(null);

    const { selectedGenres, yearLimit, ratingList } = location.state;

    useEffect(() => {
        fetchRecommendation(selectedGenres, yearLimit, ratingList, setRecommendedMovie);
    }, [selectedGenres, yearLimit, ratingList]);

    if (!recommendedMovie) return <RecommendationContainer>Loading...</RecommendationContainer>;

    return (
        <RecommendationContainer>
            <RecommendationTitle>Hello, this is the film we recommend you should watch:</RecommendationTitle>
            <MoviePoster src={recommendedMovie.poster} alt={recommendedMovie.title} />
            <h2 style={{color: 'white'}}>{recommendedMovie.title}</h2>
        </RecommendationContainer>
    );
};

export default MovieRecommendation;
