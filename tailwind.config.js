module.exports = {
  purge: {
    enabled: true,
    content:[
      "./templates/*.html"
    ]
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors:{
          'blue_nav': '#2B3A67',
          'dark_ele_blue':'#496A81',
          'cadet_blue':'#66999B',
          'heathered-gray': {
            DEFAULT: '#B3AF8F',
            '50': '#FFFFFF',
            '100': '#FFFFFF',
            '200': '#F1F0EA',
            '300': '#DCDACC',
            '400': '#C8C5AD',
            '500': '#B3AF8F',
            '600': '#9E9971',
            '700': '#837E59',
            '800': '#656144',
            '900': '#464430'
          },
          'macaroni-and-cheese': {
            DEFAULT: '#FFC482',
            '50': '#FFFFFF',
            '100': '#FFFFFF',
            '200': '#FFFFFF',
            '300': '#FFF4E8',
            '400': '#FFDCB5',
            '500': '#FFC482',
            '600': '#FFAC4F',
            '700': '#FF941C',
            '800': '#E87A00',
            '900': '#B56000'
          },
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
