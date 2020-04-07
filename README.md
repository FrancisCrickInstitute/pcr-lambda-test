# pcr-lambda-functions

### Notes:

- increase memory in lambda

- for xlsToCSV.py build python dependency package locally and zip with it lambda_function.py

- for pcr_tests.py use this   arn:aws:lambda:eu-west-2:113088814899:layer:Klayers-python37-pandas:1 for a layer


#### list of packages required for xlstoCSV and use linux versions

- pandas
- numpy
- xlrd



for package dependency follow
[https://medium.com/@korniichuk/lambda-with-pandas-fd81aa2ff25e](https://medium.com/@korniichuk/lambda-with-pandas-fd81aa2ff25e)


