#!/bin/bash

if [ $# -ne 1 ]; then
    echo "引数として実行したい処理名を与えてください。" 1>&2
    echo "  jv_target : jv_target出力csvのMySQLへの取り込み" 1>&2
    echo "  train : ディープラーニング学習" 1>&2
    echo "  predict : ディープラーニング予測" 1>&2
    exit 1
fi

rm -rf /home/noza/keiba/twi/1*.csv*
rm -rf /home/noza/keiba/twi/2*.csv*
if [ $1 = "jv_target" ]; then
    nkf -wd /media/noza/UBUNTU/source/jv_target.csv > ./jv_target_tmp.csv
    python3 set_jvtarget_to_db.py
elif [ $1 = "train_init" ]; then
    cp -rf /media/noza/UBUNTU/product/*.csv /home/noza/keiba/twi/
    for f in ./[0-9]*.csv;
        do nkf -wd $f > ${f}_tmp;
    done
    python3 dl_input_maker.py
    python3 train.py
elif [ $1 = "train" ]; then
    cp -rf /media/noza/UBUNTU/deep_model/* /home/noza/keiba/twi/
    python3 train.py
elif [ $1 = "predict" -o $1 = "honban" ]; then
    if [ $1 = "predict" ]; then
        cp -rf /media/noza/UBUNTU/research/*.csv /home/noza/keiba/twi/
    elif [ $1 = "honban" ]; then
        cp -rf /media/noza/UBUNTU/honban/*.csv /home/noza/keiba/twi/
    fi
    for f in ./[0-9]*.csv;   
        do nkf -wd $f > ${f}_tmp;
    done            
    python3 dl_input_maker.py
    python3 predict.py
fi
