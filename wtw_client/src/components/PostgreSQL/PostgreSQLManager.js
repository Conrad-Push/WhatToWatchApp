import { useEffect, useState } from "react";
import axios from "axios";

function PostgreSQLManager() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        let url = "/postgresql/database/status";

        const response = await axios.get(url);

        if (response.status !== 200) {
          throw new Error("Network response was not ok");
        }

        setData(response.data);

        setLoading(false);
      } catch (error) {
        console.log(error);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="App-header">
      <div className="title">DB Manager - PostgreSQL</div>
      <div>
        <p>{data.message}</p>
        <p>{data.db_state}</p>
        {data.tables_details && (
          <div>
            <h2>Tables Details:</h2>
            <ul>
              {data.tables_details.map((table) => (
                <li key={table.name}>
                  Name: {table.name}, Size: {table.size}
                </li>
              ))}
            </ul>
          </div>
        )}
        <p>{data.execution_time}</p>
      </div>
    </div>
  );
}
export default PostgreSQLManager;
