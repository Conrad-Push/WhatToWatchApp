import { useEffect, useState } from "react";
import axios from "axios";
import Card from "./Card";
import AddFilmPanel from "./AddFilmPanel";

function PostgreSQL() {
  const [films, setFilms] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sortOption, setSortOption] = useState("None");
  const [filterValue, setFilterValue] = useState("");
  const [searchValue, setSearchValue] = useState("");

  useEffect(() => {
    const fetchFilms = async () => {
      try {
        let url = "/films/";

        if (sortOption !== "None") {
          url += `?sort_by=${sortOption}`;
        }

        if (searchValue !== "") {
          url += url.includes("?") ? "&" : "?";
          url += `filter_by=title&filter_value=${searchValue}`;
        }

        const response = await axios.get(url);

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
  }, [sortOption, searchValue]);

  const handleSortChange = (event) => {
    setSortOption(event.target.value);
  };

  const handleSearchChange = (event) => {
    setFilterValue(event.target.value);
  };

  const handleSearchClick = () => {
    setSearchValue(filterValue);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="App-header">
      <div className="title">PostgreSQL</div>
      <div className="filters">
        <div className="sort-dropdown">
          <label htmlFor="sort">Sort By:</label>
          <select id="sort" value={sortOption} onChange={handleSortChange}>
            <option value="None">None</option>
            <option value="title">Title</option>
            <option value="year">Year</option>
            <option value="rate">Rate</option>
          </select>
        </div>
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search..."
            value={filterValue}
            onChange={handleSearchChange}
          />
          <button onClick={handleSearchClick}>Search</button>
        </div>
      </div>
      <div className="films-container">
        <Card films={films} setFilms={setFilms} />
        <AddFilmPanel setFilms={setFilms} />
      </div>
    </div>
  );
}
export default PostgreSQL;
