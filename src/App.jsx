// import './App.css'
import Navbar from './Components/Navbar'
import Home from './Components/Home'
import About from './Components/About'
import Services from './Components/Services'
import Therapy from './Components/Therapy'
import Footer from './Components/Footer'


function App() {
  return (
    <>
      <Navbar></Navbar>
      <main>
        <div id='home'><Home></Home></div>
        <div id='about'><About></About></div>
        <div id='services'><Services></Services></div>
        <div id='doctors'><Therapy></Therapy></div>
      </main>
      <Footer></Footer>
    </>
  )
}

export default App
