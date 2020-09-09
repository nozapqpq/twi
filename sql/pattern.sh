for f in ../[0-9]*.csv;
do nkf -wd $f > ${f}_tmp;
done
python3 run.py
