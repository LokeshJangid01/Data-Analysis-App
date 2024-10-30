from django.shortcuts import render
from .models import Product,Purchase
import pandas as pd
from django.http import HttpResponse
from .forms import DataForm
import matplotlib
matplotlib.use('Agg')  # Set backend to Agg for non-GUI environments
import matplotlib.pyplot as plt
import io
import base64


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
    # print(plt.style.available)
    GRAPH_CHOICES = {c:c for c in plt.style.available}
    
    
    table_data = None  # Ensure table_data is always defined
    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES)
        if form.is_valid():
            text_data = form.cleaned_data.get('text_data')
            file_data = form.cleaned_data.get('file_data')
            graph_type = form.cleaned_data.get('graph_type')  # Get selected graph type
            graph_size = form.cleaned_data.get('graph_size')  # Get selected graph size
            graph_style = form.cleaned_data.get('graph_style')  # Get selected graph style
            # print(graph_style)
            
            
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
            figsize = None
            if graph_size == 'S':
                figsize = (5,3)
            elif graph_size == 'M':
                figsize = (8,5)
            else:
                figsize = (12,8)
            # Generate the selected graph
            if data is not None:
                buffer = io.BytesIO()
                plt.figure(figsize=figsize)
                
                if graph_type == 'line':
                    plt.style.use(GRAPH_CHOICES[graph_style])
                    plt.plot(data, linewidth=2, marker='o', markersize=5)
                    plt.title("Line Graph")
                    
                    
                
                elif graph_type == 'bar':
                    plt.style.use(GRAPH_CHOICES[graph_style])
                    plt.bar(data.index, data.values)
                    plt.title("Bar Chart")
                    
                
                elif graph_type == 'pie':
                    plt.style.use(GRAPH_CHOICES[graph_style])
                    plt.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
                    plt.title("Pie Chart")
                
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                
                # Convert to base64 to display in HTML
                graph_url = base64.b64encode(buffer.getvalue()).decode('utf-8')
                buffer.close()
                plt.close()
                # print(graph_url)

            return render(request, 'product/Dataview.html', {
                'table_data': data.reset_index().values.tolist(),
                'graph_url': graph_url  # Pass selected graph URL to the template
            })
        
    
    else:
        form = DataForm()
    
    return render(request, 'product/home.html', {
        'form': form,
        
        })