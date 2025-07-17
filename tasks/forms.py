from django import forms
from tasks.models import Task, TaskDetail

# Django Basic Form
# class TaskForm(forms.Form):
#     title = forms.CharField(max_length=250,label='Task Title')
#     description = forms.CharField(widget=forms.Textarea, label='Task Description')
#     due_date = forms.DateField(widget=forms.SelectDateWidget, label='Due Date')
#     assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[], label='Assigned To')


#     def __init__(self, *args, **kwargs):
#         # print(args,kwargs)
#         employees=kwargs.pop('employees',[])
#         print(employees)
#         super().__init__(*args, **kwargs)
#         self.fields['assigned_to'].choices=[(emp.id, emp.name) for emp in employees]

# Django FormModel

"""Form Mixing"""
class StyleFormMixing:

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    """ Mixing to apply style to Form field """
    default_classes = "w-full border-2 rounded-lg p-2"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':"border-2 rounded-lg",
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"border-2 rounded-lg p-4",
                    'placeholder':f"Enter {field.label}"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })


class TaskModelForm(StyleFormMixing, forms.ModelForm):
    class Meta:
        model = Task
        # fields = '__all__'
        fields = ['title','description','due_date','assigned_to'] #add 'assigned_to'
        # exclude = ['project','is_completed','created_at','updated_at']
        # define widgets which is not 
        widgets={
            'due_date':forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }
        """ Manual Widget"""
        # widgets={
        #     'title': forms.TextInput(attrs={
        #         'class':" w-full border-2 rounded-lg",
        #         'placeholder':"Enter Your Title"
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class':"w-full border-2 rounded-lg",
        #         'placeholder':'Give your task description'
        #     }),
        #     'due_date': forms.SelectDateWidget(attrs={
        #         'class':"border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        #     }),
        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={
        #         'class':"mt-1 w-full text-blue-600 bg-white border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
        #     })
        # } 


class TaskDetailModelForm(StyleFormMixing, forms.ModelForm):
    class Meta:
        model =  TaskDetail
        fields = ['priority','notes','asset']