#!/bin/bash
psql postgres://$1:$2@localhost:5432/$3 <<EOF
\copy car_data (Make,Model,Price,Reg_year,Vehicle_type,Miles,Engine_size,Horsepower,Trans_type,Fuel_type) from '/Database.csv' delimiter ',' CSV HEADER;
EOF
