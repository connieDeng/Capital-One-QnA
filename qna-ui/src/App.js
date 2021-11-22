import React, { useState } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

import {top10Banks,top100Questions, legalAgreements} from "./top100Questions";

function App() {
  const [bank, setbank] = React.useState('');
  const [inputValue, setInputValue] = React.useState('');

  return (
    <div className="App" style={{ "display":"flex", "justifyContent":"center", "textAlign" : "center", "paddingTop":"20vh"}}>
      <section style={{"minWidth":"70vw", "minHeight":"35vh", "display":"flex", "justifyContent":"space-between", "flexDirection" : "column", "alignItems":"center"}}>
        <h1>Financial QnA</h1>
        {/* this is displaying the top 10 banks */}
        <Autocomplete
          value={bank}
          onChange={(event, newValue) => {
            setbank(newValue);
          }}
          inputValue={inputValue}
          onInputChange={(event, newInputValue) => {
            setInputValue(newInputValue);
          }}
          style={{"backgroundColor":'white', "width":"40vw"}}
          id="combo-box-demo"
          options={top10Banks}
          renderInput={(params) => <TextField {...params} label="Banks" />}
        />
        <section>
          <div> Summary of {bank}</div>
          <div> fake stats </div>
        </section>
        {/* <iframe src= {"https://www.bankofamerica.com/"} style={{"backgroundColor":'white', "minWidth":"40vw", "minHeight" :"40vh"}}></iframe > */}

        <Autocomplete
          style={{"backgroundColor":'white', "width":"40vw"}}
          freeSolo
          id="combo-box-demo"
          options={top100Questions}
          renderInput={(params) => <TextField {...params} label="Question" />}
        />
        <Button variant="contained">Submit</Button>
      </section>
    </div>
  );
}


export default App;
