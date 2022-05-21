import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Button, ButtonGroup } from 'react-bootstrap';

function App() {
  return (
    <div className="App">
      <Container>
        <Button variant="primary">Primary</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="success">Success</Button>
        <Button variant="danger">Danger</Button>
        <Button variant="warning">Warning</Button>
        <Button variant="info">Info</Button>
        <Button variant="light">Light</Button>
        <Button variant="dark">Dark</Button>
      </Container>
    </div>
  );
}

export default App;
