#!/bin/bash

if [ $# -ne 1 ]; then
    echo "引数として実行したい処理名を与えてください。" 1>&2
    echo "  jv_target : jv_target出力csvのMySQLへの取り込み" 1>&2
    echo "  train : ディープラーニング学習" 1>&2
    echo "  predict : ディープラーニング予測" 1>&2
    exit 1
fi

if [ $1 = "jv_target" ]; then
    nkf -wd ../jv_target.csv > ../jv_target_tmp.csv
    python3 set_jvtarget_to_db.py
elif [ $1 = "train" ]; then
    rm -rf /home/noza/keiba/twi/1*.csv*
    rm -rf /home/noza/keiba/twi/2*.csv*
    cp -rf /media/noza/UBUNTU/product/1306*.csv /home/noza/keiba/twi/
    for f in ./[0-9]*.csv;
        do nkf -wd $f > ${f}_tmp;
    done
    python3 dl_input_maker.py
    python3 train.py
elif [ $1 = "predict" ]; then
    rm -rf /home/noza/keiba/twi/1*.csv* 
    rm -rf /home/noza/keiba/twi/2*.csv*
    cp -rf /media/noza/UBUNTU/research/*.csv /home/noza/keiba/twi/
    for f in ./[0-9]*.csv;   
        do nkf -wd $f > ${f}_tmp;
    done            
    python3 dl_input_maker.py
    python3 predict.py
fi
