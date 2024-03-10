import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Questions() {
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const [currentQuestionId, setCurrentQuestionId] = useState(1); // Start from the first question

    useEffect(() => {
        fetchQuestion();
    }, [currentQuestionId]);

    const fetchQuestion = () => {
        axios.get(`/quiz-walk/api/question/questions/${currentQuestionId}`)
            .then(response => {
                setCurrentQuestion(response.data);
            })
            .catch(error => console.error('Error fetching question:', error));
    };

    const handleSubmit = (userAnswer) => {
        axios.post('/quiz-walk/api/question/submit-response/', {
            questionId: currentQuestionId,
            userAnswer
        })
        .then(response => {
            // Handle submission feedback here
            // Assume the next question's ID is the current ID + 1
            setCurrentQuestionId(currentQuestionId + 1);
        })
        .catch(error => console.error('Error submitting answer:', error));
    };

    // Check if the currentQuestion is loaded
    if (!currentQuestion) return <div>Loading question...</div>;

    return (
        <div>
            <h1>{currentQuestion.question_text}</h1>
            <form onSubmit={(e) => e.preventDefault()}>
                <input type="text" id="userAnswer" />
                <button onClick={() => handleSubmit(document.getElementById('userAnswer').value)}>Submit</button>
            </form>
        </div>
    );
}

export default Questions;