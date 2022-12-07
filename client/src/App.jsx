import { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import SignIn from 'pages/SignIn';
import TextList from 'pages/TextList';
import TextInspection from 'pages/TextInspection';
import 'App.css';

const App = () => {
  //= localStorage에서 모드 정보 불러온 후 없으면 기기 다크모드 감지 후 모드 설정
  const [mode, setMode] = useState(
    !!localStorage.getItem('viewMode')
      ? localStorage.getItem('viewMode')
      : window.matchMedia &&
        window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light'
  );
  const modeState = { mode, setMode };

  useEffect(() => {
    if (!Boolean(localStorage.getItem('viewMode')))
      localStorage.setItem('viewMode', 'light');
  }, []);

  return (
    <div className={`container ${mode}`}>
      <Routes>
        <Route path='/' element={<SignIn {...modeState} />} />
        <Route path='/home/:tf/' element={<TextList {...modeState} />} />
        <Route
          path='/home/:tf/:option/:word'
          element={<TextList {...modeState} />}
        />
        <Route
          path='/detail/:tf/:oid'
          element={<TextInspection {...modeState} />}
        />
        <Route
          path='/detail/:tf/:option/:word/:oid'
          element={<TextInspection {...modeState} />}
        />
      </Routes>
    </div>
  );
};

export default App;
