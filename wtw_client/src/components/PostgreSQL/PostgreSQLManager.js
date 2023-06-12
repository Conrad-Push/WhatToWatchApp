import { useEffect, useState } from "react";
import axios from "axios";
import DatabaseStatus from "../DatabaseStatus";
import DatabaseDetails from "../DatabaseDetails";
import ScrapDataPanel from "../ScrapDataPanel";
import GenerateDataPanel from "../GenerateDataPanel";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function PostgreSQLManager() {
  const [loading, setLoading] = useState(true);
  const [DBState, setDBState] = useState("Not connected");
  const [tablesDetails, setTablesDetails] = useState([]);

  useEffect(() => {
    const abortController = new AbortController();

    const fetchData = async () => {
      try {
        let url = "/postgresql/database/status";

        const response = await axios.get(url, {
          signal: abortController.signal,
        });

        if (response.status !== 200) {
          throw new Error("Network response was not ok");
        }

        const {
          message: mess,
          db_state: newDBState,
          tables_details: newTablesDetails,
          execution_time: execTime,
        } = response.data;

        if (!abortController.signal.aborted) {
          setDBState(newDBState);
          setTablesDetails(newTablesDetails);

          if (mess && execTime) {
            let infoText = `${mess} in ${execTime} second(s)`;

            toast.info(infoText, {
              position: toast.POSITION.BOTTOM_LEFT,
            });
          }

          setLoading(false);
        }

        setLoading(false);
      } catch (error) {
        console.log(error);
      }
    };

    fetchData();

    return () => {
      abortController.abort();
    };
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="App-header">
      <div className="title">DB Manager - PostgreSQL</div>
      {DBState && <DatabaseStatus status={DBState} />}
      {tablesDetails && (
        <div className="db-manager-container">
          <DatabaseDetails details={tablesDetails} />
          <div className="data-panels-container">
            <ScrapDataPanel
              setLoading={setLoading}
              setTablesDetails={setTablesDetails}
            />
            <GenerateDataPanel
              setLoading={setLoading}
              setTablesDetails={setTablesDetails}
            />
          </div>
        </div>
      )}

      <ToastContainer />
    </div>
  );
}
export default PostgreSQLManager;
