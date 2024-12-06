import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./SecondPage.css";

const SecondPage = ({ saveWeights }) => {
  const navigate = useNavigate();

  const sectionsList = [
    "hardSkills",
    "experience",
    "education",
    "project",
    "courses",
    "certificates",
    "languages",
    "awards",
    "achievement",
    "internships",
    "researchPapers",
    "portfolio",
  ];

  const [sections, setSections] = useState(
    Object.fromEntries(
      sectionsList.map((section) => [
        section,
        ["hardSkills", "experience", "education"].includes(section),
      ])
    )
  );

  const [weights, setWeights] = useState(
    Object.fromEntries(
      sectionsList.map((section) => [
        section,
        ["hardSkills", "experience", "education"].includes(section) ? 0 : 0,
      ])
    )
  );

  const handleWeightChange = (key, value) => {
    const totalWeight =
      Object.values(weights).reduce((acc, val) => acc + val, 0) +
      value -
      (weights[key] || 0);

    if (totalWeight > 100) {
      alert("Total weightage cannot exceed 100%");
      return;
    }

    setWeights((prevWeights) => ({
      ...prevWeights,
      [key]: value,
    }));
  };

  const handleAddSection = (section) => {
    setSections({ ...sections, [section]: true });
  };

  const handleRemoveSection = (section) => {
    setSections({ ...sections, [section]: false });
    setWeights((prevWeights) => ({ ...prevWeights, [section]: 0 }));
  };

  const handleProceed = () => {
    const totalWeight = Object.values(weights).reduce((acc, val) => acc + val, 0);

    if (totalWeight !== 100) {
      alert("Total weightage must be exactly 100% to proceed.");
      return;
    }

    saveWeights(weights);
    navigate("/result");
  };

  const getSliderBackground = (value) => {
    return `linear-gradient(to right, #007bff ${value}%, #ddd ${value}%)`;
  };

  return (
    <div className="second-page">
      <header className="header">
        <h1>Adjust Weightages</h1>
      </header>

      <div className="section-buttons">
        {sectionsList
          .filter((section) => !sections[section])
          .map((section) => (
            <button
              key={section}
              className="add-button"
              onClick={() => handleAddSection(section)}
            >
              {section.charAt(0).toUpperCase() + section.slice(1)}
            </button>
          ))}
      </div>

      <div className="weightage-container">
        {Object.keys(sections)
          .filter((key) => sections[key])
          .map((key) => (
            <div className="weightage-item" key={key}>
              <label className="weightage-label">
                {key.charAt(0).toUpperCase() + key.slice(1)}:
              </label>
              <div className="weightage-box">{weights[key] || 0}%</div>
              <div className="slider-container">
                <input
                  type="range"
                  min="0"
                  max="100"
                  step="1"
                  value={weights[key] || 0}
                  onChange={(e) =>
                    handleWeightChange(key, Number(e.target.value))
                  }
                  className="weightage-slider"
                  style={{ background: getSliderBackground(weights[key] || 0) }}
                />
                <div className="slider-scale">
                  {Array.from({ length: 21 }, (_, i) => {
                    const scaleValue = i * 5;
                    const isMajor = scaleValue % 10 === 0;
                    return (
                      <div key={i} className="scale-mark">
                        <div
                          className="midline"
                          style={{
                            height: isMajor ? "10px" : "5px",
                            backgroundColor: isMajor ? "#333" : "#aaa",
                          }}
                        />
                        {isMajor && (
                          <span className="scale-label">{scaleValue}</span>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
              <button
                className="remove-button"
                onClick={() => handleRemoveSection(key)}
              >
                &ndash;
              </button>
            </div>
          ))}
      </div>

      <div className="total-weightage">
        <strong>Total Weightage:</strong>{" "}
        {Object.values(weights).reduce((acc, val) => acc + val, 0)}%
      </div>

      <button className="proceed-button" onClick={handleProceed}>
        Proceed
      </button>
    </div>
  );
};

export default SecondPage;
