module.exports = {
  devServer: {
    proxy: 'https://localhost:8888'
  },
  publicPath: "",
  productionSourceMap: false, // to hide source code
  pluginOptions: {
    sitemap: {
      urls: [
        "https://www.stickydo.us/",
        "https://www.stickydo.us/login",
        "https://www.stickydo.us/register",
      ],
    },
  },
};
