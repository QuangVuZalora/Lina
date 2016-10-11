# cd /home/vu/projects/Lina/src
cd /home/ubuntu/Lina

source env_lina/bin/activate 

python data/init.py 

bash data/get_sku_properties.sh

python data/combine_data.py
