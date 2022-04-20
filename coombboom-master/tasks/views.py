from datetime import date

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from groups.models import Project
from tasks.forms import TaskCreationForm
from tasks.models import Task
from coombboom.decorators import project_access_control, authentication_required, has_project_task_perm


def task(request):
    return render(request, 'tasks/task_index.html')


@authentication_required
@project_access_control('project.add_task_perm')
def create_task(request, projects):
    """
    Method for creating a task. Tasks can be project-specific, if not they are global

    :param request: A request that collects the task inputs
    :return: returns a render of the html-page with a toast depending on the result

    """
    form = TaskCreationForm()
    if not request.method == 'POST':
        return render(request, 'tasks/task_creation.html', {'form': form, 'teams': projects})

    form = TaskCreationForm(request.POST)
    if not form.is_valid():
        return HttpResponse("form not valid")

    try:
        new_task = Task()
        project_id = request.POST['projects']

        # if not post[projects] is empty then assign else don't assign, will become <null> in db
        if not project_id == '':
            new_task.project_id = project_id

        new_task.task_name = request.POST['task_name']
        new_task.est_time = request.POST['est_time']
        new_task.expected_time = request.POST['expected_time']
        new_task.task_status = request.POST['task_status']
        new_task.start_date = request.POST['start_date']
        new_task.original_time = new_task.expected_time
        new_task.save()
        return render(request, 'tasks/task_creation.html')
    except ValueError:
        return HttpResponse("No Duplicate name")


@authentication_required
@has_project_task_perm('project.update_estimate')
def display_task_get(request, only_sel_fields=True):
    """
    Update task info, by default if you have update_estimate perm then you can update estimate and
        status for task
    Currently accessed through any of the tasks lists in Dashboard app
    if user is admin or staff or superuser then you can edit all fields for task
    param: request: request object
    :param only_sel_fields => True or False, Default True if not supplied. This is the var
        we switch on to disable other fields if you dont have full perms
    """
    if not request.method == 'POST':
        task_id = request.GET['id']
        data = Task.objects.get(pk=task_id)
        projects = Project.objects.all()
        # try to catch because task.project_id is null if task is global
        try:
            current_project = Project.objects.get(pk=data.project_id)
        except Project.DoesNotExist:
            current_project = 0
        task_to_edit = {"info_task": data,
                        "all_projects": projects,
                        "only_update_select_fields": only_sel_fields
                        }
        return render(request,
                      'tasks/task_edit.html',
                      task_to_edit)

    task_id = request.POST['task_id']
    edit_task = Task.objects.get(pk=task_id)
    time = request.POST['expected_time']
    if edit_task.expected_time != float(time):
        if not edit_task.time_changed:
            edit_task.original_time = edit_task.expected_time

        edit_task.time_changed = True
        edit_task.when_changed = date.today()
    try:
        if not only_sel_fields:
            edit_task.task_name = request.POST['task_name']
            edit_task.start_date = request.POST['start_date']
            edit_task.est_time = request.POST['est_time']

        edit_task.expected_time = request.POST['expected_time']
        edit_task.task_status = request.POST['task_status']
    except MultiValueDictKeyError:
        pass
    edit_task.save()
    return redirect('dashboard:')


@authentication_required
@project_access_control('project.change_task')
def display_task(request, projects):
    """
    Method for displaying tasks in a list. A task can be selected and edited if necessary.

    :param request: A request that gets the selected task from the list.
    :return: returns a render of the html-page for task editing.

    """
    if request.method == 'POST':
        button = request.POST['button']
        if button == "alter":
            task_id = request.POST['task_id']
            edit_task = Task.objects.get(pk=task_id)
            time = request.POST['expected_time']
            if edit_task.expected_time != float(time):
                if not edit_task.time_changed:
                    edit_task.original_time = edit_task.expected_time

                edit_task.time_changed = True
                edit_task.when_changed = date.today()

            edit_task.task_name = request.POST['task_name']
            edit_task.start_date = request.POST['start_date']
            edit_task.expected_time = request.POST['expected_time']
            edit_task.task_status = request.POST['task_status']
            edit_task.est_time = request.POST['est_time']
            edit_task.save()
            data = Task.objects.all()
            edit_task = {
                "all_tasks": data
            }
            return render(request, 'tasks/task_display.html', edit_task)

        elif button == "edit":
            task_id = request.POST['task_id']
            data = Task.objects.get(pk=task_id)
            projects = Project.objects.all()
            # try to catch because task.project_id is null if task is global
            try:
                current_project = Project.objects.get(pk=data.project_id)
            except Project.DoesNotExist:
                current_project = 0
            edit_task = {"info_task": data,
                         "all_projects": projects,
                         }

        return render(request, 'tasks/task_edit.html', edit_task)

    else:
        data = Task.objects.all()

        edit_task = {
            "all_tasks": data,

        }
        return render(request, 'tasks/task_display.html', edit_task)
