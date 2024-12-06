import React, { useEffect, useState } from "react";
import "./ResultPage.css";

async function sendDataToColab(data) {
  const colabUrl = "http://127.0.0.1:5000/postdata"; // Replace with your ngrok URL

  try {
    const response = await fetch(colabUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const responseData = await response.json();
    console.log("Response from Backend:", responseData);

    return responseData;
  } catch (error) {
    console.error("Error sending data to backend:", error);
    return { error: error.message };
  }
}

const ResultPage = ({ weights }) => {
  const [responseData, setResponseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      setError(null); 
      try {
        const response = await sendDataToColab(weights);
        if (response.error) {
          throw new Error(response.error);
        }
        setResponseData(response);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [weights]);

  return (
    <div className="result-page">
      <header className="header">
        <h1>User Weightage Results</h1>
      </header>

      <table className="results-table">
        <thead>
          <tr>
            <th>Category</th>
            <th>Weightage (%)</th>
          </tr>
        </thead>
        <tbody>
          {Object.keys(weights)
            .filter((key) => weights[key] > 0) // Show only weightages greater than 0
            .map((key) => (
              <tr key={key}>
                <td>{key.charAt(0).toUpperCase() + key.slice(1)}</td>
                <td>{weights[key]}%</td>
              </tr>
            ))}
        </tbody>
      </table>


      {/* Show a message if no weightage is set */}
      {Object.keys(weights).every((key) => weights[key] === 0) && (
        <p style={{ textAlign: "center", color: "#777", marginTop: "20px" }}>
          No weightages have been assigned.
        </p>
      )}


       {/* Show loading message after weightage table and before response table */}
       {loading && <div className="loading-message">Please wait for the results...</div>}

      {/* Display error message if any */}
      {error && <div className="error-message">Error: {error}</div>}

      {/* Display the response table only if loading is complete and there's data */}
      {!loading && responseData && (
        <div className="response-section">
          <h2 className="response-header">CV RANKING</h2>
          <div className="scrollable-table-container">
            <table className="response-table">
              <thead>
                <tr>
                  <th>Applicant</th>
                  <th>Match Score</th>
                </tr>
              </thead>
              <tbody>
                {responseData.map(([Applicant, score], index) => (
                  <tr key={index}>
                    <td>{Applicant}</td>
                    <td>{score.toFixed(4)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
          </div>
        );
      };

export default ResultPage;





