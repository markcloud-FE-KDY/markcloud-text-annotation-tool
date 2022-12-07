const { createProxyMiddleware } = require('http-proxy-middleware');

const inspect = 'http://192.168.0.44:8000/';
const user = 'http://192.168.0.25:5555/';

module.exports = app => {
  app.use(
    '/markdict',
    createProxyMiddleware({
      target: inspect,
      changeOrigin: true,
    })
  );
  app.use(
    '/api',
    createProxyMiddleware({
      target: user,
      changeOrigin: true,
    })
  );
};
