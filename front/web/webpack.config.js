//const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const ExtractTextPlugin = require("extract-text-webpack-plugin")
const path = require("path")

module.exports = {
    entry: './app.js',
    output: {
      path: path.resolve(__dirname, '../build'),
      filename: 'bundle.js'
    },
    devtool: "source-map",
    plugins: [
        new ExtractTextPlugin ({
            filename: "styles.css"
        }),
      ],
    module: {
        rules: [
            {
                test: /.js?$/,
                exclude: /(node_modules|bower_components)/,
                use: [
                    {
                        loader: "babel-loader",
                        options:{
                            presets: ['stage-0', 'es2015', 'react']
                        }
                    },
                    {
                        loader: "babel-loader",
                        options:{
                            presets: [
                                [
                                    'jsxz',
                                    {
                                        dir: 'webflow'
                                    }
                                ]
                            ],
                            parserOpts: {
                                plugins: [
                                    "jsx","flow","doExpressions","objectRestSpread","classProperties",
                                    "exportExtensions","asyncGenerators","functionBind","functionSent","dynamicImport",
                                    ['decorators', { decoratorsBeforeExport: false, legacy: true }]
                                ]
                            }
                        }
                    }
                ]
            },
            {
                test: /\.css$/,
                use:  ExtractTextPlugin.extract({use: "css-loader"})
            }
        ]
    },
  };