import { useEffect, useState } from "react";
import axios from "axios";
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
              position: toast.POSITION.BOTTOM_RIGHT,
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

  const getStatusColor = () => {
    if (DBState.toLowerCase() === "started") {
      return "#11de11";
    } else {
      return "#fc152b";
    }
  };

  const capitalize = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="App-header">
      <div className="title">DB Manager - PostgreSQL</div>
      <div>
        <p>
          Database status:{" "}
          <span style={{ color: getStatusColor() }}>{capitalize(DBState)}</span>
        </p>
        {tablesDetails && (
          <div>
            <h2>Tables Details:</h2>
            <ul>
              {tablesDetails.map((table) => (
                <li key={table.name}>
                  Name: {table.name}, Size: {table.size}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <ToastContainer />
    </div>
  );
}
export default PostgreSQLManager;
