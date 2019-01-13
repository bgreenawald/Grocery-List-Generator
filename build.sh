# Ensure that the virtual environment is closed.
deactivate

# Remove exising zip.
rm ~/Documents/Grocery-List-Generator/grocery.zip;

# Zip the virtual environment.
cd venv/lib/python3.6/site-packages/;
zip -r9 ~/Documents/Grocery-List-Generator/grocery.zip .;

# Add the function code.
cd ~/Documents/Grocery-List-Generator/
zip -g grocery.zip creds.py client_secret.json get_items.py lambda_function.py write_items.py;

# Remove the old version of the package on S3
aws s3 rm s3://bhg5yd-grocerylist/grocery.zip;

# Upload the new version of the package to s3
aws s3 cp grocery.zip s3://bhg5yd-grocerylist/grocery.zip;

