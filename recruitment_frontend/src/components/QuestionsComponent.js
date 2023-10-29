import './QuestionsComponent.css'
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function QuestionsComponent({email,onNext}) {
    const [questions, setQuestions] = useState([]);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState({});

    useEffect(() => {
        axios.get('http://localhost:8000/api/random_questions/')
            .then(response => setQuestions(response.data));
    }, []);

    function handleAnswerChange(event) {
        const updatedAnswers = { ...answers };
        updatedAnswers[questions[currentQuestionIndex].id] = event.target.value;
        setAnswers(updatedAnswers);
    }

    function handleNext() {
        if (currentQuestionIndex === questions.length - 1) {
            handleSubmit();
        } else {
            setCurrentQuestionIndex(currentQuestionIndex + 1);
        }
    }

    function handleBack() {
        if (currentQuestionIndex > 0) {
            setCurrentQuestionIndex(currentQuestionIndex - 1);
        }
    }

    async function handleSubmit() {
        const payload = {
            answers:answers,
            email:email
        };
        console.log(payload);
        try {
            await axios.post('http://localhost:8000/api/save_answer/', payload);
            setCurrentQuestionIndex(0);  // Reset to the first question after submitting
            setAnswers({});  // Clear the answers
            alert('Your answers have been submitted!');
            onNext();
        } catch (error) {
            console.error("Error saving answers:", error);
            alert('There was an error submitting your answers. Please try again.');
        }
    }

    return (
        <div>
            <div key={questions[currentQuestionIndex]?.id}>
                <p>{questions[currentQuestionIndex]?.text}</p>
                {["option_1", "option_2", "option_3", "option_4"].map((option, index) => (
                    <div className="option-div" key={index}>
                        <input 
                            type="radio" 
                            id={`option-${index}`}
                            name={questions[currentQuestionIndex]?.id} 
                            value={questions[currentQuestionIndex]?.[option]} 
                            onChange={handleAnswerChange}
                            checked={answers[questions[currentQuestionIndex]?.id] === questions[currentQuestionIndex]?.[option]}
                        />
                        <label htmlFor={`option-${index}`}>{questions[currentQuestionIndex]?.[option]}</label>
                    </div>
                ))}
                <button onClick={handleBack} disabled={currentQuestionIndex === 0}>Back</button>
                <button onClick={handleNext} disabled={!answers[questions[currentQuestionIndex]?.id]}>
                    {currentQuestionIndex === questions.length - 1 ? 'Submit' : 'Next'}
                </button>
            </div>
        </div>
    );
}

export default QuestionsComponent;
