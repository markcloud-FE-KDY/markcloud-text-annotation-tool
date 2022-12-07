import { useEffect, useState } from 'react';
import $ from 'jquery';
import Calendar from 'react-calendar';
import { RiCloseFill } from 'react-icons/ri';
import { changeState, enterFn, addZero } from 'js/common';
import 'react-calendar/dist/Calendar.css';

const SearchOpt = ({ setSearchOpt, navigate, tf }) => {
  const [opt, setOpt] = useState('calendar');
  const [prevDate, setPrevDate] = useState(new Date());
  const [nextDate, setNextDate] = useState(new Date());
  const [text, setText] = useState('');
  const [prevTime, setPrevTime] = useState({
    part: 'am',
    hour: 12,
    min: 0,
  });
  const [nextTime, setNextTime] = useState({
    part: 'am',
    hour: 12,
    min: 0,
  });

  const outClick = e => {
    if (e.target.className === 'modal-wrap') {
      setSearchOpt(false);
      window.removeEventListener('click', e => outClick(e));
    }
  };

  const calcTime = time => {
    return time.part === 'am'
      ? Number(time.hour) === 12
        ? `00`
        : Number(time.hour) < 10
        ? addZero(time.hour)
        : time.hour
      : Number(time.hour) + 12 === 24
      ? 12
      : Number(time.hour) + 12;
  };

  const setTimeFn = (time, date, setDate) => {
    const day = new Date(date);
    const hour =
      time.part === 'am'
        ? Number(time.hour) === 12
          ? 0
          : Number(time.hour)
        : Number(time.hour) + 12 === 24
        ? 12
        : Number(time.hour) + 12;
    day.setHours(hour, Number(time.min), 0);
    setDate(day);
  };

  useEffect(() => {
    window.addEventListener('click', e => outClick(e));
    setOpt('calendar');
  }, []);

  useEffect(() => {
    if (opt === 'worker' || opt === 'text') setText('');
    if (opt === 'calendar') {
      setPrevDate(new Date());
      setNextDate(new Date());
      setPrevTime({
        part: 'am',
        hour: 12,
        min: 0,
      });
      setNextTime({
        part: 'am',
        hour: 12,
        min: 0,
      });
    }
  }, [opt]);

  useEffect(() => {
    setTimeFn(prevTime, prevDate, setPrevDate);
  }, [prevTime]);

  useEffect(() => {
    setTimeFn(nextTime, nextDate, setNextDate);
  }, [nextTime]);

  useEffect(() => {
    if (opt === 'text' || opt === 'worker') $('.searchInput').focus();
  }, [opt]);

  return (
    <div className='modal-wrap'>
      <div className='modal'>
        <span onClick={() => setSearchOpt(false)}>
          <RiCloseFill />
        </span>
        <ul>
          <li
            className={opt === 'calendar' && 'active'}
            onClick={() => setOpt('calendar')}>
            날짜/시간 검색
          </li>
          <li
            className={opt === 'text' && 'active'}
            onClick={() => setOpt('text')}>
            문자 검색
          </li>
          <li
            className={opt === 'worker' && 'active'}
            onClick={() => setOpt('worker')}>
            검수자 검색
          </li>
        </ul>
        <div className={`section ${opt}`}>
          {opt === 'calendar' && (
            <>
              {' '}
              <div>
                <div>
                  <Calendar
                    value={prevDate}
                    onChange={setPrevDate}
                    calendarType='US'
                    formatDay={(l, date) =>
                      date.toLocaleString('en', { day: 'numeric' })
                    }
                    showNeighboringMonth={false}
                  />
                  <div className='row selectTime'>
                    <select
                      value={prevTime.part}
                      onChange={e =>
                        changeState(setPrevTime, 'part', e.target.value)
                      }>
                      <option value='am'>오전</option>
                      <option value='pm'>오후</option>
                    </select>
                    <select
                      value={prevTime.hour}
                      onChange={e =>
                        changeState(setPrevTime, 'hour', e.target.value)
                      }>
                      {Array(12)
                        .fill(0)
                        .map((i, idx) => {
                          return (
                            <option value={idx + 1}>{addZero(idx + 1)}</option>
                          );
                        })}
                    </select>
                    <span className='hour'>시</span>
                    <select
                      value={prevTime.min}
                      onChange={e =>
                        changeState(setPrevTime, 'min', e.target.value)
                      }>
                      {Array(60)
                        .fill(0)
                        .map((i, idx) => {
                          return <option value={idx}>{addZero(idx)}</option>;
                        })}
                    </select>
                    <span>분</span>
                  </div>
                  <div className='row'>
                    <input
                      type='date'
                      value={`${prevDate.getFullYear()}-${addZero(
                        prevDate.getMonth() + 1
                      )}-${addZero(prevDate.getDate())}`}
                      readOnly
                    />
                    <input
                      type='time'
                      value={`${calcTime(prevTime)}:${addZero(
                        prevTime.min
                      )}:00`}
                      readOnly
                    />
                  </div>
                </div>
                <span>~</span>
                <div>
                  <Calendar
                    value={nextDate}
                    onChange={setNextDate}
                    calendarType='US'
                    formatDay={(l, date) =>
                      date.toLocaleString('en', { day: 'numeric' })
                    }
                    showNeighboringMonth={false}
                  />
                  <div className='row selectTime'>
                    <select
                      value={nextTime.part}
                      onChange={e =>
                        changeState(setNextTime, 'part', e.target.value)
                      }>
                      <option value='am'>오전</option>
                      <option value='pm'>오후</option>
                    </select>
                    <select
                      value={nextTime.hour}
                      onChange={e =>
                        changeState(setNextTime, 'hour', e.target.value)
                      }>
                      {Array(12)
                        .fill(0)
                        .map((i, idx) => {
                          return (
                            <option value={idx + 1}>{addZero(idx + 1)}</option>
                          );
                        })}
                    </select>
                    <span className='hour'>시</span>
                    <select
                      value={nextTime.min}
                      onChange={e =>
                        changeState(setNextTime, 'min', e.target.value)
                      }>
                      {Array(60)
                        .fill(0)
                        .map((i, idx) => {
                          return <option value={idx}>{addZero(idx)}</option>;
                        })}
                    </select>
                    <span>분</span>
                  </div>
                  <div className='row'>
                    <input
                      type='date'
                      value={`${nextDate.getFullYear()}-${addZero(
                        nextDate.getMonth() + 1
                      )}-${addZero(nextDate.getDate())}`}
                      readOnly
                    />
                    <input
                      type='time'
                      value={`${calcTime(nextTime)}:${addZero(
                        nextTime.min
                      )}:00`}
                      readOnly
                    />
                  </div>
                </div>
              </div>
              <button
                onClick={() => {
                  setSearchOpt(false);
                  navigate(
                    `/home/1/calendar/${Math.floor(
                      prevDate / 1000
                    )}&${Math.floor(nextDate / 1000)}`
                  );
                }}>
                검색
              </button>
            </>
          )}
          {(opt === 'text' || opt === 'worker') && (
            <>
              <input
                type='text'
                placeholder='검색어를 입력하세요.'
                className='searchInput'
                value={text}
                onChange={e => setText(e.target.value)}
                onKeyDown={e =>
                  enterFn(e, () => {
                    setSearchOpt(false);
                    navigate(`/home/${opt === 'text' ? 0 : 1}/${opt}/${text}`);
                  })
                }
              />
              <button
                onClick={() => {
                  setSearchOpt(false);
                  navigate(`/home/${opt === 'text' ? 0 : 1}/${opt}/${text}`);
                }}>
                검색 
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchOpt;
