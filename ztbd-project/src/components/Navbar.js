import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import SlidingPane from "react-sliding-pane";
import "react-sliding-pane/dist/react-sliding-pane.css";

function Navbar() {
  const navigate = useNavigate();
  const [state, setState] = useState({
    isPaneOpen: false,
  });


  return (
    <div className='navBox'>
      <nav className="navbar navbar-expand-lg navbar-light navCss">
        <button className="btn" onClick={() => setState({ isPaneOpen: true })}>
          <span className="navbar-toggler-icon"></span>
        </button>
        <SlidingPane
          className="topSlider"
          overlayClassName="topSlider"
          isOpen={state.isPaneOpen}
          title={<a className="navbar-brand logo" onClick={() => { navigate("/"); setState({ isPaneOpen: false }) }}></a>}
          width='300px'
          from='left'
          onRequestClose={() => {
            setState({ isPaneOpen: false });
          }}>

          <ul>
            <li><a onClick={() => { navigate("/mysql"); setState({ isPaneOpen: false }); }}>MySQL</a></li>
            <li><a onClick={() => { navigate("/mongodb"); setState({ isPaneOpen: false }); }}>MongoDB</a></li>
            <li><a onClick={() => { navigate("/redis"); setState({ isPaneOpen: false }); }}>Redis</a></li>
          </ul>
        </SlidingPane>
        
        <a className="navbar-brand logo" onClick={() => { navigate("/") }}>Bazy</a>
        <div className='navv'>
        <a onClick={() => { navigate("/mysql"); setState({ isPaneOpen: false }); }}>MySQL</a>
        <a onClick={() => { navigate("/mongodb"); setState({ isPaneOpen: false }); }}>MongoDB</a>
        <a onClick={() => { navigate("/redis"); setState({ isPaneOpen: false }); }}>Redis</a>
        </div>
      </nav>

    </div>

  )
}

export default Navbar;