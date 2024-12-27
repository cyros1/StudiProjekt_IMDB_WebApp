module.exports = {
  mode: 'jit',
  content: [
      './IMBD_app/templates/**/*.html',
      './IMBD_app/static/**/*.js',
  ],
  theme: {
      extend: {
        colors:{
          "dark-purple": "#4E299B",
          "light-pink": "#DF99D8",
          "search-bar-pink": "#c686ce",
          "search-bar-purple": "#7245aa"
        },
      },
  },
  plugins: [],
};
