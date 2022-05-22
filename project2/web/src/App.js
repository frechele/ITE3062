import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from 'react';
import { Container, Button } from 'react-bootstrap';

import Header from './components/Header';

function ProblemScreen() {
  return (
      <div className="App">
        <Header />

        <h1>Fuck you</h1>
      </div>
  )
}

function App() {
  const [screen, setScreen] = useState(false);

  if (screen == false) {
    return (
      <div>
        <Header />
        
        {
          screen === false
          ?
          <Container>
          <p>본 user study에서는 인공지능이 제공하는 정보의 양과 질에 따른 사용성(usability)과 효율성(efficiency)을 측정하고자 합니다.</p>
          <p>아래 시작버튼을 누르면 총 20문제가 나오며, 각 문제마다 이미지와 이미지에 대한 질문이 주어집니다.
            각 문제에 관련된 추가 정보가 제공될 수도 있습니다.
          </p>
    
          <div className="text-center">
            <Button variant="outline-primary" onClick={ () => { setScreen(true) }}>시작</Button>
          </div>
          </Container>
          : <ProblemScreen />
        }
      </div>
    );
  } else {
    return ProblemScreen();
  }
}

export default App;
