#!/bin/bash
for file in $(find . -name "*.html") $(find . -name "*.py")
do
    filename=$(basename $file)
    echo "Filtering $file..."
    sed -e "s/\/BHMcalc\///g" $file > /tmp/$filename
    sed -e "s/\/\//\//g" /tmp/$filename > $file
done
