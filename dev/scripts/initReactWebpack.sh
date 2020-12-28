#!/usr/bin/env bash

declare -a packagesDev=(
    react react-dom webpack webpack-cli
    @babel/core @babel/preset-env @babel/preset-react babel-loader
)
npm install --save-dev ${packagesDev[@]}
