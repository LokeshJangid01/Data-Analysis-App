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
                ###############################
                #          LINE GRAPH         #
                ###############################
                # Create the plot with customizations
                plt.figure(figsize=(8, 5))  # Custom size plt.style.use('ggplot')
                plt.style.use('ggplot')
                
                ax = plt.gca()  # Get current axes
                ax.set_facecolor('#0f0f0f')  # Set plot (axes) background color
                plt.plot(data, color='green', linewidth=2, marker='o', markersize=5)  # Line style
                plt.title("Customized Line Graph of Input Data", fontsize=16, color='darkblue')  # Title customization
                plt.xlabel("Index", fontsize=12, color='gray')
                plt.ylabel("Value", fontsize=12, color='gray')
                # plt.grid(True, linestyle=':', color='lightgray')  # Custom grid style
                
                # Save plot to an in-memory bytes buffer
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                
                # Encode the buffer to a base64 string to embed in HTML
                line_graph_url = base64.b64encode(buffer.getvalue()).decode('utf-8')
                buffer.close()
                plt.close()  # Close the plot to free memory
                ###############################
                #          BAR GRAPH         #
                ###############################   
                # Create the plot
                # Create a bar chart using plt.bar()
                # plt.bar(data.index, data.values, color='skyblue', edgecolor='black')
                # plt.style.use('grayscale')
                # plt.title("Bar Chart of Input Data", fontsize=16, color='darkblue')
                # plt.xlabel("Index", fontsize=12, color='gray')
                # plt.ylabel("Value", fontsize=12, color='gray')
                # plt.grid(axis='y', linestyle=':', color='lightgray')  # Grid on the y-axis only
                #######################
                #       styles        #
                #######################
                """
                print(plt.style.available)
                    ['bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-dark', 'tableau-colorblind10', ...]

                """
                plt.style.use('tableau-colorblind10')
                plt.bar(data.index,data.values)
                plt.title("Bar Chart of Input Data")
                plt.xlabel("Index")
                plt.ylabel("Value")


                
                # Save plot to an in-memory bytes buffer
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                
                # Encode the buffer to a base64 string to embed in HTML
                bar_graph_url = base64.b64encode(buffer.getvalue()).decode('utf-8')
                buffer.close()
                plt.close()  # Close the plot to free memory
                ###############################
                #          PIE GRAPH         #
                ###############################   
                # Create the plot
                plt.figure(figsize=(8, 5), facecolor='#f5f5f5')
                plt.style.use('grayscale')
                # Create a pie chart using plt.pie()
                plt.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
                plt.title("Pie Chart of Input Data", fontsize=16, color='darkblue')
                # plt.figure()
                # plt.style.use('ggplot')
                # data.plot(kind='pie')
                # plt.title("Pie Graph of Input Data")
                # plt.xlabel("Index")
                # plt.ylabel("Value")
                
                # Save plot to an in-memory bytes buffer
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                
                # Encode the buffer to a base64 string to embed in HTML
                pie_graph_url = base64.b64encode(buffer.getvalue()).decode('utf-8')
                buffer.close()
                plt.close()  # Close the plot to free memory
                             
            #table_html = data_frame.to_html(index=True)  # index=True to show default pandas indexes

            return render(request, 'product/Dataview.html', {
                'table_data': table_data,
                'line_graph_url': line_graph_url , # Pass graph URL to the template
                'bar_graph_url': bar_graph_url,  # Pass bar graph URL to the template
                'pie_graph_url': pie_graph_url  # Pass bar graph URL to the template
                })
        
    
    else:
        form = DataForm()
    
    return render(request, 'product/home.html', {
        'form': form,
        
        })