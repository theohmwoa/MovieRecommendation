import React, {useEffect, useState} from 'react';
import styled from '@emotion/styled';
import { useNavigate, useLocation } from 'react-router-dom';

const RatingContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #282c34;
`;

const StyledButton = styled.button`
  background-color: #444;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  margin: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #666;
  }

  &:active {
    transform: scale(0.98);
  }

  width: 150px; 
  text-align: center;
`;

const ButtonContainer = styled.div`
  display: flex;
  gap: 20px;
  margin-top: 20px;
`;


const MovieTitle = styled.h1`
  color: white;
`;

const MoviePoster = styled.img`
  max-width: 300px;
  margin: 20px 0;
`;

const StarsContainer = styled.div`
  display: flex;
  gap: 10px;
  margin: 20px 0;
`;

const Star = styled.span`
  font-size: 24px;
  cursor: pointer;
  color: ${props => props.active ? 'yellow' : 'white'};
`;

const fetchData = async (selectedGenres, yearLimit, ratingList, setMovie) => {
    const data = {
        genres: selectedGenres,
        start_date: yearLimit,
        user_rated_movies: ratingList
    };

    console.log(data);

    try {
        const response = await fetch("http://localhost:5000/next_movie_to_rate",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });
        const result = await response.json();
        console.log(result);
        setMovie(result);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
};

const MovieRating = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const [rating, setRating] = useState(0);

    const [ratingList, setRatingList] = useState([]);

    const { selectedGenres, yearLimit} = location.state;

    const [movie, setMovie] = useState({
        movieId: 124747,
        title: "The Incredible Adventures of Marco Polo (1998)",
        genre: "Adventure",
        poster: "https://image.tmdb.org/t/p/w500/l2nZz19b48LXC5g9FvaoH03pC3B.jpg"
    });



    useEffect(() => {
        fetchData(selectedGenres, yearLimit, ratingList, setMovie);
    }, [ratingList, selectedGenres, yearLimit, setMovie]);

    const handleRating = (value) => {
        setRating(value);
    };

    const rateMore = () => {
        setRatingList(prevRatingList => [...prevRatingList, {movieId: movie.movieId, rating: rating}]);
        fetchData(selectedGenres, yearLimit, ratingList, setMovie);
        setRating(0)
    }

    const skipMovie = () => {
        setRatingList(prevRatingList => [...prevRatingList, {movieId: movie.movieId, rating: -1}]);
        fetchData(selectedGenres, yearLimit, ratingList, setMovie);
        setRating(0)
    }

    const getReccomendation = (navigate, selectedGenres, yearLimit, ratingList) => {
        navigate('/recommendation', { state: { selectedGenres, yearLimit, ratingList } });
    }

    return (
        <RatingContainer>
            <MovieTitle>{movie.title}</MovieTitle>
            <MoviePoster src={movie.poster} alt={movie.title} />
            <StarsContainer>
                {[...Array(10)].map((_, index) => (
                    <Star
                        key={index}
                        active={index < rating}
                        onClick={() => handleRating(index + 1)}
                    >
                        ★
                    </Star>
                ))}
            </StarsContainer>
            <ButtonContainer>
                <StyledButton onClick={() => rateMore()}>Rate More</StyledButton>
                <StyledButton onClick={() => skipMovie()}>Skip Movie</StyledButton>
                <StyledButton onClick={() => getReccomendation(navigate, selectedGenres, yearLimit, ratingList)}>Get My Movie</StyledButton>
            </ButtonContainer>
        </RatingContainer>
    );
};

export default MovieRating;
