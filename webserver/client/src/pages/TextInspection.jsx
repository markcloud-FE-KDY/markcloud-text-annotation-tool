import { useState, useEffect } from 'react';
import $ from 'jquery';
import ReactHotKey from 'react-shortcut';
import { useParams, useNavigate } from 'react-router-dom';
import { ImArrowLeft, ImArrowRight } from 'react-icons/im';
import HotkeyGuide from 'components/HotkeyGuide';
import ViewMode from 'components/ViewMode';
import { getTextDetail, modifyText } from 'js/api';
import { enterFn, catchErrorHandler, changeState } from 'js/common';
import { getCookie } from 'js/cookie';

const TextInspection = ({ mode, setMode }) => {
  const [info, setInfo] = useState({});
  const [similar, setSimilar] = useState('');
  const [input, setInput] = useState('');
  const { tf, oid, option, word } = useParams();
  const navigate = useNavigate();
  let prevent = false;

  //= 상세내역 불러오기
  const getDetail = async () => {
    if (prevent) return;
    prevent = true;
    setTimeout(() => {
      prevent = false;
    }, 200);
    setSimilar('');
    setInput('');
    $('.active').removeClass('active');
    let result;
    if (!option?.length) result = await getTextDetail(oid, tf);
    else if (option === 'text') result = await getTextDetail(oid, tf, word);
    else if (option === 'worker')
      result = await getTextDetail(oid, tf, false, word);
    else if (option === 'calendar') {
      const date = word.split('&');
      result = await getTextDetail(oid, tf, false, false, date[0], date[1]);
    }
    if (typeof result === 'object') {
      setInfo(prev => {
        let clone = { ...prev };
        clone = result?.data?.current;
        clone.next = result?.data?.next;
        clone.prev = result?.data?.previous;
        clone.pageUp = result?.data?.pageUp;
        clone.pageDown = result?.data?.pageDown;
        return clone;
      });
    } else return catchErrorHandler(result);
  };

  //= direction에 따라 페이지 변경
  const changePage = direction => {
    if (direction === 'next' && info.pageUp)
      localStorage.setItem('page', Number(localStorage.getItem('page')) + 1);
    else if (direction === 'prev' && info.pageDown)
      localStorage.setItem('page', Number(localStorage.getItem('page')) - 1);
    else if (
      direction === 'next' &&
      Number(localStorage.getItem('totalPage')) ===
        Number(localStorage.getItem('page')) &&
      info.next === null
    )
      return alert(`마지막 페이지입니다.`);
    else if (
      direction === 'prev' &&
      Number(localStorage.getItem('page')) === 1 &&
      info.prev === null
    )
      return alert(`첫 페이지입니다.`);

    if (option?.length && word?.length)
      navigate(`/detail/${tf}/${option}/${word}/${info[direction]}`);
    else navigate(`/detail/${tf}/${info[direction]}`);
  };

  //= 검수
  const postResult = async status => {
    let data;
    if (status === 'pass') {
      if (info?.passCheck) return console.log('pass');
      data = { userInput: '' };
    } else {
      if (!input.length && !similar.length)
        return alert('유사 단어를 선택하거나 입력해 주세요.');
      data = { userInput: `${input.length ? input : similar}` };
    }
    const result = await modifyText(oid, status === 'pass', data);
    if (typeof result === 'object') {
      setInput('');
      setSimilar('');
      $('input').blur();
      if (status === 'pass') getDetail();
      else changePage('next');
    } else return catchErrorHandler(result);
  };

  //= 단축키로 유사 단어 선택할 때
  const hotkeyCheck = i => {
    if (info?.passCheck || info?.humanCheck) return;
    $('.active').removeClass('active');
    if (i === 0) {
      setSimilar('');
      return;
    }
    if (input.length) setInput('');
    setSimilar($(`#${i}`).text());
    $(`#${i}`).addClass('active');
  };

  //= 직접 유사 단어 선택할 때
  const checkSimilar = e => {
    if (info?.passCheck || info?.humanCheck) return;
    $('.active').removeClass('active');
    if (
      e.target.textContent === '유사 단어가 없습니다.' ||
      e.target.textContent === ''
    )
      return;
    if (input.length) setInput('');
    setSimilar(e.target.textContent);
    e.target.className = 'active';
  };

  useEffect(() => {
    if (!getCookie('myToken')) {
      navigate('/');
      return alert('로그인이 필요한 서비스입니다.');
    }
  }, []);

  useEffect(() => {
    getDetail();
  }, [oid]);

  useEffect(() => {
    if (input.includes('@')) $('input').blur();
    const regExp =
      /[a-z0-9]|[ /[\{\}\[\]\/?.;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]/g;
    if (regExp.test(input)) setInput(input.substring(0, input.length - 1));
  }, [input]);

  return (
    <>
      <ViewMode mode={mode} setMode={setMode} />
      <div className='content-wrap inspect'>
        <ReactHotKey keys='ESC' onKeysPressed={() => hotkeyCheck(0)} />
        {info?.modelResult?.length && (
          <ReactHotKey keys='1' onKeysPressed={() => hotkeyCheck(1)} />
        )}
        {Array(5)
          .fill(0)
          .map((i, idx) => {
            return (
              <>
                {info?.similarWords?.length >= idx + 1 && (
                  <ReactHotKey
                    keys={`${idx + 2}`}
                    onKeysPressed={() => hotkeyCheck(idx + 2)}
                  />
                )}
              </>
            );
          }, <></>)}
        {info?.humanCheck || (
          <ReactHotKey
            keys='Enter'
            onKeysPressed={() => postResult('complete')}
          />
        )}
        <ReactHotKey keys='Space' onKeysPressed={() => postResult('pass')} />
        <ReactHotKey
          keys='!'
          onKeysPressed={() => {
            $('input').focus();
          }}
        />
        <ReactHotKey
          keys='#'
          onKeysPressed={() => {
            if (info?.passCheck) changeState(setInfo, 'passCheck', false);
          }}
        />
        <ReactHotKey keys='left' onKeysPressed={() => changePage('prev')} />
        <ReactHotKey keys='right' onKeysPressed={() => changePage('next')} />
        <div className='icons row'>
          <ImArrowLeft className='prev' onClick={() => changePage('prev')} />
          <div className='column'>
            <button
              onClick={() => {
                if (option && word) navigate(`/home/${tf}/${option}/${word}`);
                else navigate(`/home/${tf}`);
              }}>
              HOME
            </button>
          </div>
          <ImArrowRight className='next' onClick={() => changePage('next')} />
        </div>
        <div
          className={`wordStep row ${
            info?.humanCheck ? 'viewResult' : 'blockResult'
          }`}>
          <div className='connect-word mobile-none'></div>
          <div className='word'>
            <span>원본 영어</span>
            {info?.originalEng?.length === 1 ? (
              <div>{info?.originalEng}</div>
            ) : (
              <div className='originalList'>
                <ul>
                  {info?.originalEng?.slice(0, 5).reduce((acc, content) => {
                    return (
                      <>
                        {acc}
                        <li>{content}</li>
                      </>
                    );
                  }, <></>)}
                  {info?.originalEng?.length > 5 && <li>...</li>}
                </ul>
              </div>
            )}
          </div>
          <div className='word'>
            <span>1차 가공 영어</span>
            <div>{info?.productNameEng}</div>
          </div>
        </div>
        <hr />
        {info?.passCheck ? (
          <>
            <span className='checkStatus'>
              {info?.passCheck && '보류된 단어입니다.'}
            </span>
          </>
        ) : (
          <>
            {' '}
            <div className='row list'>
              <div className='column modelResult'>
                <span className='guideText'>
                  {info?.humanCheck ? '검수 종류' : '모델 단어'}
                </span>
                <div className='modelResults'>
                  {info?.humanCheck
                    ? (info?.resultStatus === 'direct' && '직접') ||
                      (info?.resultStatus === 'candidate' && '후보') ||
                      (info?.resultStatus === 'model' && '모델')
                    : info?.modelResult}
                </div>
              </div>
              <div className='column'>
                <span className='guideText'>
                  {info?.humanCheck ? '검수 결과' : '후보 단어'}
                </span>
                <div className='similarWords column'>
                  {info?.humanCheck
                    ? info?.directInput?.length > 1
                      ? info?.directInput?.reduce((acc, i) => {
                          return (
                            <>
                              {acc}
                              <span className='directInputs'>{i}</span>
                            </>
                          );
                        }, <></>)
                      : info?.directInput
                    : !info?.similarWords?.length && '후보 단어가 없습니다.'}
                  <div className='row'>
                    {Array(3)
                      .fill(0)
                      .map((i, idx) => {
                        return (
                          <>
                            {info?.similarWords?.length >= idx + 1 &&
                              !info?.humanCheck && (
                                <div
                                  onClick={e => checkSimilar(e)}
                                  id={idx + 1}>
                                  {info?.similarWords[idx]}
                                </div>
                              )}
                          </>
                        );
                      }, <></>)}
                  </div>
                  {info?.similarWords?.length > 3 && !info?.humanCheck ? (
                    <div className='row second'>
                      {Array(3)
                        .fill(0)
                        .map((i, idx) => {
                          return (
                            <>
                              {info?.similarWords?.length >= idx + 4 && (
                                <div
                                  onClick={e => checkSimilar(e)}
                                  id={idx + 4}>
                                  {info?.similarWords[idx + 3]}
                                </div>
                              )}
                            </>
                          );
                        }, <></>)}
                    </div>
                  ) : (
                    ''
                  )}
                </div>
              </div>
            </div>
            {info?.humanCheck || (
              <input
                type='text'
                placeholder='직접 입력'
                value={input}
                onChange={e => {
                  if (similar.length) hotkeyCheck(0);
                  setInput(e.target.value);
                }}
                className={`${info?.humanCheck ? 'complete' : 'inComplete'}`}
                readOnly={info?.humanCheck || info?.passCheck}
                onKeyDown={e => enterFn(e, () => postResult('complete'))}
              />
            )}
            {info?.passCheck || info?.humanCheck || (
              <p>한글과 콤마(,)만 입력 가능합니다.</p>
            )}
          </>
        )}
        <hr />
        <div className='btnWrap column'>
          {info?.humanCheck ? (
            <div className='row'>
              {info?.worker === getCookie('userInfo') ||
              getCookie('userInfo') === 'admin' ? (
                <button
                  onClick={() => changeState(setInfo, 'humanCheck', false)}>
                  수정
                </button>
              ) : (
                ''
              )}
              <button onClick={() => changePage('next')}>다음</button>
            </div>
          ) : info?.passCheck ? (
            <div className='row'>
              {info?.worker === getCookie('userInfo') ||
              getCookie('userInfo') === 'admin' ? (
                <button
                  onClick={() => changeState(setInfo, 'passCheck', false)}>
                  수정
                </button>
              ) : (
                ''
              )}
              <button onClick={() => changePage('next')}>다음</button>
            </div>
          ) : (
            <div className='row'>
              <button onClick={() => postResult('pass')}>보류</button>
              <button onClick={() => postResult('complete')}>완료</button>
            </div>
          )}
        </div>
      </div>
      <HotkeyGuide />
    </>
  );
};

export default TextInspection;
