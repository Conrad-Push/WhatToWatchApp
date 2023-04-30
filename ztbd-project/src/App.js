import './App.css';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Redis from './components/Redis';
import MongoDB from './components/MongoDB';
import MySQL from './components/MySQL';


function App() {
  return (
    <div className="App" >
      <Navbar/>
      <Routes>
        <Route exact path="/" element={<Home/>} />
        <Route exact path="/redis" element={<Redis/>} />
        <Route exact path="/mongodb" element={<MongoDB/>} />
        <Route exact path="/mysql" element={<MySQL/>} />

      </Routes>
      {/* <header className="App-header">
       Halo
      </header> */}
    </div>
  );
}

export default App;
