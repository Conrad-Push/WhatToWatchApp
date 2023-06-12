import React from "react";

function DatabaseDetails(props) {
  const capitalize = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
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
    </div>
  );
}

export default DatabaseDetails;
