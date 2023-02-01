const { createProxyMiddleware } = require('http-proxy-middleware');

const inspect = 'http://192.168.0.44:8001/';

module.exports = app => {
  app.use(
    '/markdict',
    createProxyMiddleware({
      target: inspect,
      changeOrigin: true,
    })
  );
};
