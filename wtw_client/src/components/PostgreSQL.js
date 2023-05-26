import { useEffect, useState } from "react";
import axios from "axios";
import Card from "./Card";
import AddFilm from "./AddFilm";

function PostgreSQL() {
  const [films, setFilms] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFilms = async () => {
      try {
        const response = await axios.get("/films/");
        if (response.status !== 200) {
          throw new Error("Network response was not ok");
        }
        const data = response.data;
        setFilms(data);
        setLoading(false);
      } catch (error) {
        console.log(error);
      }
    };

    fetchFilms();
  }, [films]);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="App-header">
      <div className="title">PostgreSQL</div>
      <div className="page-design">
        <div>
          <Card films={films} />
        </div>
        <div>
          <AddFilm />
        </div>
      </div>
    </div>
  );
}
export default PostgreSQL;
