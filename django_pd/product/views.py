from django.shortcuts import render
from .models import Product,Purchase
import pandas as pd
from django.http import HttpResponse
from .forms import DataForm
import io


# Create your views here.
# def chart_select_view(request):
#     product_df = pd.DataFrame(Product.objects.all().values())
#     #qs2 = Product.objects.all().values_list()
#     purchase_df = pd.DataFrame(Purchase.objects.all().values())
#     product_df['product_id'] = product_df['id']
#     df = pd.merge(purchase_df,product_df,on='product_id').drop(['id_y','date_y'],axis=1).rename({'id_x':'id','date_x':'date'},axis=1)
    
#     #print(qs2)
#     context = {
#         'products':product_df.to_html(),
#         'purchase':purchase_df.to_html(),
#         'df':df.to_html(),
#     }
    
    
    
#     return render(request,'product/main.html',context)
def home(request):
    table_data = None  # Ensure table_data is always defined
    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES)
        if form.is_valid():
            text_data = form.cleaned_data.get('text_data')
            file_data = form.cleaned_data.get('file_data')
            
            # Print text data if available
            # Handle text data as a sequence of numbers
            if text_data:
                # Convert the text data into a list of numbers
                try:
                    # numbers = list(map(int, text_data.split(',')))
                    # data_frame = pd.DataFrame(numbers, columns=["Number"])
                    data = pd.Series([int(num) for num in text_data.split(',')])
                except ValueError:
                    return HttpResponse("Please enter a valid sequence of numbers separated by commas.")

            # Print file data if available
            if file_data:
                try:
                    # Determine file type and load with pandas
                    if file_data.name.endswith('.csv'):
                        data = pd.read_csv(file_data)
                    elif file_data.name.endswith(('.xls', '.xlsx')):
                        data = pd.read_excel(file_data)
                    else:
                        return HttpResponse("Unsupported file format.")
                    
                    print("File Data:\n", data)
                except Exception as e:
                    return HttpResponse(f"Error processing file: {e}")
            
            # return HttpResponse("Data received. Check console for output.")
            # Convert DataFrame to HTML table for rendering
            if data is not None:
                table_data = data.reset_index().values.tolist()  # Convert to list of [index, value] pairs
            #table_html = data_frame.to_html(index=True)  # index=True to show default pandas indexes

            # return render(request, 'product/table.html', {'table_html': table_html})
        
    
    else:
        form = DataForm()
    
    return render(request, 'product/home.html', {
        'form': form,
        'table_data': table_data
        })