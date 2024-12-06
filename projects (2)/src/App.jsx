import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FirstPage from "./components/FirstPage";
import SecondPage from "./components/SecondPage";
import ResultPage from "./components/ResultPage";

function App() {
  const [weights, setWeights] = useState({});

  const saveWeights = (newWeights) => {
    setWeights(newWeights);
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<FirstPage saveWeights={saveWeights} />} />
        <Route path="/second" element={<SecondPage saveWeights={saveWeights} />} />
        <Route path="/result" element={<ResultPage weights={weights} />} />
      </Routes>
    </Router>
  );
}

export default App;
