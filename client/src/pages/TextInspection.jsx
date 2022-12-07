import React, { useState, useEffect } from 'react';
import $ from 'jquery';
import { useParams, useNavigate } from 'react-router-dom';
import ReactHotKey from 'react-shortcut';
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
    if (typeof result === 'object')
      setInfo(prev => {
        let clone = { ...prev };
        clone = result?.data?.current;
        clone.next = result?.data?.next;
        clone.prev = result?.data?.previous;
        return clone;
      });
    else return catchErrorHandler(result);
  };

  const changePage = direction => {
    if (info[direction] === null)
      return alert(`${direction === 'prev' ? '첫' : '마지막'} 페이지입니다.`);
    else if (option?.length && word?.length)
      navigate(`/detail/${tf}/${option}/${word}/${info[direction]}`);
    else navigate(`/detail/${tf}/${info[direction]}`);
  };

  const postResult = async status => {
    let data;
    if (status === 'pass') {
      if (info?.passCheck) return console.log('pass');
      data = { modelResult: '' };
    } else {
      if (!input.length && !similar.length)
        return alert('유사 단어를 선택하거나 입력해 주세요.');
      data = { modelResult: `${input.length ? input : similar}` };
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
    const regExp = /[a-z0-9]|[ \[\]{}()<>?|`~!@#$%^&*-_+=,.;:\"'\\]/g;
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
          {info?.humanCheck && (
            <div className='word'>
              <span>검수 결과</span>
              <div>{info?.modelResult}</div>
            </div>
          )}
        </div>
        <hr />
        {info?.humanCheck || info?.passCheck ? (
          <>
            <span className='checkStatus'>
              {info?.humanCheck && '검수가 완료된 단어입니다.'}
              {info?.passCheck && '보류된 단어입니다.'}
            </span>
          </>
        ) : (
          <>
            {' '}
            <span className='similarWordsGuide'>유사 단어 목록</span>
            <div className='similarWords column'>
              <div className='row'>
                <div onClick={e => checkSimilar(e)} id={1}>
                  {info?.modelResult}
                </div>
                {Array(2)
                  .fill(0)
                  .map((i, idx) => {
                    return (
                      <>
                        {info?.similarWords?.length >= idx + 1 &&
                          !info?.humanCheck && (
                            <div onClick={e => checkSimilar(e)} id={idx + 2}>
                              {info?.similarWords[idx]}
                            </div>
                          )}
                      </>
                    );
                  }, <></>)}
              </div>
              {info?.similarWords?.length > 2 && !info?.humanCheck ? (
                <div className='row second'>
                  {Array(3)
                    .fill(0)
                    .map((i, idx) => {
                      return (
                        <>
                          {info?.similarWords?.length >= idx + 3 && (
                            <div onClick={e => checkSimilar(e)} id={idx + 4}>
                              {info?.similarWords[idx + 2]}
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
            {info?.passCheck || info?.humanCheck || (
              <p>한글만 입력 가능합니다.</p>
            )}
          </>
        )}
        <hr />
        <div className='btnWrap column'>
          {info?.humanCheck ? (
            <>
              <button onClick={() => changePage('next')}>다음</button>
            </>
          ) : info?.passCheck ? (
            <div className='row'>
              <button onClick={() => changeState(setInfo, 'passCheck', false)}>
                수정
              </button>
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
