import React from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function DatabaseDetails(props) {
  const capitalize = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
  };

  const handleReload = async (e) => {
    e.preventDefault();
    props.setLoading(true);

    try {
      const response = await axios.get("/postgresql/database/status");

      if (response.status === 200) {
        const {
          message: mess,
          db_state: newDBState,
          tables_details: newTablesDetails,
          execution_time: execTime,
        } = response.data;

        props.setDBState(newDBState);
        props.setTablesDetails(newTablesDetails);

        if (mess && execTime) {
          let infoText = `${mess} in ${execTime} second(s)`;

          toast.info(infoText, {
            position: toast.POSITION.BOTTOM_LEFT,
          });
        }
      }

      props.setLoading(false);
    } catch (error) {
      console.log(error);

      let errorText = "Error while checking the database status";
      toast.error(errorText, {
        position: toast.POSITION.BOTTOM_LEFT,
      });
      props.setLoading(false);
    }
  };

  const handleRestartTables = async (e) => {
    e.preventDefault();
    props.setLoading(true);

    try {
      const response = await axios.get("/postgresql/database/tables/restart");

      if (response.status === 200) {
        const {
          message: mess,
          db_state: newDBState,
          tables_details: newTablesDetails,
          execution_time: execTime,
        } = response.data;

        props.setDBState(newDBState);
        props.setTablesDetails(newTablesDetails);

        if (mess && execTime) {
          let infoText = `${mess} in ${execTime} second(s)`;

          toast.warning(infoText, {
            position: toast.POSITION.BOTTOM_LEFT,
          });
        }
      }

      props.setLoading(false);
    } catch (error) {
      console.log(error);

      let errorText = "Error while restarting the tables";
      toast.error(errorText, {
        position: toast.POSITION.BOTTOM_LEFT,
      });

      props.setLoading(false);
    }
  };

  return (
    <div>
      <h1>Details</h1>
      <div className="box">
        <div className="db-details-card">
          <div className="card-content">
            <h2>Tables:</h2>
            <ul className="table-list">
              {props.details.map((table) => (
                <li key={table.name}>
                  <div className="table-info">
                    <span className="table-name">
                      {capitalize(table.name)}:{" "}
                    </span>
                    <span className="table-size">{table.size}</span>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
      <div className="back-button-container">
        <button className="reload-button" onClick={handleReload}>
          Reload
        </button>
        <button className="restart-button" onClick={handleRestartTables}>
          Restart Tables
        </button>
      </div>
      <ToastContainer />
    </div>
  );
}

export default DatabaseDetails;
