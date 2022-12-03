#!/bin/bash

for incfile in data/scripts/*.inc ; do
    poryfile="${incfile::-4}.pory"
    echo "Converting: $incfile"
    touch $poryfile
    echo 'raw `' >> $poryfile
    cat $incfile >> $poryfile
    echo '`' >> $poryfile
done