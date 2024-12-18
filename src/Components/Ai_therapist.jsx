import React from 'react';
import Navbar from './Navbar';
import Main from './components/Main/Main';
import ContextProvider from '../context/Context';

function AITherapist() {
  console.log("AITherapist component rendered");
  
  return (
    <div id="body">
      <Navbar />
      <ContextProvider>
        <div id='inner-root' style={{ marginTop: '50px' }}>
          <Main />
        </div>
      </ContextProvider>
    </div>
  );
}

export default AITherapist;