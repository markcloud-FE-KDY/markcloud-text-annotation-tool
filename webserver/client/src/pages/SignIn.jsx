import { useState, useEffect } from 'react';
import $ from 'jquery';
import { useNavigate } from 'react-router-dom';
import ViewMode from 'components/ViewMode';
import { getCookie, setCookie } from 'js/cookie';
import { signIn } from 'js/api';
import { enterFn, catchErrorHandler } from 'js/common';

const SignIn = ({ mode, setMode }) => {
  const [userId, setUserId] = useState('');
  const [userPw, setUserPw] = useState('');
  const navigate = useNavigate();

  const logIn = async () => {
    if (userId === '' && userPw === '') {
      alert('아이디와 비밀번호가 입력되지 않았습니다.');
      $('.userIdInput').focus();
      return;
    } else if (userId === '') {
      alert(`아이디를 입력해 주세요.`);
      $('.userIdInput').focus();
      return;
    } else if (userPw === '') {
      alert('비밀번호를 입력해 주세요.');
      $('.userPwInput').focus();
      return;
    }
    const result = await signIn(userId, userPw);
    if (typeof result === 'object') {
      const { access_token, username } = result?.data;
      setCookie('myToken', access_token, {
        path: '/',
      });
      setCookie('userInfo', username, {
        path: '/',
      });
      navigate('/home/0');
    } else catchErrorHandler(result);
  };

  useEffect(() => {
    if (getCookie('myToken')) navigate('/home/0');
    else $('.userIdInput').focus();
  }, []);

  return (
    <>
      <ViewMode mode={mode} setMode={setMode} />
      <div className='content-wrap sign-in'>
        <div className='header'>
          <h1>MARKCLOUD</h1>
          <h1>TEXT INSPECTION</h1>
        </div>
        <div className='loginForm'>
          <input
            type='text'
            placeholder='ID'
            className='userIdInput'
            value={userId}
            onChange={e => setUserId(e.target.value)}
            onKeyDown={e => enterFn(e, logIn)}
          />
          <input
            type='password'
            placeholder='PW'
            className='userPwInput'
            value={userPw}
            onChange={e => setUserPw(e.target.value)}
            onKeyDown={e => enterFn(e, logIn)}
          />
          <button onClick={logIn}>LOGIN</button>
        </div>
      </div>
    </>
  );
};

export default SignIn;
