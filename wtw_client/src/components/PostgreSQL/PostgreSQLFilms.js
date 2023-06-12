import { useEffect, useState } from "react";
import axios from "axios";
import FilmCard from "../FilmCard";
import AddFilmPanel from "../AddFilmPanel";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function PostgreSQLFilms() {
  const [loading, setLoading] = useState(true);
  const [films, setFilms] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [sortOption, setSortOption] = useState("None");
  const [filterValue, setFilterValue] = useState("");
  const [searchValue, setSearchValue] = useState("");

  useEffect(() => {
    const abortController = new AbortController();
    setLoading(true);

    const fetchFilms = async () => {
      try {
        let url = `/postgresql/films/?page=${page}`;

        if (sortOption !== "None") {
          url += url.includes("?") ? "&" : "?";
          url += `sort_by=${sortOption}`;
        }

        if (searchValue !== "") {
          url += url.includes("?") ? "&" : "?";
          url += `filter_by=title&filter_value=${searchValue}`;
        }

        const response = await axios.get(url, {
          signal: abortController.signal,
        });

        if (response.status !== 200) {
          throw new Error("Network response was not ok");
        }

        const {
          films: newFilms,
          total_pages: newTotalPages,
          execution_time: execTime,
        } = response.data;

        if (!abortController.signal.aborted) {
          setFilms(newFilms);
          setTotalPages(newTotalPages);

          if (execTime) {
            let infoText = `Page ${page} displayed in ${execTime} second(s)`;

            toast.info(infoText, {
              position: toast.POSITION.BOTTOM_RIGHT,
            });
          }

          setLoading(false);
        }
      } catch (error) {
        console.log(error);

        let errorText = "Error while fetching data";
        toast.error(errorText, {
          position: toast.POSITION.BOTTOM_RIGHT,
        });
      }
    };

    fetchFilms();

    return () => {
      abortController.abort();
    };
  }, [page, sortOption, searchValue]);

  const handleSortChange = (event) => {
    setSortOption(event.target.value);
    setLoading(true);
    setPage(1);
    setFilms([]);
  };

  const handleSearchChange = (event) => {
    setFilterValue(event.target.value);
  };

  const handleSearchClick = () => {
    if (filterValue !== searchValue) {
      setSearchValue(filterValue);
      setLoading(true);
      setPage(1);
      setFilms([]);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="App-header">
      <div className="title">Films - PostgreSQL</div>
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
        <FilmCard
          films={films}
          page={page}
          totalPages={totalPages}
          setFilms={setFilms}
          setPage={setPage}
          setLoading={setLoading}
        />

        <AddFilmPanel setFilms={setFilms} setLoading={setLoading} />
      </div>
      <ToastContainer />
    </div>
  );
}
export default PostgreSQLFilms;
