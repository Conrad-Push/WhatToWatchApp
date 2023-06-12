import { useState } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function ScrapDataPanel(props) {
  const [filmsToScrap, setFilmsToScrap] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleScrapData = async (e) => {
    e.preventDefault();

    if (filmsToScrap) {
      setErrorMessage("");

      if (parseInt(filmsToScrap) < 1) {
        setErrorMessage("Films to scrap should be 1 or more");
        return;
      }

      if (parseInt(filmsToScrap) > 250) {
        setErrorMessage("Films to scrap should be 250 or less");
        return;
      }

      props.setLoading(true);

      try {
        const dataAmount = {
          data_amount: filmsToScrap,
        };

        const response = await axios.post(
          "/postgresql/database/data/scrap",
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
        setErrorMessage("Error while scrapping data");
        props.setLoading(false);
      }

      setFilmsToScrap("");
    } else {
      setErrorMessage("Please fill the required field");
    }
  };

  const handleFilmsToScrapChange = (event) => {
    setFilmsToScrap(event.target.value);
  };

  return (
    <div>
      <h1>Data scrapper</h1>
      <div className="box">
        <div className="db-details-card">
          <form className="card-content">
            <h2>Scrap data:</h2>
            <input
              type="number"
              placeholder="Films to scrap..."
              value={filmsToScrap}
              onChange={handleFilmsToScrapChange}
              required
            />
            {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
            <button className="scrapData-button" onClick={handleScrapData}>
              Scrap data
            </button>
          </form>
        </div>
      </div>
      <ToastContainer />
    </div>
  );
}

export default ScrapDataPanel;
