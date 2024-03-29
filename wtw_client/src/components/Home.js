import React from "react";
import homepageLogo from "../homepageLogo.png";

function Home() {
  return (
    <div className="homepage-box">
      <h1 className="homepage-title">Welcome to the "What to watch App"!</h1>
      <p className="homepage-content">
        Discover a vast collection of films and their details. Whether you're a
        movie enthusiast or looking for something new to watch, our database has
        got you covered.
      </p>
      <img src={homepageLogo} alt="Film" className="homepage-image" />
    </div>
  );
}

export default Home;
