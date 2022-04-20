import re
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from datetime import datetime, timedelta
# Create your views here.
from account.models import User
from coombboom.decorators import has_global_perm, authentication_required, can_export_project, can_export_group
from groups.models import Project
from groups.views import get_group_project_membership
from tasks.models import Task
from workreg.models import Entry


def get_labels_for_chart(tasks):
    """
    Method to get labels for chart
    Takes array of tasks for project
    returns array with oldest date incrementing to youngest date for all tasks on project

    :param tasks: is for example Task.objects.filter(projects_id=2), list of tasks for project for example.
    """
    labels = [0]  # start label 0
    try:
        start_dates = tasks.values_list('start_date')
        end_dates = tasks.values_list('est_time')
        oldest = min(start_dates)
        newest = max(end_dates)
        time_delta = newest[0] - oldest[0]
        for day in range(time_delta.days):
            temp = oldest[0] + timedelta(days=day)
            labels.append(str(temp))  # add date as string to labels array
    except ValueError:
        pass
    return labels


def get_maximum_storypoints(tasks):
    """
    get maximum of number for Yaxes in chart
    :param tasks: is for example Task.objects.filter(projects_id=2)
    """
    max_y_points = 0
    for task in tasks:
        max_y_points += task.original_time

    return max_y_points


def get_ideal_and_goal_line(tasks, labels, max_y_points):
    """
    Creates a list of 2 lists
    list[0] creates array of data for the perfect ideal line for chart based on max Yaxes
    points and how many labels exists

    list[1] creates array of data for goal line in chart,, which is just [max_y_points, <---> ... ]

    :param tasks: is for example Task.objects.filter(projects_id=2)
    :param labels: is array of labels
    :param max_y_points: maximum number for Yaxes
    """
    ideal_and_goal_line = [[], []]
    try:

        label_len = (len(labels))
        base_to_increment = max_y_points / (label_len - 1)
        for i in range(label_len):
            ideal_and_goal_line[0].append(base_to_increment * i)
            ideal_and_goal_line[1].append(max_y_points)
    except ZeroDivisionError:
        pass

    return ideal_and_goal_line


def get_actual_line(workreg, labels):
    """
    get actual_line data from workreg sorted by date oldest to youngest

    :param workreg: array of wokrerg registrations for project
    :param labels: is array of labels
    """
    actual_line = [0]
    data = []
    current_date = datetime.now()
    for label in labels:  # for each label .ex '2021-04-24', array is sorted from oldest date.
        if label == 0: continue
        label_date = datetime.strptime(label, '%Y-%m-%d')
        if label_date <= current_date:  # first element is 0 and not from db and dont do anything if date is in the future
            x = workreg.values_list('time_spent').filter(end_date=label)  # QuerySet of time spent on a specific day
            data.append(x)  # append to data array, even if empty
    x = 0.0  # keep X out of for loop because we want to add time on top of existing time
    for t in range(len(data)):
        for n in data[t]:
            # convert tuple to str to float
            x += float(str(n[0]))
        actual_line.append(x)

    return actual_line


def percentage_done(workreg, max_y_points):
    """
    Get percentage done total time spent / total time planned
    :param workreg array of workreg objects
    :param max_y_points: maximum number for Yaxes
    """
    percentage = 0.0
    try:
        str_time_spent = str(workreg.aggregate(Sum('time_spent')))
        total_time_spent = float(re.sub(r'[^0-9\.]', '', str_time_spent))
        percentage = round((total_time_spent / max_y_points) * 100, 1)
    except ValueError:
        pass
    except ZeroDivisionError:
        pass

    return percentage


@authentication_required
@can_export_project('project.generate_report')
def project(request, display_workreg=None):
    """
    display data in /dashboard/project?id=x
    displays visual chart for project progress
    displays progressbar with percent complete
    displays tasks for project
    :param request: is for example Task.objects.filter(projects_id=2)
    :param display_workreg: decorator supplies True or False, is true if user has perm
        or is admin. If true workreg for team will show, else will only load tasks and graph
    """
    if request.method == 'GET':
        id_project = request.GET['id']
        try:
            project_obj = Project.objects.get(pk=id_project)
        except Project.DoesNotExist:
            return redirect('dashboard:')
        # tasks, get max story points by adding task original times together
        tasks = Task.objects.filter(project_id=id_project)
        max_y_points = get_maximum_storypoints(tasks)
        labels = get_labels_for_chart(tasks)
        ideal_and_goal_line = get_ideal_and_goal_line(tasks, labels, max_y_points)
        goal_line = ideal_and_goal_line[1]
        ideal_line = ideal_and_goal_line[0]
        workreg = Entry.objects.filter(project_id=id_project)
        actual_line = get_actual_line(workreg, labels)
        percent_complete = percentage_done(workreg, max_y_points)
        context = {
            'ideal_line_arr': ideal_line,
            'goal_line_arr': goal_line,
            'max_y_points': max_y_points,
            'labels_for_x': labels,
            'actual_line_arr': actual_line,
            'percent_done': percent_complete,
            'dashboard_tasks': 1,
            'tasks': tasks,
            'workreg': workreg,
            'tableType': project_obj.name,
            'display_workreg': display_workreg
        }
        if not display_workreg:
            context.pop('workreg')

        return render(request, 'project_dashboard.html', context)


@authentication_required
@can_export_group('groups.report_generation_group')
def team(request, display_workreg=None):
    """
    Team dashboard function, displays graph, tasks and hours for team
    :param request : request object
    :param display_workreg : decorator supplies True or False, is true if user has perm
        or is admin. If true workreg for team will show, else will only load tasks and graph
    """
    if request.method == 'GET':
        id_group = request.GET['id']
        try:
            group_to_display = Group.objects.get(pk=id_group)
        except Group.DoesNotExist:
            return redirect('dashboard:')
        projects = get_group_project_membership(group_to_display)
        workreg = []
        tasks = []
        users_in_grp = list(group_to_display.user_set.all().values_list('id', flat=True))
        for proj in projects:
            tasks.append(Task.objects.filter(project_id=proj.pk))
            workreg.append(Entry.objects.filter(project_id=proj.pk))

        max_y_points = get_maximum_storypoints(tasks[0])
        labels = get_labels_for_chart(tasks[0])
        ideal_and_goal_line = get_ideal_and_goal_line(tasks[0], labels, max_y_points)
        goal_line = ideal_and_goal_line[1]
        ideal_line = ideal_and_goal_line[0]

        actual_line = get_actual_line(workreg[0], labels)
        percent_complete = percentage_done(workreg[0], max_y_points)

        context = {
            'ideal_line_arr': ideal_line,
            'goal_line_arr': goal_line,
            'max_y_points': max_y_points,
            'labels_for_x': labels,
            'actual_line_arr': actual_line,
            'percent_done': percent_complete,
            'dashboard_tasks': 1,
            'tasks': tasks[0],
            'workreg': workreg[0],
            'tableType': group_to_display.name,
            'display_workreg': display_workreg
        }

        if not display_workreg:
            context.pop('workreg')

        return render(request, 'team_dashboard.html', context)


@authentication_required
def load_dash_user(request):
    """
    load dashboard for user
    task, projects and teams.

    Admins will be able to access all projects and teams from here
    :param
    :request: request object
    """
    groups = request.user.groups.all()
    projects = []
    for group in groups:
        p = get_group_project_membership(group)
        for project_object in p:
            projects.append(project_object)
    workreg_user = Entry.objects.filter(user_id=request.user.pk)
    tasks_user = []
    for reg in workreg_user:
        tasks_user.append(Task.objects.get(task_name=reg.task))
    if request.user.is_staff or request.user.is_superuser:
        groups = Group.objects.all()
        projects = Project.objects.all()
        tasks_user = Task.objects.all()
    return render(request, 'dashboard_user.html', {
        'groups': groups,
        'projects': projects,
        'workreg': workreg_user,
        'dashboard_tasks': 1,
        'tasks': tasks_user,
        'display_workreg': True,
        'tableType': request.user.first_name + ' ' + request.user.last_name
    })


@authentication_required
@has_global_perm('groups.report_generation')
def load_grps_proj(request):
    """
    load all groups, projects and tasks in the system on single page
    :param request: request object
    """
    if request.method == 'GET':
        g = Group.objects.all()
        p = Project.objects.all()
        t = Task.objects.all()
        return render(request, 'dashboard.html', {
            'projects': p,
            'tasks': t,
            'groups': g
        })


def list_to_string_help(array):
    """
    helper function to iterate through array and create a single string with all the values
    comma delimited
    :param
    :array: array to create string of
    """
    return ', '.join([str(elem) for elem in array])


@authentication_required
@can_export_project('project.generate_report')
def csv_ajax_get_project(request, display_workreg=None):
    """
    supplies ajax requests with json objects to export data to csv for projects
    :param
    :request: request object
    :display_workreg: not used in method, just an argument because decorator used provides it
    """
    if not display_workreg:
        return redirect('dashboard:')
    if request.method == 'GET':
        id_project = request.GET['id']
        project_obj = Project.objects.get(pk=id_project)
        # tasks, get max story points by adding task original times together
        tasks = Task.objects.filter(project_id=id_project)
        max_y_points = get_maximum_storypoints(tasks)
        labels = get_labels_for_chart(tasks)
        ideal_and_goal_line = get_ideal_and_goal_line(tasks, labels, max_y_points)
        goal_line = ideal_and_goal_line[1]
        ideal_line = ideal_and_goal_line[0]
        workreg = Entry.objects.filter(project_id=id_project)
        actual_line = get_actual_line(workreg, labels)

        str_actual = list_to_string_help(actual_line)
        str_ideal = list_to_string_help(ideal_line)
        str_goal = list_to_string_help(goal_line)
        str_labels = list_to_string_help(labels)

        task_arr = []
        for task in tasks:
            task_arr.append(task.task_name + ', ' + str(task.expected_time) + ', ' + str(
                task.original_time) + ', ' + str(task.task_status) + ', ' +
                            str(task.start_date) + ', ' + str(task.est_time))
        workreg_arr = []
        for reg in workreg:
            workreg_arr.append(reg.comment + ', ' + reg.place + ', ' + str(reg.start_date) + ', ' + str(
                reg.end_date) + ',' + str(reg.time_spent) + ', ' + str(reg.from_time) + ', ' +
                               str(reg.end_time) + ', ' + str(
                User.objects.get(pk=reg.user_id).get_full_name()) + ', ' + str(
                Task.objects.get(pk=reg.task_id).task_name))
        return JsonResponse({
            'goal_line': str_goal,
            'ideal_line': str_ideal,
            'actual_line': str_actual,
            'labels': str_labels,
            'tasks': list(task_arr),
            'workreg': list(workreg_arr),
            'name': project_obj.name
        })


@authentication_required
@can_export_group('groups.report_generation_group')
def csv_ajax_get_team(request, display_workreg=None):
    """
    supplies ajax requests with json objects to export data to csv - for teams
    :param
    :request: request object
    :display_workreg: not used in method, just an argument because decorator used provides it
    """
    if not display_workreg:
        return redirect('dashboard:')
    if request.method == 'GET':
        id_group = request.GET['id']
        try:
            group_to_display = Group.objects.get(pk=id_group)
        except Group.DoesNotExist:
            return redirect('dashboard:')
        projects = get_group_project_membership(group_to_display)
        workreg = []
        tasks = []
        users_in_grp = list(group_to_display.user_set.all().values_list('id', flat=True))
        for proj in projects:
            tasks.append(Task.objects.filter(project_id=proj.pk))
            workreg.append(Entry.objects.filter(project_id=proj.pk))

        max_y_points = get_maximum_storypoints(tasks[0])
        labels = get_labels_for_chart(tasks[0])
        ideal_and_goal_line = get_ideal_and_goal_line(tasks[0], labels, max_y_points)
        goal_line = ideal_and_goal_line[1]
        ideal_line = ideal_and_goal_line[0]

        actual_line = get_actual_line(workreg[0], labels)

        str_actual = list_to_string_help(actual_line)
        str_ideal = list_to_string_help(ideal_line)
        str_goal = list_to_string_help(goal_line)
        str_labels = list_to_string_help(labels)

        task_arr = []
        for task in tasks[0]:
            task_arr.append(task.task_name + ', ' + str(task.expected_time) + ', ' + str(
                task.original_time) + ', ' + str(task.task_status) + ', ' +
                            str(task.start_date) + ', ' + str(task.est_time))
        workreg_arr = []
        for reg in workreg[0]:
            workreg_arr.append(reg.comment + ', ' + reg.place + ', ' + str(reg.start_date) + ', ' + str(
                reg.end_date) + ',' + str(reg.time_spent) + ', ' + str(reg.from_time) + ', ' +
                               str(reg.end_time) + ', ' + str(
                User.objects.get(pk=reg.user_id).get_full_name()) + ', ' + str(
                Task.objects.get(pk=reg.task_id).task_name))
        return JsonResponse({
            'goal_line': str_goal,
            'ideal_line': str_ideal,
            'actual_line': str_actual,
            'labels': str_labels,
            'tasks': list(task_arr),
            'workreg': list(workreg_arr),
            'name': group_to_display.name
        })
