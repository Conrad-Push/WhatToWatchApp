import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import SlidingPane from "react-sliding-pane";
import "react-sliding-pane/dist/react-sliding-pane.css";

function Navbar() {
  const navigate = useNavigate();
  const [state, setState] = useState({
    isPaneOpen: false,
  });
  const [selectedDatabase, setSelectedDatabase] = useState("");

  useEffect(() => {
    const storedDatabase = localStorage.getItem("selectedDatabase");
    if (storedDatabase) {
      setSelectedDatabase(storedDatabase);
    }
  }, []);

  const handleDatabaseChange = (database) => {
    setSelectedDatabase(database);
    localStorage.setItem("selectedDatabase", database);
    setState({ isPaneOpen: false });
  };

  const handleHomeClick = () => {
    setSelectedDatabase("");
    localStorage.removeItem("selectedDatabase");
    setState({ isPaneOpen: false });
    navigate("/");
  };

  return (
    <div className="navBox">
      <nav className="navbar navbar-expand-lg navbar-light navCss">
        <button className="btn" onClick={() => setState({ isPaneOpen: true })}>
          <span className="navbar-toggler-icon"></span>
        </button>
        <SlidingPane
          className="topSlider"
          overlayClassName="topSlider"
          isOpen={state.isPaneOpen}
          title={
            <a className="navbar-brand logo" onClick={handleHomeClick}>
              What to watch App
            </a>
          }
          width="300px"
          from="left"
          onRequestClose={() => {
            setState({ isPaneOpen: false });
          }}
        >
          {selectedDatabase ? (
            <ul>
              <li>
                <a
                  onClick={() => {
                    navigate(`/${selectedDatabase}/films`);
                    setState({ isPaneOpen: false });
                  }}
                >
                  Films
                </a>
              </li>
              <li>
                <a
                  onClick={() => {
                    navigate(`/${selectedDatabase}/manager`);
                    setState({ isPaneOpen: false });
                  }}
                >
                  Database Manager
                </a>
              </li>
            </ul>
          ) : (
            <ul>
              <li>
                <a
                  onClick={() => {
                    navigate("/");
                    setState({ isPaneOpen: false });
                  }}
                >
                  Home
                </a>
              </li>
              <li>
                <a
                  onClick={() => {
                    navigate("/technologies");
                    setState({ isPaneOpen: false });
                  }}
                >
                  Technologies
                </a>
              </li>
              <li>
                <a
                  onClick={() => {
                    navigate("/authors");
                    setState({ isPaneOpen: false });
                  }}
                >
                  Authors
                </a>
              </li>
            </ul>
          )}
        </SlidingPane>

        <a className="navbar-brand logo" onClick={handleHomeClick}>
          What to watch App
        </a>
        <div className="navv">
          <a
            onClick={() => {
              handleDatabaseChange("postgresql");
              navigate("/postgresql/films");
              setState({ isPaneOpen: false });
            }}
          >
            PostgreSQL
          </a>
          <a
            onClick={() => {
              handleDatabaseChange("mongodb");
              navigate("/mongodb/films");
              setState({ isPaneOpen: false });
            }}
          >
            MongoDB
          </a>
          <a
            onClick={() => {
              handleDatabaseChange("cassandra");
              navigate("/cassandra/films");
              setState({ isPaneOpen: false });
            }}
          >
            Cassandra
          </a>
          <a
            onClick={() => {
              handleDatabaseChange("");
              navigate("/statistics");
              setState({ isPaneOpen: false });
            }}
          >
            Statistics
          </a>
        </div>
      </nav>
    </div>
  );
}

export default Navbar;
