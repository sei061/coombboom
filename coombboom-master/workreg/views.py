from datetime import timezone, datetime
from unicodedata import decimal

from django.forms import modelform_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from groups.models import Project
from tasks.models import Task
from .forms import AddEntryForm
from django.utils import timezone
from . import forms
from .models import Entry
from django.urls import reverse_lazy

EntryForm = modelform_factory(Entry, exclude=[])


def new(request):
    """
    A method that lets user register their own timestamps for when working with a specific
    project and task. Also makes you choose date from-end and timestamps from-end.

    :param request: A request that collects the workreg inputs
    :return: returns a render of the html-page with a toast depending on the result
    """
    page_title = "Legg til timeregistrering"
    form = AddEntryForm(request.POST or None)

    if request.method == 'POST':
        form = AddEntryForm(request.POST)

        if form.is_valid():
            try:
                if Entry.objects.get(end_time=None):
                    entry = Entry.objects.get(end_time=None)
                    entry.end_time = timezone.now()
                    entry.save()

            except Exception:
                pass

            finally:
                # get time data
                start_time = form.cleaned_data.get('from_time')
                end_time = form.cleaned_data.get('end_time')
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                # Get task object from form
                task_pk = request.POST['task']

                # TODO how is [form.cleaned_data.get('task')]  task_name?

                # calculate time spent
                time_spent = datetime.combine(end_date, end_time) - datetime.combine(start_date, start_time)
                # time spent to hours
                time_spent = (time_spent.seconds / 3600)
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                instance = form.save()
                # get ID of new row & instantiate object
                entry_id = instance.id
                entry_obj = Entry.objects.get(pk=entry_id)
                # set time spent & subtract time allotted for task
                entry_obj.time_spent = time_spent
                task_obj = Task.objects.get(pk=task_pk)
                task_obj.expected_time = task_obj.expected_time - time_spent
                # set project if exists and is not global task
                global_tasks = Task.objects.filter(project_id=None)
                global_tasks_id = global_tasks.values_list('id', flat=True)
                project_id = request.POST['project']
                entry_obj.project_id = project_id
                if int(task_pk) in global_tasks_id:
                    entry_obj.project_id = None
                # save changes
                task_obj.save()
                entry_obj.save()

            return render(request, 'workreg/add_entry.html', {
                'form': form,
                'toast': 'Registrering lagt til',
                'projects': Project.objects.all(),
                'tasks': Task.objects.none(),
                'global_tasks': global_tasks
            })
    global_tasks = Task.objects.filter(project_id=None)
    return render(request, 'workreg/add_entry.html', {
        'form': form,
        'projects': Project.objects.all(),
        'tasks': Task.objects.none(),
        'global_tasks': global_tasks,
    })


def workreg_update_view(request, pk):
    """

    A method that makes users edit their own workregs

    :param request: A request that collects the workreg inputs
    :param pk: gets the PK of the logged in user
    :return: returns a render of the html-page with a toast depending on the result
    """
    person = get_object_or_404(Entry, pk=pk)
    form = AddEntryForm(instance=person)
    if request.method == 'POST':
        form = AddEntryForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_change', pk=pk)
    return render(request, 'workreg/add_entry.html', {'form': form})


def list(request):
    """

    A method that makes a list of all the registered workregs from all users. We can also use this to
    make individual lists based on who created the workregs.

    :param request: A request that collects the workreg inputs
    :return: returns a render of the html-page that shows list of all workregs
    """
    lists = Entry.objects.all()

    # TODO this is commented section useless. since new() is changed.

    # entries_for_user = []  # create empty arr
    # for all_entries in lists:  # for all entries in lists
    #    if request.user.id == all_entries.user.id:  # if user.id == entry.user.id
    #        entries_for_user.append(all_entries)  # append object to entries_for_user
    # for entry in entrires for user
    # for entry in entries_for_user:
    #    task_id = entry.task_id  # task id
    #    task = Task.objects.get(pk=task_id)  # instantiate task object
    #    hours_used_for_task = entry.total_duration  # hours used
    #    time_difference = int(hours_used_for_task) - int(task.original_time)
    #    task.expected_time = hours_used_for_task  # set expected_time to hours sued
    #    task.save()  # save to db

    context = {'lists': lists}

    return render(request, 'workreg/list_entry.html', context)


def stop(request):
    """

    This method is not in use. The plan was to make a stop button to let users stop the workreg when they
    wanted to.

    :param request: A request that collects the workreg inputs
    :return: returns a render of the html-page that shows list of all workregs
    """
    if request.method == 'POST':
        entry_id = request.POST.get('id_stop')
        lists = Entry.objects.all()
        context = {'lists': lists}

        if Entry.objects.get(end_time=None):
            entry = Entry.objects.get(end_time=None)
            entry.end_time = timezone.now()
            entry.save(force_update=True)
        # entry = Entry.objects.get(id=entry_id)
        # .end_time = timezone.now()
        # entry.save()

        return render(request, 'workreg/list_entry.html', context)
    else:
        return request(request, 'workreg/list_entry.html', {'error_msg': True})


def start_pause(request):
    """

    This is not in use. Plan was to make the user be able to stop and start specific workregs when
    they went to lunsj etc.

    :param request: A request that collects the workreg inputs
    :return: returns a render of the html-page that shows list of all workregs
    """
    if request.method == 'POST':
        if request.POST.get('id_start_pause'):
            lists = Entry.objects.all()
            context = {'lists': lists}

            entry = Entry()
            entry.user = request.user
            entry.task_id = '1'
            entry.end_date = timezone.now()
            entry.save()

            return render(request, 'workreg/list_entry.html', context)
        else:
            return redirect(request, 'workreg/list_entry.html', {'error_msg': True})


class DeleteEntryView(DeleteView):
    model = Entry
    template_name = 'workreg/delete_workreg.html'
    success_url = reverse_lazy('index')


def delete_entry(request, pk):
    if request.method == "POST":
        target_entry = Entry.objects.get(id=pk)
        target_entry.is_deleted = True
        target_entry.save()
        return redirect('workreg:entry-list')


def load_tasks(request):
    """

    This method is used so we can have independency between projects and tasks. So if you choose a project
    only tasks thats is created under that project will be shown.

    :param request: A request that collects the projects inputs
    :return: returns a render of the html-page that lists all the tasks under specific projects
    """
    project_id = request.GET.get('project_id')
    tasks = Task.objects.filter(project_id=project_id)
    return render(request, 'workreg/task_dropdown_list_options.html', {'tasks': tasks})
