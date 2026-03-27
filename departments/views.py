from django.shortcuts import render, get_object_or_404, redirect
from .models import Department
from django.contrib import messages

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/list.html', {'departments': departments})

def department_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        established_date = request.POST.get('established_date')
        
        Department.objects.create(
            name=name,
            description=description,
            established_date=established_date
        )
        messages.success(request, "Département ajouté avec succès.")
        return redirect('department_list')
    return render(request, 'departments/add.html')

def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.description = request.POST.get('description')
        department.established_date = request.POST.get('established_date')
        department.save()
        messages.success(request, "Département mis à jour.")
        return redirect('department_list')
    return render(request, 'departments/edit.html', {'department': department})

def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, "Département supprimé.")
        return redirect('department_list')
    return render(request, 'departments/delete.html', {'department': department})
