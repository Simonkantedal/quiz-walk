import React, { useState } from 'react';
import axios from 'axios';

function SubmitResponse() {
    const [response, setResponse] = useState('');

    const question_id = 1;
    const user_id = "team_1";

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log("handleSubmit called");

        // Ensure the request payload includes all required data
        axios.post('/quiz-walk/api/response/responses/', {
            question_id: question_id,
            user_id: user_id,
            user_answer: response
        })
        .then(res => {
            console.log(res);
            console.log(res.data);
        })
        .catch(err => {
            console.error(err);
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Svar:
                <input type="text" value={response} onChange={e => setResponse(e.target.value)} />
            </label>
            <button type="submit">Svara</button>
        </form>
    );
}

export default SubmitResponse;