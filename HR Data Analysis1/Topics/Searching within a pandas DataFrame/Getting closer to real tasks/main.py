# your code here. the dataset is already loaded as sales_data.

print(sales_data.query("Category in ('Technology', 'Furniture') & `Sales` < 25"))