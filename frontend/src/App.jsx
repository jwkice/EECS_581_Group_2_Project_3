import { useState } from 'react'
import ChessboardComponent from './components/ChessboardComponent';
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <ChessboardComponent />
    </div>
  );
}

export default App;
