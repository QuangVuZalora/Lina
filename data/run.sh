. config.sh
cd $RECSYS_HOME

source env_lina/bin/activate
python manage.py collectstatic
deactivate

python data/init.py 

bash data/get_sku_properties.sh

python data/combine_data.py
