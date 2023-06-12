import { useState } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function GenerateDataPanel(props) {
  const [filmsToGenerate, setFilmsToGenerate] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleGenerateData = async (e) => {
    e.preventDefault();

    if (filmsToGenerate) {
      setErrorMessage("");

      if (parseInt(filmsToGenerate) < 1) {
        setErrorMessage("Films to generate should be 1 or more");
        return;
      }

      if (parseInt(filmsToGenerate) > 500000) {
        setErrorMessage("Films to generate should be 500 000 or less");
        return;
      }

      props.setLoading(true);

      try {
        const dataAmount = {
          data_amount: filmsToGenerate,
        };

        const response = await axios.post(
          "/postgresql/database/data/generate",
          dataAmount
        );

        if (response.status === 200) {
          const { message: mess, execution_time: execTime } = response.data;

          if (mess && execTime) {
            let infoText = `${mess} in ${execTime} second(s)`;

            toast.success(infoText, {
              position: toast.POSITION.BOTTOM_LEFT,
            });
          }
        }

        props.setLoading(false);
      } catch (error) {
        console.log(error);
        setErrorMessage("Error while generating data");
        props.setLoading(false);
      }

      setFilmsToGenerate("");
    } else {
      setErrorMessage("Please fill the required field");
    }
  };

  const handleFilmsToGenerateChange = (event) => {
    setFilmsToGenerate(event.target.value);
  };

  return (
    <div>
      <h1>Data generator</h1>
      <div className="box">
        <div className="db-details-card">
          <form className="card-content">
            <h2>Generate data:</h2>
            <input
              type="number"
              placeholder="Films to generate..."
              value={filmsToGenerate}
              onChange={handleFilmsToGenerateChange}
              required
            />
            {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
            <button
              className="generateData-button"
              onClick={handleGenerateData}
            >
              Generate data
            </button>
          </form>
        </div>
      </div>
      <ToastContainer />
    </div>
  );
}

export default GenerateDataPanel;
