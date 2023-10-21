import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GenreSelection from './GenreSelection';
import MovieRating from './MovieRating';
import MovieRecommendation from "./MovieRecommendation";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<GenreSelection />} />
                <Route path="/rating" element={<MovieRating />} />
                <Route path="/recommendation" element={<MovieRecommendation />} />
            </Routes>
        </Router>
    );
}


export default App;
