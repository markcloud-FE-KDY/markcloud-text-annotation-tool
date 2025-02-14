import { useState, useEffect } from 'react';
import { GrFormPrevious, GrFormNext } from 'react-icons/gr';
import { changeState } from 'js/common';

const Pagination = ({ pageInfo, setPageInfo }) => {
  const [pageGroup, setPageGroup] = useState([]);
  const { totalPage, page } = pageInfo;

  const changePage = p => {
    if (page === p) return;
    else changeState(setPageInfo, 'page', p);
  };
  const changePageGroup = p => {
    const arr = [];
    let first =
      p % 10 === 0
        ? p - 9
        : parseInt(p / 10) === 0
        ? 1
        : parseInt(p / 10) * 10 + 1;
    let last =
      p % 10 === 0
        ? p
        : parseInt(p / 10) === 0
        ? 10
        : parseInt(p / 10) * 10 + 10 > totalPage
        ? totalPage
        : parseInt(p / 10) * 10 + 10;
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
    changePage(
      direction === 'prev'
        ? page - 10
        : page + 10 > totalPage
        ? totalPage
        : page + 10
    );
  };

  useEffect(() => {
    changePageGroup(page);
  }, [pageInfo]);

  const renderPagination = () => {
    const prevCheck = page > 10;
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
          className={`prev ${page >= 11 ? 'active' : 'block'}`}>
          <GrFormPrevious />
        </li>
        {middle}
        <li
          onClick={() => changePara(nextCheck ? 'next' : null)}
          className={`next ${
            totalPage >= 11
              ? pageGroup.includes(totalPage)
                ? 'block'
                : 'active'
              : 'block'
          }`}>
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
        </div>
      ) : (
        ''
      )}
    </>
  );
};

export default Pagination;
