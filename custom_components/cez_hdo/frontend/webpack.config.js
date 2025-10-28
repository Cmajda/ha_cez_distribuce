const path = require('path');

module.exports = {
  entry: './src/cez-hdo-card-working.ts',
  output: {
    filename: 'cez-hdo-card.js',
    path: path.resolve(__dirname, 'dist'),
    clean: true,
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: {
          loader: 'ts-loader',
          options: {
            transpileOnly: true
          }
        },
        exclude: /node_modules/,
      },
    ],
  },
  optimization: {
    minimize: true,
  },
};
