import { useState, useEffect } from 'react';
import $ from 'jquery';
import { GrFormPrevious, GrFormNext } from 'react-icons/gr';
import { changeState, enterFn } from 'js/common';

const Pagination = ({ pageInfo, setPageInfo }) => {
  const [pageGroup, setPageGroup] = useState([]);
  const { totalPage, page } = pageInfo;
  const [movePage, setMovePage] = useState(page);

  const pageSearch = () => {
    if (movePage > totalPage || movePage === '0') {
      setMovePage(page);
      $('.pageInput').focus();
      if (movePage > totalPage)
        alert(
          '입력하신 숫자가 총 페이지 수보다 더 큽니다.\n다시 입력해 주세요.'
        );
      else if (movePage === '0')
        alert('잘못된 입력입니다.\n다시 입력해 주세요.');
      return;
    }
    changePage(Number(movePage));
  };

  const changePage = p => {
    if (page === p) return;
    else {
      changeState(setPageInfo, 'page', p);
      setMovePage('');
    }
  };
  const changePageGroup = p => {
    const arr = [];
    let first = p - 4;
    let last = p + 4;
    if (p <= 5) {
      first = 1;
      last = 9;
    }
    if (p >= totalPage - 4) {
      first = totalPage - 8;
      last = totalPage;
    }
    if (totalPage < 10) {
      first = 1;
      last = totalPage;
    }
    for (let i = first; i < last + 1; i++) {
      arr.push(i);
    }
    setPageGroup(arr);
  };
  const changePara = direction => {
    if (!direction) return;
    changePage(direction === 'prev' ? page - 1 : page + 1);
  };

  useEffect(() => {
    changePageGroup(page);
  }, [pageInfo]);

  const renderPagination = () => {
    const prevCheck = page > 1;
    const middle = pageGroup.reduce((acc, nowPage) => {
      return (
        <>
          {acc}
          <li
            onClick={() => changePage(nowPage)}
            className={nowPage === page && 'now'}>
            {nowPage}
          </li>
        </>
      );
    }, <></>);
    const nextCheck = page < totalPage;
    return (
      <>
        <li
          onClick={() => changePara(prevCheck ? 'prev' : null)}
          className={`prev ${page === 1 ? 'block' : 'active'}`}>
          <GrFormPrevious />
        </li>
        {middle}
        <li
          onClick={() => changePara(nextCheck ? 'next' : null)}
          className={`next ${totalPage === page ? 'block' : 'active'}`}>
          <GrFormNext />
        </li>
      </>
    );
  };
  return (
    <>
      {pageInfo.totalPage > 1 ? (
        <div className='paging row'>
          <ul className='pagination row'>{renderPagination()}</ul>
          <div className='pageInput'>
            <span>
              <input
                type='text'
                className='pageInput'
                value={movePage}
                onChange={e => setMovePage(e.target.value)}
                onKeyDown={e => enterFn(e, pageSearch)}
              />{' '}
              / {totalPage}
            </span>
            <button onClick={pageSearch}>이동</button>
          </div>
        </div>
      ) : (
        ''
      )}
    </>
  );
};

export default Pagination;
