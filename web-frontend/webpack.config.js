const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const { resolve, jpom } = require("path");

module.exports = {
  entry: "./src/ts/index.ts",
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.scss$/,
        use: ["style-loader", "css-loader", "sass-loader"],
      },
    ],
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },
  output: {
    filename: "bundle.js",
    path: resolve(__dirname, "dist"),
    publicPath: "/",
  },
  devServer: {
    static: {
      directory: resolve(__dirname, "static"),
    },
    port: 8000,
    open: true,
    hot: true,
  },
  plugins: [
    new HtmlWebpackPlugin({
      filename: "./index.html",
      template: resolve(__dirname, "./static/main.html"),
      inject: "body",
    }),

  ],
};
