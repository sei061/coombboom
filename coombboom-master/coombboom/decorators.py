from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import redirect
from guardian.core import ObjectPermissionChecker
from groups.models import Project
from tasks.models import Task


def authentication_required(view_function):
    """
    checks if user is authenticated (logged in). if not logged in => redirect to login page
    """
    def wrapper_function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return view_function(request, *args, **kwargs)

    return wrapper_function


def has_global_perm(perm_to_check=''):
    """
    checks that the user has global perm  => perm_to_check through group or admin/superuser/staff
    param: perm_to_check: permission codename to check
    """
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.is_staff or user.has_perm(perm_to_check):
                return view_function(request, *args, **kwargs)
            perms_for_user = user.get_all_permissions()  # get all perms for user
            for permission in perms_for_user:  # for each permission in perms for user
                if permission == perm_to_check:  # check if perm equals perm required to access resource
                    return view_function(request, *args, **kwargs)  # return true if so
            return HttpResponse("You dont have global perm required for this action")

        return wrapper_function

    return decorator


def group_access_control(perm_to_check=''):
    """
    checks perm on user, supplies groups that the user has given perm on through group membership
    param: perm_to_check: permission codename to check
    """
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            user = request.user
            if user.is_staff or user.is_superuser or user.is_admin:
                groups = Group.objects.all()
                return view_function(request, groups, *args, **kwargs)
            groups = user.groups.all()
            groups_with_perm = []
            for group in groups:
                if user.has_perm(perm=perm_to_check, obj=group):
                    groups_with_perm.append(group)
            if not groups_with_perm:
                return HttpResponse("You dont have have the object based permssion required for any groups")

            return view_function(request, groups_with_perm, *args, **kwargs)

        return wrapper_function

    return decorator


def project_access_control(perm_to_check=''):
    """
    checks perm on user, supplies projects that the user has given perm on through group membership
    currently used for def task_create
    param: perm_to_check: permission codename to check
    """
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            user = request.user
            # if user is staff, admin or superuser then call function
            if user.is_staff or user.is_superuser or user.is_admin:
                projects = Project.objects.all()
                return view_function(request, projects, *args, **kwargs)
            # if not start with get groups for user, get all projects
            groups_for_user = user.groups.all()
            projects = Project.objects.all()
            # instantiate array to hold projects that any group is a member of has.
            project_with_perm = []
            # check perm for each group on each project
            for group in groups_for_user:
                checker = ObjectPermissionChecker(group)
                for project in projects:
                    if checker.has_perm(perm=perm_to_check, obj=project):
                        # if group has perm on project then append to array
                        project_with_perm.append(project)
            # TODO need some logic for GLOBAL TASKS? Atm not providing a project when creating tasks creates globaltask
            # if project_with_perm is empty after iterating then we have no permission to create any task
            if not project_with_perm:
                return redirect('index')
            # return call function with project_with_perm added
            return view_function(request, project_with_perm, *args, **kwargs)

        return wrapper_function

    return decorator


def has_project_task_perm(perm_to_check=''):
    """
    checks perm on user, checks that the user has given perm on project for a specific task
    currently used for def display_task_get
    param: perm_to_check: permission codename to check
    """
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            task_id = request.GET['id']
            user = request.user
            if task_id == '':
                return redirect('dashboard:')

            if user.is_superuser or user.is_staff or user.has_perm(perm_to_check):
                return view_function(request, False, *args, **kwargs)

            groups_for_user = user.groups.all()
            projects = Project.objects.all()
            task = Task.objects.get(pk=task_id)

            try:
                task_project = Project.objects.get(pk=task.project_id)
            except AttributeError:  # TODO logic for global task here? global perm for global task?
                return redirect('dashboard:')

            # check perm for each group on each project
            for group in groups_for_user:
                checker = ObjectPermissionChecker(group)
                if checker.has_perm(perm=perm_to_check, obj=task_project):
                    # if group has perm on project then append to array
                    return view_function(request, *args, **kwargs)

            return redirect('dashboard:')

        return wrapper_function

    return decorator


def can_export_project(perm_to_check=''):
    """
    checks user permissions, or indirect perms through groups for user
    used for def project and def csv_ajax_get_project
    param: perm_to_check: permission codename to check
    """
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            user = request.user
            project_id = request.GET['id']
            if project_id == '':
                return redirect('dashboard:')
            try:
                project = Project.objects.get(pk=project_id)
            except Project.DoesNotExist:
                return redirect('dashboard:')
            # if user is staff, admin or superuser then call function
            if user.is_staff or user.is_superuser or user.is_admin:
                return view_function(request, display_workreg=True, *args, **kwargs)
            # if not start with get groups for user, get all projects
            groups_for_user = user.groups.all()
            # check perm for each group on each project
            for group in groups_for_user:
                checker = ObjectPermissionChecker(group)
                if checker.has_perm(perm=perm_to_check, obj=project):
                    # if group has perm on project then append to array
                    return view_function(request, display_workreg=True, *args, **kwargs)
            return view_function(request, display_workreg=False, *args, **kwargs)

        return wrapper_function

    return decorator


def can_export_group(perm_to_check=''):
    """
    checks perm for user trying to access method.
    this decorator is used for def team and def csv_ajax_get_team
    param: perm_to_check: permission codename to check
    """
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.is_staff or user.has_perm(perm_to_check):
                return view_function(request, display_workreg=True, *args, **kwargs)
            perms_for_user = user.get_all_permissions()  # get all perms for user
            for permission in perms_for_user:  # for each permission in perms for user
                if permission == perm_to_check:  # check if perm equals perm required to access resource
                    return view_function(request, display_workreg=True, *args, **kwargs)  # return true if so

            return view_function(request, display_workreg=False, *args, **kwargs)

        return wrapper_function

    return decorator
