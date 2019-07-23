const path = require('path');
const webpack = require('webpack');

module.exports = {
    entry: [
        `./assets/js/base.js`,
        `./assets/js/webapp.js`
    ],
    resolve:{
        alias: {
            jquery: "jquery/src/jquery",
            'mapbox-gl': 'mapbox-gl/dist/mapbox-gl',
        }
    },
    mode: 'production',
    output: {
        path: path.join(__dirname, '..', 'static', 'js'),
        publicPath: '/static/js/webapp.js',
        filename: 'webapp.js',
    },
    optimization: {
        minimize: false
    },
    performance:{
        hints: false
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                query: {
                    presets: ['@babel/preset-env', '@babel/preset-react']
                }
            }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            moment: 'moment'
        }),
        new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /de|en/)
    ]
};