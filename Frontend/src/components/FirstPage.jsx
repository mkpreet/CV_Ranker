import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./FirstPage.css";

const FirstPage = ({ saveWeights }) => {
  const navigate = useNavigate();
  const defaultWeights = { skills: 35, experience: 35, education: 30 };
  const [choice, setChoice] = useState(null); // Tracks if "Yes" or "No" is selected

  const handleChoice = (selectedChoice) => {
    setChoice(selectedChoice);
    if (selectedChoice === "yes") {
      navigate("/second"); // Directly redirect to second page on "Yes"
    }
  };

  const handleProceed = () => {
    if (choice === "no") {
      saveWeights(defaultWeights); // Save default weights
      navigate("/result"); // Redirect to result page
    }
  };

  return (
    <div className="first-page">
      <header className="first-header">
        <h1>Set Weightages</h1>
      </header>

      <div className="first-weightage-container">
        <div className="first-weightage-item">
          <span>Skills:</span>
          <div className="first-weight-box">{defaultWeights.skills}%</div>
        </div>
        <div className="first-weightage-item">
          <span>Work Experience:</span>
          <div className="first-weight-box">{defaultWeights.workExperience}%</div>
        </div>
        <div className="first-weightage-item">
          <span>Education:</span>
          <div className="first-weight-box">{defaultWeights.education}%</div>
        </div>
      </div>

      <p className="first-question">Do you want to adjust the weightages?</p>

      <div className="first-button-group">
        <button
          className={`first-choice-button ${choice === "no" ? "active" : ""}`}
          onClick={() => handleChoice("no")}
        >
          No
        </button>
        <button
          className={`first-choice-button ${choice === "yes" ? "active" : ""}`}
          onClick={() => handleChoice("yes")}
        >
          Yes
        </button>
      </div>

      {/* Show Proceed button only if "No" is selected */}
      {choice === "no" && (
        <button className="first-proceed-button" onClick={handleProceed}>
          Proceed
        </button>
      )}
    </div>
  );
};

export default FirstPage;
