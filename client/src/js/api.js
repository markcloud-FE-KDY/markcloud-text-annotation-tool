import axios from 'axios';
import { getCookie, setCookie, removeCookie } from './cookie';

const headers = {
  'Content-Type': 'application/json',
};

// = 마크클라우드 토큰 만료 시 토큰 재발급 API
// const token = async () => {
//   const headers = {
//     'Content-Type': 'application/json',
//     'access-token': getCookie('myToken'),
//     'refresh-token': getCookie('rfToken'),
//   };
//   try {
//     const res = await axios.get('/api/users/self/token', { headers });
//     setCookie('myToken', res.data.data.access_token, {
//       path: '/',
//     });
//     return window.location.reload();
//   } catch (error) {
//     const { detail } = error?.response?.detail;
//     if (detail === 'DuplicateLoginDetection' || detail === 'LoginRequired') {
//       removeCookie('myToken');
//       removeCookie('rfToken');
//       window.location.reload();
//       return alert(
//         `${
//           detail === 'LoginRequired' ? '토큰이 만료 되어' : '중복 로그인이 되어'
//         } 로그아웃 합니다.\n다시 로그인해 주세요.`
//       );
//     }
//   }
// };

const catchError = async error => {
  const { status } = error?.response;
  const { detail } = error?.response?.data;
  switch (status) {
    case 403:
      if (detail?.includes('Invaild Password')) return 'wrongPw';
      else if (detail === 'Invaild User ID') return 'wrongId';
      else if (detail === 'Logins Exceeded') return 'excessLogin';
      else if (detail === 'Retired User') return 'retiredUser';
      // else if (detail === 'AccessTokenExpired') return await token();
      break;
    case 500:
    case 504:
      return 'serverError';
    default:
      return;
  }
};

// = 마크클라우드 로그인 시 필요한 아이피 가져오는 API
// const getIp = async () => {
//   try {
//     const result = await axios.get('https://api.ip.pe.kr/');
//     return result.data;
//   } catch (error) {
//     alert('이상이 발생했습니다.\n잠시 후 다시 시도해주세요.');
//   }
// };

// = 마크클라우드 로그인 API
// export const signIn = async (id, pw) => {
//   const query = {
//     user_id: id,
//     password: pw,
//     login_ip: await getIp(),
//   };
//   try {
//     return await axios.post('/api/auth/login', query);
//   } catch (error) {
//     return catchError(error);
//   }
// };

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
