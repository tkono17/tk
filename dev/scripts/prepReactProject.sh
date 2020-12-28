#!/usr/bin/env bash

function help() {
    echo "Usage: $0 <ProjectName>"
    echo "Examples:"
    echo "> $0 MyProject"
    echo "(This will create a directory called MyProject with initial files)"
    echo "> $0 ."
    echo "(This will create the initial files here)"
}

function createInitFiles() {
    cat <<EOF > webpack.config.js
const path = require('path')
module.exports = {
  entry: {
    'index': './src/index.js'
  },
  output: {
    path: path.resolve(__dirname, 'dist'), 
    filename: '[name].js'
  },
  module: {
    rules: [
      {
	exclude: /node_modules/,
	use: [
	  {
	    loader: 'babel-loader'
	  }
	]
      }
    ]
  },
  resolve: {
    extensions: [ '.js', 'jsx' ]
  }
}
EOF
    mkdir src dist html
    cat <<EOF > html/index.html
<html>
  <head>
    <meta charset="utf-8"></meta>
    <title>Paper stack application</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="text/javascript" src="../dist/index.js"></script>
  </body>
</html>
EOF
    cat <<EOF > src/index.js
import React from 'react'
import ReactDOM from 'react-dom'

ReactDOM.render(<h1>Paper stack application (1.0.0)</h1>, 
                document.getElementById('root'))
EOF
    cat <<EOF > .babelrc
{
  "presets": [ "@babel/preset-env", "@babel/preset-react" ]
}
EOF
}

if [[ $# == 0 ]]; then
    help
    exit 1
fi

pname=$1

dir0=$(pwd)
if [[ $pname == '.' ]]; then
    pname=$(basename ${dir0})
else
    mkdir $pname
    cd $pname
fi
npm init -y
createInitFiles
echo "Execute initReactWebpack.sh to install Node packages"
cd ${dir0}
