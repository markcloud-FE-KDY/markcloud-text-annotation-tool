import Cookies from 'universal-cookie';

const cookies = new Cookies();

export const setCookie = (name, value, option) => {
  cookies.set(name, value, { ...option });
};

export const getCookie = name => cookies.get(name);

export const removeCookie = (name, option) => {
  cookies.remove(name, { ...option });
};
