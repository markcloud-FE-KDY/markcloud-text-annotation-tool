export const catchErrorHandler = error => {
  if (error === 'serverError') return alert('잠시 후 다시 시도해 주세요.');
  else if (error === 'wrongId')
    return alert('아이디 또는 비밀번호가 틀렸습니다.\n다시 입력해 주세요.');
  else if (error === 'wrongPw')
    return alert('비밀번호가 틀렸습니다.\n다시 입력해 주세요.');
  else if (error === 'excessLogin')
    return alert(
      '로그인 시도 횟수를 초과하였습니다.\n나중에 다시 시도해 주세요.'
    );
  else if (error === 'retiredUser') {
    if (window.confirm('탈퇴한 회원입니다.\n다시 가입하시겠습니까?'))
      window.open('https://markcloud.co.kr/sign-up');
    else return;
  } 
};

export const changeState = (setState, column, value) => {
  setState(prev => {
    const clone = { ...prev };
    clone[column] = value;
    return clone;
  });
};

export const enterFn = (e, Fn) => {
  if (e.key === 'Enter') Fn();
  else return;
};

export const addZero = t => {
  if (t < 10) return `0${t}`;
  else return t;
};
