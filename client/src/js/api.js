import axios from 'axios';
import { getCookie } from './cookie';

// = 에러 핸들링
const catchError = async error => {
  const { status } = error?.response;
  const { detail } = error?.response?.data;
  switch (status) {
    case 403:
      if (detail?.includes('Invaild Password')) return 'wrongPw';
      else if (detail === 'Invaild User ID') return 'wrongId';
      else if (detail === 'Logins Exceeded') return 'excessLogin';
      else if (detail === 'Retired User') return 'retiredUser';
      break;
    case 500:
    case 504:
      return 'serverError';
    default:
      return;
  }
};

// = 지원님 로그인 API
export const signIn = async (id, pw) => {
  try {
    return await axios.post(
      `/markdict/login`,
      `grant_type=&username=${id}&password=${pw}&scope=&client_id=&client_secret=`,
      { 'Content-Type': 'application/x-www-form-urlencoded' }
    );
  } catch (error) {
    return catchError(error);
  }
};

// = 텍스트 리스트 불러오기
export const getList = async (
  { page, limit },
  select,
  keyword,
  worker,
  date_start,
  date_end
) => {
  try {
    return await axios.get(
      `/markdict/list_search?page=${page - 1}&size=${limit}&tf=${select}${
        keyword ? `&keyword=${keyword}` : ''
      }${worker ? `&worker=${worker}` : ''}&date_start=${
        date_start ? `${date_start}` : '0'
      }&date_end=${date_end ? `${date_end}` : '0'}`
    );
  } catch (error) {
    return catchError(error);
  }
};

// = 텍스트 상세내역 불러오기
export const getTextDetail = async (
  oid,
  select,
  keyword,
  worker,
  date_start,
  date_end
) => {
  try {
    return await axios.get(
      `/markdict/detail?oid=${oid}&tf=${select}${
        keyword ? `&keyword=${keyword}` : ''
      }${worker ? `&worker=${worker}` : ''}&date_start=${
        date_start ? `${date_start}` : '0'
      }&date_end=${date_end ? `${date_end}` : '0'}`
    );
  } catch (error) {
    return catchError(error);
  }
};

// = 텍스트 상세내역 업데이트
export const modifyText = async (oid, pass, data) => {
  const headers = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${getCookie('myToken')}`,
  };
  try {
    return await axios.post(`/markdict/update?oid=${oid}&_pass=${pass}`, data, {
      headers,
    });
  } catch (error) {
    return catchError(error);
  }
};
