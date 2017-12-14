#!/usr/bin/env zsh

if [[ $TK_ROOT == "" ]]; then
    echo "Environment variable TK_ROOT not set"
    exit 1
fi

mkdir -p $TK_ROOT/bin
mkdir -p $TK_ROOT/lib
mkdir -p $TK_ROOT/include
mkdir -p $TK_ROOT/python


