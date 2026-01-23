
// Quiz Engine
class QuizEngine {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.score = 0;
        this.total = 0;
    }
    
    checkAnswer(questionId, selected, correct) {
        this.total++;
        const feedback = document.querySelector(`#${questionId} .feedback`);
        
        if (selected === correct) {
            this.score++;
            feedback.className = 'feedback correct';
            feedback.textContent = '✓ Correct!';
        } else {
            feedback.className = 'feedback incorrect';
            feedback.textContent = '✗ Incorrect. Try again!';
        }
        feedback.style.display = 'block';
    }
    
    showResults() {
        const percent = Math.round((this.score / this.total) * 100);
        alert(`Your score: ${this.score}/${this.total} (${percent}%)`);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.quiz = new QuizEngine('quiz-container');
    
    // Add click handlers to all options
    document.querySelectorAll('.options input').forEach(input => {
        input.addEventListener('change', (e) => {
            const question = e.target.closest('.question');
            const correct = parseInt(question.dataset.correct);
            const selected = parseInt(e.target.value);
            window.quiz.checkAnswer(question.id, selected, correct);
        });
    });
});
