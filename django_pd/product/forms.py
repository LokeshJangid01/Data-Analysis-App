# forms.py
from django import forms

class DataForm(forms.Form):
    text_data = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Type your data here...',
             'class': 'form-control form-floating',  # Bootstrap classes
             'rows': '3'  # Optional: Set the number of rows for better display
        }),
        required=False
    )
    file_data = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control form-floating'
        }),
        required=False
    )

                #########################################
                # Add a dropdown to select the graph type
                #########################################
    GRAPH_CHOICES = [
        ('line', 'Line Graph'),
        ('bar', 'Bar Graph'),
        ('pie', 'Pie Chart')
    ]
    graph_type = forms.ChoiceField(choices=GRAPH_CHOICES, required=True, label="Select Graph Type",
                 widget=forms.Select(attrs={
                     'class':"form-select"
                 })                  
                                   )
                #########################################
                # Add a dropdown to select the graph size
                #########################################
    GRAPH_CHOICES = [
        ('S', 'small'),
        ('M', 'medium'),
        ('L', 'large')
    ]
    graph_size = forms.ChoiceField(choices=GRAPH_CHOICES, required=True, label="Select Graph Size",
                widget=forms.Select(attrs={
                     'class':"form-select"
                 }) 
                 )
                #########################################
                # Add a dropdown to select the graph style
                #########################################
    GRAPH_CHOICES = [('Solarize_Light2', 'Solarize_Light2'), ('_classic_test_patch', '_classic_test_patch'), ('_mpl-gallery', '_mpl-gallery'), ('_mpl-gallery-nogrid', '_mpl-gallery-nogrid'), ('bmh', 'bmh'), ('classic', 'classic'), ('dark_background', 'dark_background'), ('fast', 'fast'), ('fivethirtyeight', 'fivethirtyeight'), ('ggplot', 'ggplot'), ('grayscale', 'grayscale'), ('seaborn-v0_8', 'seaborn-v0_8'), ('seaborn-v0_8-bright', 'seaborn-v0_8-bright'), ('seaborn-v0_8-colorblind', 'seaborn-v0_8-colorblind'), ('seaborn-v0_8-dark', 'seaborn-v0_8-dark'), ('seaborn-v0_8-dark-palette', 'seaborn-v0_8-dark-palette'), ('seaborn-v0_8-darkgrid', 'seaborn-v0_8-darkgrid'), ('seaborn-v0_8-deep', 'seaborn-v0_8-deep'), ('seaborn-v0_8-muted', 'seaborn-v0_8-muted'), ('seaborn-v0_8-notebook', 'seaborn-v0_8-notebook'), ('seaborn-v0_8-paper', 'seaborn-v0_8-paper'), ('seaborn-v0_8-pastel', 'seaborn-v0_8-pastel'), ('seaborn-v0_8-poster', 'seaborn-v0_8-poster'), ('seaborn-v0_8-talk', 'seaborn-v0_8-talk'), ('seaborn-v0_8-ticks', 'seaborn-v0_8-ticks'), ('seaborn-v0_8-white', 'seaborn-v0_8-white'), ('seaborn-v0_8-whitegrid', 'seaborn-v0_8-whitegrid'), ('tableau-colorblind10', 'tableau-colorblind10')]
    graph_style = forms.ChoiceField(choices=GRAPH_CHOICES, required=True, label="Select Graph style",
                widget=forms.Select(attrs={
                     'class':"form-select"
                 }) 
                 )

    def clean(self):
        cleaned_data = super().clean()
        text_data = cleaned_data.get('text_data')
        graph_type = cleaned_data.get('graph_type')
        graph_size = cleaned_data.get('graph_size')
        graph_style = cleaned_data.get('graph_style')
        file_data = cleaned_data.get('file_data')

        # if not text_data and not file_data and not graph_type:
        #     raise forms.ValidationError("Please enter data or upload a file.")
        
        return cleaned_data
