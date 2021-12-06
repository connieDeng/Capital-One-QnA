import React, { useState, useEffect } from 'react';
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
    if (bank && question) {
      Axios({
        method: "POST",
        data: {
          // pass the legal link of selected bank
          bank: legalAgreements[bank],
          question: question,
        },
        withCredentials: true,
        url: "http://172.17.226.136:8000/predict",
      }).then((res) => {
        console.log(res)
        setAnswers(res.data)
      });
    } else {
    
    }
  };

  return (
    <div className="App" style={{ "display":"flex", "justifyContent":"center", "textAlign" : "center", "paddingTop":"20vh"}}>
      <section style={{"minWidth":"70vw", "minHeight":"35vh", "display":"flex", "justifyContent":"space-between", "flexDirection" : "column", "alignItems":"center"}}>
        <h1>Financial QnA</h1>
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
          style={{"backgroundColor":'white', "width":"40vw", "paddingBottom": "2%"}}
          freeSolo
          id="combo-box-demo"
          options={top100Questions}
          renderInput={(params) => <TextField {...params} label="Question" />}
          onKeyDown={e => {
            if (e.code === 'Enter'){
              submitQnA();
            }
          }}
        />
        
        <section>
          <div>
          {answers.length === 0 ? 
            <div></div> 
            : 
            <div style={{"padding": "1% 2.5% 2.5% 2.5%", "overflow":"scroll", 
            "maxHeight": "20em", "maxWidth":"80em", "textAlign":"left", 
            "backgroundColor":"#EBECF0", "overflowX": "hidden"}}>      
              {showTop10Ans === false ? 
                <div>
                  <h1>Answer</h1>
                  <div>{answers.result[0]}</div> 
                </div>
                : 
                <div>
                  <h1>Top 10 Answers</h1>
                  <ol type="1">
                    {answers.result.map(function(d, idx){
                      return (<li style={{"padding": ".5% 0% .5% 0%"}} key={idx}>{d}</li>)
                    })}
                  </ol>
                </div>
              }  
            </div> 
          }
          </div>
        </section>
        
        <div style={{"paddingTop": "1%", "paddingBottom": "1%"}}>
        {answers.length === 0 ? 
          <div></div> 
          : 
          <Button variant="contained" onClick={() => setshowTop10Ans(!showTop10Ans)}> 
            {showTop10Ans?
              <div> Show only the first answer </div>
              :
              <div> Do the answers not make sense? </div>
            }
          </Button>          
        }  
        </div>

        <Button variant="contained" onClick={() => submitQnA()}>Submit</Button>          
      </section>
    </div>
  );
}


export default App;
