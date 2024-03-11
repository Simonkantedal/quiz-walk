const app = new Vue({
    el: '#app',
    data: {
        teamName: '',
        teamCreated: false,
        currentQuestionText: 'What is the capital of France?',
        userResponse: '',
        quizFinished: false
    },
    methods: {
        createTeam: function() {
            fetch('http://127.0.0.1:8000/quiz-walk/api/teams/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ team_name: this.teamName }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Team created:', data);
                this.teamCreated = true;
                this.fetchQuestion(); // Invoke fetchQuestion to fetch the first question when a team is created
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        },
        fetchQuestion: function() {
            fetch('http://127.0.0.1:8000/quiz-walk/api/questions/')
            .then(response => response.json())
            .then(data => {
                console.log('Question fetched:', data);
                // Assuming response data contains questions, adapt the next line to match the response structure
                this.currentQuestionText = data.questionText; // Update the placeholder with actual data properties
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        },
        submitResponse: function() {
            fetch('http://127.0.0.1:8000/quiz-walk/api/responses/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question_id: this.currentQuestionId,  // Ensure you manage state for current question ID
                    user_id: this.userId,  // And user/team ID
                    user_answer: this.userResponse,
                }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Response submitted:', data);
                // After submitting, you can fetch the next question or handle quiz end
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        },
    }
});