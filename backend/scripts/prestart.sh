#! /usr/bin/env sh

i=0
while [ $i -lt 6 ];
do
echo "Running inside /backend/src/scripts/prestart.sh - Let the DB start:" $i "seconds from 5";
i=$((i+1))
sleep 1;
done

python scripts/create_tables.py

