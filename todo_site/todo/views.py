from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Todo
from .forms import TodoForm

# Create your views here.
def index(request):
    item_list=Todo.objects.order_by("-date")
    if request.method=="POST":
        form=TodoForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('todo')
    form=TodoForm()

    page={
        "forms":form,
        "list":item_list,
        "title":"TODO LIST",
    }
    return render(request, 'todo/index.html', page)

def remove(request, item_id):
    item=Todo.objects.get(id=item_id)
    item.delete()
    message.info(request, "item removed !!!")
    return redirect('todo')