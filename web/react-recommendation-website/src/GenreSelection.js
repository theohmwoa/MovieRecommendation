import React, { useState } from 'react';
import styled from '@emotion/styled';
import { useNavigate } from 'react-router-dom';

const YearInputContainer = styled.div`
  margin-bottom: 20px;
  color: white;
`;

const StyledInput = styled.input`
    background-color: #444;
    border: 1px solid white;
    border-radius: 4px;
    color: white;
    margin-left: 10px;
    padding: 5px 10px;
    ::placeholder {
        color: rgba(255, 255, 255, 0.5);  // Light white placeholder text
    }
`;


const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #282c34;
`;

const CardContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;  /* Spacing between cards */
  justify-content: center;
  width: max-content;  /* Ensure container fits the content */
`;


const GenreCard = styled.div`
  width: 150px;
  height: 150px;
  border: 1px solid white;
  padding: 10px;
  margin: 10px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: ${props => (props.selected ? '#444' : 'transparent')};
`;


const GenreImage = styled.img`
  max-width: 100%;
  max-height: 100%;
`;

const GenreSelection = () => {
    const genres = [
        { name: 'Comedy', image: 'icons8-comedy-100.png' },
        { name: 'Horror', image: 'icons8-horror-100.png' },
        { name: 'Sci-Fi', image: 'icons8-sci-fi-100.png' },
        { name: 'Drama', image: 'icons8-drama-100.png' },
        { name: 'Adventure', image: 'icons8-adventure-100.png' },
        { name: 'Animation', image: 'icons8-animation-100.png' },
        { name: 'Children', image: 'icons8-children-100.png' },
        { name: 'Crime', image: 'icons8-crime-100.png' },
        { name: 'Documentary', image: 'icons8-documentary-100.png' },
        { name: 'Film-Noir', image: 'icons8-film-noir-100.png' },
        { name: 'Musical', image: 'icons8-musical-100.png' },
        { name: 'Romance', image: 'icons8-romance-100.png' },
        { name: 'Thriller', image: 'icons8-thriller-100.png' },
        { name: 'War', image: 'icons8-war-100.png' },
        { name: 'Western', image: 'icons8-western-100.png' },
    ];
    const [selectedGenres, setSelectedGenres] = useState([]);

    const [yearLimit, setYearLimit] = useState("2000");

    const navigate = useNavigate();
    const handleSelect = (genre) => {
        setSelectedGenres((prev) =>
            prev.includes(genre.name) ? prev.filter((g) => g !== genre.name) : [...prev, genre.name]
        );
    };

    const handleNext = () => {
        navigate('/rating', { state: { selectedGenres, yearLimit } });
    }

    return (
        <Container>
            <YearInputContainer>
                <label>
                    Only show films from after the year:
                    <StyledInput
                        type="number"
                        placeholder="e.g., 2015"
                        value={yearLimit}
                        onChange={(e) => setYearLimit(e.target.value)}
                    />
                </label>
            </YearInputContainer>

            <CardContainer>
                {genres.map((genre) => (
                    <GenreCard
                        key={genre.name}
                        selected={selectedGenres.includes(genre.name)}
                        onClick={() => handleSelect(genre)}
                    >
                        <GenreImage src={process.env.PUBLIC_URL + '/' + genre.image} alt={genre.name} />
                        <div>{genre.name}</div>
                    </GenreCard>
                ))}
            </CardContainer>
            <button onClick={handleNext}>Next</button>
        </Container>
    );
};

export default GenreSelection;
