from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm
from django.contrib import messages


# Create your views here.
@login_required
def todo_list(required):
    todos = Todo.objects.filter(user=required.user)
    return render(required, 'todo/todo_list.html', {'todos': todos})


@login_required
def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    return render(request, 'todo/todo_detail.html', {'todo': todo})


@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Todo created successfully!')
            return redirect('todo:todo_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TodoForm()
    return render(request, 'todo/todo_form.html', {'form': form})

@login_required
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo updated successfully!')
            return redirect('todo:todo_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/todo_form.html', {'form': form})

@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo deleted successfully!')
        return redirect('todo:todo_list')
    return render(request, 'todo/todo_confirm_delete.html', {'todo': todo})

@login_required
def todo_toggle_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    messages.success(request, f'Todo marked as {"completed" if todo.completed else "incomplete"}!')
    return redirect('todo:todo_list')