from django.shortcuts import render
from .forms import ExcelUploadForm
from .management.commands.import_data import Command

def upload_excel(request):
    if request.method == 'POST' and request.FILES['file']:
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file to a specific path
            uploaded_file = form.cleaned_data['file']
            file_path = f"media/excel_files/{uploaded_file.name}"
            
            # Save the file
            with open(file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Call the management command to import data
            command = Command()
            command.handle(file_path=file_path)

            return render(request, 'success.html')

    else:
        form = ExcelUploadForm()
    
    return render(request, 'upload_excel.html', {'form': form})