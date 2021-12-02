import React, { useState } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Axios from "axios";
import {top10Banks,top100Questions, legalAgreements} from "./info";

function App() {
  // bank chosen
  const [bank, setbank] = useState('');
  const [inputValue, setInputValue] = useState('');
  
  const [question, setQuestion] = useState('');
  const [inputValueQuestion, setInputValueQuestion] = useState('');

  const [answers, setAnswers] = useState([]);
  const [showTop10Ans, setshowTop10Ans] = useState(false);

  const submitQnA = () => {
    console.log(bank)
    console.log(question)
      Axios({
        method: "POST",
        data: {
          // pass the legal link of selected bank
          bank: legalAgreements[bank],
          question: question,
        },
        withCredentials: true,
        url: "http://172.17.226.79:8000/predict",
      }).then((res) => {
        console.log(res)
        setAnswers(res.data)
      });
  };

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
        <section style={{"padding": "1%"}} >
          {/* <div> Summary of {bank}</div>
          <div> fake stats </div> */}
        </section>
        {/* <iframe src= {"https://www.bankofamerica.com/"} style={{"backgroundColor":'white', "minWidth":"40vw", "minHeight" :"40vh"}}></iframe > */}

        {/* question input */}
        <Autocomplete
          value={question}
          onChange={(event, newValue) => {
            setQuestion(newValue);
          }}
          inputValue={inputValueQuestion}
          onInputChange={(event, newInputValue) => {
            setInputValueQuestion(newInputValue);
            setQuestion(newInputValue);
          }}
          style={{"backgroundColor":'white', "width":"40vw"}}
          freeSolo
          id="combo-box-demo"
          options={top100Questions}
          renderInput={(params) => <TextField {...params} label="Question" />}
        />
        
        <section style={{"padding": "2% 20% 2% 20% "}}>
        {answers.length === 0 ? 
          <div></div> 
          : 
          <div>      
            {showTop10Ans === false ? 
              <div>{answers.result[0]}</div> 
              : 
              <div>
                {answers.result.map(function(d, idx){
                  return (<li key={idx}>{d}</li>)
                })}
              </div>
            }  
          </div> 
        }
        </section>


        <Button variant="contained" onClick={() => setshowTop10Ans(!showTop10Ans)}> Do the answers not make sense? </Button>          
        <div style={{"padding": "0.25%"}}></div>
        <Button variant="contained" onClick={() => submitQnA()}>Submit</Button>          
      </section>
    </div>
  );
}


export default App;
