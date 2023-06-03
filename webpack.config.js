const path = require('path');

module.exports = {
  entry: './assets/scripts/index.js',  // path to our input file
  output: {
    filename: 'index-bundle.js',  // output bundle file name
    path: path.resolve(__dirname, 'network', 'static', 'network'),  // path to our Django static directory
  },
  optimization: {
    minimize: true
  }
};