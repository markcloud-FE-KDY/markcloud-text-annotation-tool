import { useEffect, useState } from 'react';
import { IoSearchCircleSharp } from 'react-icons/io5';
import { AiOutlineCloseCircle } from 'react-icons/ai';
import { useNavigate, useParams, Link } from 'react-router-dom';
import SearchOpt from 'components/SearchOpt';
import Pagination from 'components/Pagination';
import ViewMode from 'components/ViewMode';
import { getList } from 'js/api';
import { getCookie, removeCookie } from 'js/cookie';
import { changeState, catchErrorHandler, addZero } from 'js/common';

const TextList = ({ mode, setMode }) => {
  const [searchOpt, setSearchOpt] = useState(false);
  const [list, setList] = useState([]);
  const { tf, option, word } = useParams();
  const [pageInfo, setPageInfo] = useState({
    page: 1,
    totalPage: 1,
    limit: 20,
    total: 0,
  });
  const prevDate = new Date(word?.split('&')[0] * 1000);
  const nextDate = new Date(word?.split('&')[1] * 1000);
  let prevent = false;
  const navigate = useNavigate();

  useEffect(() => {
    document.title = '마크클라우드 텍스트 검수 > 홈';
  }, []);

  const getTextList = async () => {
    if (prevent) return;
    prevent = true;
    setTimeout(() => {
      prevent = false;
    }, 200);
    const result = await getList(pageInfo, tf);
    if (typeof result === 'object') {
      setList(result?.data?.data);
      setPageInfo(prev => {
        const clone = { ...prev };
        clone.totalPage = result?.data?.meta?.page_count;
        clone.total = result?.data?.meta?.total;
        return clone;
      });
    } else return catchErrorHandler(result);
  };

  const searchList = async () => {
    if (!option && !word) return;
    let result;
    if (option === 'text') result = await getList(pageInfo, tf, word);
    else if (option === 'worker')
      result = await getList(pageInfo, tf, false, word);
    else if (option === 'calendar') {
      const date = word.split('&');
      result = await getList(pageInfo, tf, false, false, date[0], date[1]);
    }
    if (typeof result === 'object') {
      setList(result?.data?.data);
      setPageInfo(prev => {
        const clone = { ...prev };
        clone.totalPage = result?.data?.meta?.page_count;
        clone.total = result?.data?.meta?.total;
        return clone;
      });
    } else return catchErrorHandler(result);
  };

  const unix2time = t => {
    const date = new Date(t * 1000);
    return `${date.getFullYear()}-${addZero(date.getMonth() + 1)}-${addZero(
      date.getDate()
    )} ${addZero(date.getHours())}:${addZero(date.getMinutes())}`;
  };

  const returnDateStamp = d => {
    return `${d.getFullYear()}-${addZero(d.getMonth() + 1)}-${addZero(
      d.getDate()
    )} ${d.getHours() < 12 ? '오전' : '오후'} ${
      d.getHours() === 0
        ? addZero(Number(d.getHours()) + 12)
        : addZero(d.getHours() < 12)
        ? addZero(Number(d.getHours()))
        : addZero(Number(d.getHours()) - 12)
    }:${addZero(d.getMinutes())}`;
  };

  const renderTableFn = () => {
    return list.reduce(
      (
        acc,
        {
          id,
          index,
          originalEng,
          productNameEng,
          modelResult,
          directInput,
          humanCheck,
          worker,
          resultStatus,
          dateModified,
          passCheck,
        },
        idx
      ) => {
        return (
          <>
            {acc}
            <Link></Link>
            <tr
              className={idx % 2 === 1 ? 'odd' : 'even'}
              onClick={() =>
                option && word
                  ? navigate(`/detail/${tf}/${option}/${word}/${id}`)
                  : navigate(`/detail/${tf}/${id}`)
              }>
              <td className='tablet-none'>{index}</td>
              <td>{originalEng}</td>
              <td>{productNameEng}</td>
              <td>
                {humanCheck
                  ? directInput?.length === 0
                    ? modelResult
                    : directInput
                  : modelResult}
              </td>
              {humanCheck ? (
                <>
                  {Number(tf) === 1 && (
                    <td>
                      {(resultStatus === 'direct' && '직접') ||
                        (resultStatus === 'model' && '모델') ||
                        (resultStatus === 'candidate' && '후보') ||
                        (resultStatus === 'original' && '기본')}
                    </td>
                  )}
                  <td className='tablet-none'>{worker}</td>
                  <td className='tablet-none'>{unix2time(dateModified)}</td>
                </>
              ) : (
                <>
                  {(Number(tf) === 1 || Number(tf) === 6) && (
                    <>
                      {' '}
                      <td className='tablet-none'>미완료</td>
                      <td className='tablet-none'>미완료</td>
                    </>
                  )}
                </>
              )}
              <td
                className={`mobile-none ${
                  humanCheck ? 'complete' : passCheck ? 'pass' : 'inComplete'
                }`}>
                {humanCheck ? '완료' : passCheck ? '보류중' : '미완료'}
              </td>
            </tr>
          </>
        );
      },
      <></>
    );
  };

  useEffect(() => {
    if (!getCookie('myToken')) {
      navigate('/');
      return alert('로그인이 필요한 서비스입니다.');
    }
  }, []);

  useEffect(() => {
    if (option && word) searchList();
    else getTextList();
  }, [pageInfo.page, pageInfo.limit, tf, option, word]);

  useEffect(() => {
    changeState(setPageInfo, 'page', 1);
  }, [tf]);

  return (
    <>
      <ViewMode mode={mode} setMode={setMode} />
      <div className='content-wrap home'>
        <div className='header'>
          <div
            className='title'
            onClick={() => {
              navigate('/home/0');
              changeState(setPageInfo, 'page', 1);
            }}>
            <h1>TEXT</h1>
            <h1>LIST</h1>
          </div>
          <div className='menu'>
            {option && word.length && option === 'text' ? (
              <div className='search'>
                <span>검색어</span>
                <span>
                  {word}
                  <AiOutlineCloseCircle
                    onClick={() => navigate(`/home/${tf}`)}
                  />
                </span>
              </div>
            ) : (
              ''
            )}
            {option && word.length && option === 'worker' ? (
              <div className='search'>
                <span>검수자</span>
                <span>
                  {word}
                  <AiOutlineCloseCircle onClick={() => navigate(`/home/0`)} />
                </span>
              </div>
            ) : (
              ''
            )}
            {word && option === 'calendar' ? (
              <div className='search'>
                <span>검색 범위</span>
                <span>
                  {returnDateStamp(prevDate)} ~ {returnDateStamp(nextDate)}
                  <AiOutlineCloseCircle onClick={() => navigate(`/home/0`)} />
                </span>
              </div>
            ) : (
              ''
            )}
            <select
              value={tf}
              onChange={e =>
                option && word
                  ? navigate(`/home/${e.target.value}/${option}/${word}`)
                  : navigate(`/home/${e.target.value}`)
              }
              className='firstSelect'>
              <option value={0}>검수 미완료만 보기</option>
              <option value={1}>검수 완료만 보기(전체)</option>
              <option value={2}>검수 완료만 보기(모델)</option>
              <option value={3}>검수 완료만 보기(후보)</option>
              <option value={4}>검수 완료만 보기(직접)</option>
              <option value={5}>검수 보류만 보기</option>
              <option value={6}>전체 보기</option>
            </select>
            <select
              value={pageInfo.limit}
              onChange={e => changeState(setPageInfo, 'limit', e.target.value)}>
              <option value={20}>20개씩 보기</option>
              <option value={50}>50개씩 보기</option>
              <option value={100}>100개씩 보기</option>
            </select>
            <button
              onClick={() => {
                setSearchOpt(true);
              }}
              className='mobile-none'>
              <IoSearchCircleSharp />
            </button>
            <button
              className='logout'
              onClick={() => {
                removeCookie('myToken', { path: '/' });
                return navigate('/');
              }}>
              로그아웃
            </button>
          </div>
        </div>
        <div className='totalCount'>
          <span>전체 데이터 개수:</span>
          <span>{pageInfo?.total.toLocaleString()}</span>
          <span>개</span>
        </div>
        <div className='content'>
          {list?.length ? (
            <div className='table-wrap'>
              <table>
                <colgroup>
                  <col width='5%' className='tablet-none' />
                  <col width='15%' />
                  <col width='15%' />
                  <col
                    width={Number(tf) === 1 || Number(tf) === 6 ? '20%' : '25%'}
                  />
                  {(Number(tf) === 1 || Number(tf) === 6) && (
                    <>
                      {Number(tf) === 1 && <col width='5%' />}
                      <col width='10%' className='tablet-none' />
                      <col width='15%' className='tablet-none' />
                    </>
                  )}
                  <col width='10%' className='mobile-none' />
                </colgroup>
                <thead>
                  <tr>
                    <th className='tablet-none'>ID</th>
                    <th>원본 영어</th>
                    <th>1차 가공 영어</th>
                    {Number(tf) === 0 || Number(tf) === 5 ? (
                      <th>후보 단어</th>
                    ) : (
                      <>
                        <th>결과</th>
                        {Number(tf) === 1 && <th>종류</th>}
                        <th className='tablet-none'>검수자</th>
                        <th className='tablet-none'>검수 날짜</th>
                      </>
                    )}
                    <th className='mobile-none'>검수 여부</th>
                  </tr>
                </thead>
                <tbody>{renderTableFn()}</tbody>
              </table>
            </div>
          ) : (
            <div className='none-list'>목록이 없습니다.</div>
          )}
        </div>
        <Pagination pageInfo={pageInfo} setPageInfo={setPageInfo} />
      </div>
      {searchOpt && (
        <SearchOpt setSearchOpt={setSearchOpt} navigate={navigate} tf={tf} />
      )}
    </>
  );
};

export default TextList;
