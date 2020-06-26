#!/usr/bin/env zsh

title="Some page"
fname_out="reactpage.html"

cat <<EOF >> ${fname_out}
<!DOCTYPE html>
<html>
  <head>
    <title>${title}</title>
    <meta charset="utf-8"/>
    <script src="https://unpkg.com/react@15/dist/react.min.js"></script>
    <script src="https://unpkg.com/react-dom@15/dist/react-dom.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-core/5.8.38/browser.min.js"></script>
  </head>
  <body>
    <div id="root"/>
    <script type="text/babel">
    </script>
  </body>
</html>
EOF
