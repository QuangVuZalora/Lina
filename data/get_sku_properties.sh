. data/config.sh
echo "$(date): Start query sku's category" >> query.log 2>&1

safe_psql_footer_off "
    select country, sku, product_url, image_url, lq_image_url
    from ds_aggregated.catalog_config
    where status = 'active' and image_url is not null and country = 'sg'
    " > $RECSYS_HOME/data/metadata/sku_properties_sg.csv
echo $Country

echo "$(date): Finish query" >> query.log 2>&1