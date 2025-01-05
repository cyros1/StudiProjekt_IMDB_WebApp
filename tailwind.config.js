module.exports = {
  mode: 'jit',
  content: [
      './IMBD_app/templates/**/*.html',
      './IMBD_app/static/**/*.js',
      './IMBD_app/static/**/*.css',
  ],
  theme: {
      extend: {
        height: {
          'logo-large': '50rem', // Custom height for the logo
        },
        colors:{
          "dark-purple": "#4E299B",
          "light-pink": "#DF99D8",
          "search-bar-pink": "#c686ce",
          "search-bar-purple": "#7245aa",
          // cards+create colors:
          "footer-purple": "#2D1E35",
          "f-lighter-purple": "#402B4C",
          "f-border-purple": "#362242",
          "text-white": "#DDD1DD",
          //submit colors:
          "submit-button": "#5F3C71",
          "hover-button": "#7A4D94"
        },
      },
  },
  plugins: [],
};
