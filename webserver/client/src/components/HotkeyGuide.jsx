import { useState, useEffect } from 'react';
import { IoCloseSharp } from 'react-icons/io5';

const HotkeyGuide = () => {
  const [guide, setGuide] = useState(
    !!localStorage.getItem('hotKeyGuide')
      ? localStorage.getItem('hotKeyGuide')
      : 'open'
  );

  useEffect(() => {
    if (!Boolean(localStorage.getItem('hotKeyGuide')))
      localStorage.setItem('hotKeyGuide', 'open');
    localStorage.setItem('hotKeyGuide', guide);
  }, [guide]);

  return (
    <div
      className={`hotkeyGuide mobile-none ${guide}`}
      onClick={() => guide === 'close' && setGuide('open')}>
      <div className='row head'>
        <span>
          <p className='wide-tablet-none'>텍스트 검수</p> 가이드
        </span>
        {guide === 'open' && (
          <div>
            <IoCloseSharp onClick={() => setGuide('close')} />
          </div>
        )}
      </div>
      {guide === 'open' && (
        <>
          <div className='row keys'>
            <div>
              <span className='key'>1</span> ~ <span className='key'>6</span>
            </div>
            <div>유사 단어 선택</div>
          </div>
          <div className='row keys'>
            <div>
              <span className='key'>ESC</span>
            </div>
            <div>유사 단어 선택 취소</div>
          </div>
          <div className='row keys'>
            <div>
              <span className='key'>!</span>
            </div>
            <div>직접 입력창 활성화</div>
          </div>
          <div className='row keys'>
            <div>
              <span className='key'>@</span>
            </div>
            <div>직접 입력창 비활성화</div>
          </div>
          <div className='row keys'>
            <div>
              <span className='key'>#</span>
            </div>
            <div>보류 단어 수정</div>
          </div>
          <div className='row keys'>
            <div>
              <span className='key'>$</span>
            </div>
            <div>검수 완료 단어 수정</div>
          </div>
          <div className='row keys'>
            <div>
              <span className='key'>Space</span>
            </div>
            <div>PASS</div>
          </div>
          <div className='row keys'>
            <div>
              <span className='key'>Enter</span>
            </div>
            <div>완료</div>
          </div>
          <div className='row keys'>
            <div>
              <span className='key'>←</span> / <span className='key'>→</span>
            </div>
            <div>이전 페이지 / 다음 페이지</div>
          </div>
          <hr />
          <div className='inputGuide'>
            <p>
              <span className='highlight'>모델 단어</span>가 결과일 때는 직접
              입력해야 합니다.
            </p>
            <p>
              직접 입력 항목을 입력하실 때 가장 유사하다고 생각하는 단어는{' '}
              <span className='highlight'>콤마(,)를 기준</span>
              으로 제일 앞에 적어 주세요.
            </p>
          </div>
        </>
      )}
    </div>
  );
};

export default HotkeyGuide;
