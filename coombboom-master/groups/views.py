from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign_perm, get_perms_for_model, remove_perm, get_group_perms
from django.db import IntegrityError

from coombboom.decorators import authentication_required, has_global_perm, group_access_control, project_access_control
from .models import Project
from .forms import ValidateGroupForm, ValidateProjectForm, ValidateAddPermForm, ValidatePermGroupForm, \
    ValidatePermToGroupForm
from account.models import User
from django.contrib.auth.models import Group, Permission
from tasks.models import Task


# Create your views here.

@authentication_required
@has_global_perm('groups.view_group')
def view_groups(request):
    """
    returns view of all groups in db
    :param request: request object
    :return: render template
    """
    return render(request, 'view_groups.html', {'groups': Group.objects.all()})


@authentication_required
@has_global_perm('groups.view_project')
def view_projects(request):
    """
    returns view of all projects
    :param request: request object
    :return: render template
    """


    return render(request, 'view_projects.html', {'projects':Project.objects.all()})


# localhost/groups/new_team
@authentication_required
@has_global_perm('groups.read_group')
def add_new_group(request):
    """
    add new team, handles form & post data
    :param request: request object
    :return: render template
    """
    # check if user has perm to add teams
    users = User.objects.all()  # get users to list in form
    form = ValidateGroupForm(request.POST)  # instantiate ValidateGroupForm

    if not request.method == 'POST':
        return render(request, 'add_group.html', {'form': form,
                                                  'users': users,
                                                  'projects': Project.objects.all(),
                                                  })
    if not form.is_valid():
        return HttpResponse("<h1>form not valid!<h1>")

    name = form.cleaned_data.get('name')  # get name of group to be created
    author = request.user  # get author of group to be created
    users_to_add = request.POST.getlist('users')  # get users to add into group

    try:  # try to avoid uniquename err
        team_created = create_group(name, author, '0')  # create new group
        for user in map(int, users_to_add):  # for each user
            team_created.user_set.add(user)  # add user to group

        perms = get_perms_for_model(team_created)  # give all perms of created group to author
        for perm in perms:
            assign_perm(perm, author, team_created)

        # add team to projects if they are present
        if request.POST.getlist('projects'):
            projects = request.POST.getlist('projects')
            for project in projects:
                p = Project.objects.get(pk=project)
                assign_perm('member', team_created, p)

        return render(request, 'add_group.html',
                      {'form': form,
                       'users': users,
                       'projects': Project.objects.all(),
                       'toast': 'Added Team'})

    except IntegrityError:  # err; unique name. name exists already
        return render(  # return user to form with error msg
            request,
            'add_group.html',
            {'form': form,
             'users': users,
             'projects': Project.objects.all(),
             'error': "Team with this name already exists",
             })


# localhost/group/new_project
@authentication_required
@has_global_perm('project.add_project')
def add_new_project(request):
    """
    add new project, renders form & handles post
    :param request:
    :return:
    """
    form = ValidateProjectForm(request.POST)  # instantiate ValidateProjectForm
    team_objects = Group.objects.all()  # get all teams to list in form
    if not request.method == 'POST':
        return render(request, 'add_project.html', {'form': form, 'teams': team_objects})

    if not form.is_valid():
        return render(request, 'add_project.html', {'form': form, 'teams': team_objects, 'error': 'form not valid'})

    name = form.cleaned_data.get('name')  # get name of project
    author = request.user  # get author of project
    teams_to_add = request.POST.getlist('teams')  # get teams to add to project

    project_created = create_project(name, author)

    assign_perm('groups.add_task_perm', author)
    assign_perm('groups.update_estimate', author)
    assign_perm('groups.edit_group_project', author)
    assign_perm('groups.generate_report', author)
    assign_perm('groups.edit_project', author)
    assign_perm('groups.read_project', author)
    assign_perm('groups.give_perm', author)
    assign_perm('groups.add_perm_project', author)
    assign_perm('groups.member', author)

    # TODO: Make table for connecting thine project id tho thy user id's for whom may know if thine is part of project if thine dont have table for such.

    try:  # catch error duplicate project name
        for team in map(int, teams_to_add):  # for each team selected
            team_object = Group.objects.filter(pk=team)  # get team instance
            assign_perm('member', team_object, project_created)  # set team member of project

            return render(request, 'add_project.html',
                          {'form': form, 'teams': team_objects, 'toast': 'Added Project'})  # return success
    except IntegrityError:  # exception uniquename err
        return render(  # render form with err msg
            request,
            'add_group.html',
            {'form': form,
             'teams': team_objects,
             'error': "Project with this name already exists"
             })


# localhost/group/add_perm_group
@authentication_required
@has_global_perm('groups.add_perm_group')
def add_perm_group(request):
    """
    add permission group, render form & handle post
    :param request: request object
    :return: render template
    """
    perms = Permission.objects.exclude(codename='member')  # get perms to list in form
    users = User.objects.all()  # get users to list in form
    form = ValidatePermGroupForm(request.POST)  # instantiate form

    if not request.method == 'POST':
        return render(request, 'add_perm_group.html', {'form': form, 'perms': perms, 'users': users})

    if not form.is_valid():
        return HttpResponse("<h1> Form not valid<h1>")  # form is not valid return err

    name = form.cleaned_data.get('team_name')  # get name for permission group
    author = request.user  # get author of the permission group
    perms_to_add = request.POST.getlist('perms')  # get list of permissions to assign to group
    users_to_add = request.POST.getlist('users')  # get list of users to add into perm group

    perm_group = create_group(name, author, '1')  # create group
    try:
        for perm in perms_to_add:  # for each perm selected, assign to group
            p = Permission.objects.get(pk=perm)  # get Perm object
            assign_perm(p, perm_group)  # assign perm

        for user in users_to_add:  # for each user selected, add to group
            perm_group.user_set.add(user)  # add users to group

        perms = get_perms_for_model(perm_group)  # give all perms of created group to author

        for perm in perms:
            assign_perm(perm, author, perm_group)

        return render(request, 'add_perm_group.html',
                      {'form': form, 'perms': perms, 'users': users, 'toast': 'Perm group added'})
    except IntegrityError:  # except
        return render(request, 'add_perm_group.html',
                      {'form': form, 'perms': perms, 'users': users,
                       'error': 'Perm group with this name already exists'})


# assign perm to create groups or Project. User selects which in form
@authentication_required
@has_global_perm('account.assign_create_group')
def add_perm_user(request):
    """
    add permission to user
    :param request: request object
    :return: render template
    """

    form = ValidateAddPermForm(request.POST)  # instantiate ValidateAddPermForm
    users = User.objects.all()  # get users to list in form
    perms = Permission.objects.exclude(codename='member')

    if not request.method == 'POST':
        return render(request, 'add_perm_to_user.html', {'form': form, 'users': users, 'perms': perms})

    if not form.is_valid():
        return HttpResponse("<h1> not valid form <h1>")

    perms_to_add = request.POST.getlist('perms')
    users = request.POST.getlist('users')  # get users we are assigning perms to
    for perm in perms_to_add:  # for each perm
        p = Permission.objects.get(pk=perm)  # instantiate permission object
        for user in users:  # for each user
            assign_perm(p, User.objects.get(pk=user))  # assign perm
    return render(request, 'add_perm_to_user.html', {
        'form': form,
        'users': users,
        'perms': perms,
        'toast': 'Permission to user added'
    })  # return success


@authentication_required
@has_global_perm('groups.change_group')
def change_group(request):
    """
    Edit group
    Can edit Group name, members and project membership status
    :param request: request object
    :return: webpage
    """
    all_users = User.objects.all()
    all_projects = Project.objects.all()
    form = ValidateGroupForm(request.POST)  # instantiate ValidateGroupForm
    if not request.method == 'POST':  # if not POST then its a get request or something else
        try:
            id_g = request.GET['id']  # if id parm not in url this will return MultiValueDictKeyError
            g = Group.objects.get(pk=id_g)  # get group we are editing

            # Create array of project primary keys for auto selecting html
            member_of_projects = []
            for project in get_group_project_membership(g):
                member_of_projects.append(project.pk)
            return render(request, 'change_group.html',
                          {'group': g,  # pass group we are editing to html
                           'users_in_grp': list(g.user_set.all().values_list('id', flat=True)),  # pass users already
                           # in group for preselection
                           'project_member': member_of_projects,  # pass projects the group is a member of
                           'projects': all_projects,
                           'users': all_users,  # pass users, to be able to add to group
                           'form': form})
        except MultiValueDictKeyError:
            return redirect('groups:view group objects')

    if not form.is_valid():
        return HttpResponse("<h1>form not valid!<h1>")

    name = form.cleaned_data.get('name')  # get name of group to be created
    users_to_add = request.POST.getlist('users')  # get users to add into group
    g_id = request.POST['id_group']
    group_to_edit = Group.objects.get(pk=g_id)

    member_of_projects = []
    for project in get_group_project_membership(group_to_edit):
        member_of_projects.append(project.pk)

    try:
        users_in_grp = list(group_to_edit.user_set.all().values_list('id', flat=True))
        update_user_group_membership(users_in_grp,
                                     users_to_add,
                                     group_to_edit, name)

        if request.POST.getlist('projects') != ['']:
            updated_project_memberships = request.POST.getlist('projects')
            update_group_project_membership(member_of_projects,
                                            updated_project_memberships,
                                            group_to_edit)
        # dont need to do anything or check if a user is in both lists
        return render(request, 'change_group.html',
                      {'form': form,
                       'users': all_users,
                       'group': group_to_edit,
                       'project_member': member_of_projects,  # pass projects the group is a member of
                       'projects': all_projects,
                       'users_in_grp': users_to_add,
                       'toast': 'Changed Group'})
    except IntegrityError:  # err; unique name. name exists already
        return render(  # return user to form with error msg
            request,
            'change_group.html',
            {'form': form,
             'users': all_users,
             'group': group_to_edit,
             'project_member': member_of_projects,  # pass projects the group is a member of
             'projects': all_projects,
             'users_in_grp': users_to_add,
             'error': "Team with this name already exists"
             })


@authentication_required
@has_global_perm('groups.change_group')
def add_perm_to_group(request):
    """
    Add perm to existing group
    Can add object based permission from group to project
    can add global permission to group
    :param request: request object
    :return: render template
    """

    form = ValidatePermToGroupForm()
    groups = Group.objects.all()
    projects = Project.objects.all()
    group_perms = get_perms_for_model(Group)
    project_perms = list(get_perms_for_model(Project))

    # remove 'member' perm from array. because we dont want to display this in the selector projectPerms
    remove_team_membership = Permission.objects.get(codename='member')
    project_perms.remove(remove_team_membership)

    # get perms that are supposed to be global only
    perm = get_global_perms()

    if not request.method == 'POST':
        return render(request, 'add_perm_to_group.html', {
            'perms': perm,
            'form': form,
            'groups': groups,
            'projects': projects,
            'groupPerms': group_perms,
            'projectPerms': project_perms,
        })
    form = ValidatePermToGroupForm(request.POST)
    if not form.is_valid():
        return render(request, 'add_perm_to_group.html', {
            'perms': perm,
            'form': form,
            'groups': groups,
            'error': 'Form is not valid!',
            'projects': projects,
            'groupPerms': group_perms,
            'projectPerms': project_perms,

        })
    group_id = form.cleaned_data.get('group_to_edit')
    group_to_edit = Group.objects.get(pk=group_id)

    # if all_perms present then add global perms, else do nothing
    if request.POST.getlist('all_perms'):
        set_group_global_perms(request.POST.getlist('all_perms'), group_to_edit)

    # if  project present then add perms, else do nothing
    if request.POST['projects']:
        project_id = request.POST['projects']
        id_of_project_perms_to_add = request.POST.getlist('projectPerms')
        set_group_project_perms(project_id, id_of_project_perms_to_add, group_to_edit)

    toast = "Updated permissions"

    return render(request, 'add_perm_to_group.html', {
        'perms': perm,
        'form': form,
        'groups': groups,
        'toast': toast,
        'projects': projects,
        'groupPerms': group_perms,
        'projectPerms': project_perms,

    })


def change_project(request):
    """
    method to change project detail
    """
    if check_perm(request.user, 'groups.change_project'):
        all_teams = Group.objects.all()
        form = ValidateProjectForm()
        if 'id' in request.GET and request.method == 'GET':
            id_p = request.GET['id']
            p = Project.objects.get(pk=id_p)
            teams_already = []
            for team in all_teams:
                checker = ObjectPermissionChecker(team)
                if checker.has_perm('member', p):
                    teams_already.append(team.pk)
            return render(request, 'change_project.html',
                          {'project': p,
                           'teams': all_teams,
                           'form': form,
                           'preselectTeams': teams_already
                           })

        elif request.method == 'POST':
            print(request.POST)
            form = ValidateProjectForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                team_to_add = request.POST.getlist('group')
                project_id = request.POST['id_project']
                project_to_edit = Project.objects.get(pk=project_id)
                project_to_edit.name = name
                project_to_edit.save()

                return render(request, 'change_project.html',
                              {'form': form,
                               'project_id': project_to_edit,
                               'teams': team_to_add,
                               'toast': 'Changed Project'})


# Create group, save creator of group
def create_group(group, author, is_perm_group):  # create group
    """
    creates new team or perm group, parms self-explanatory
    :param group: group object
    :param author: user object
    :param is_perm_group: boolean 0 og 1. 1(true) if perm group
    :return:
    """
    return Group.objects.create(name=group, author=author,
                                is_perm_group=is_perm_group)  # return group created with perms


# Create project, add group(s) to project, save creator of project
def create_project(project_name, author):  # create project
    """
    creates new project with project_name as name and author as author in db
    :param project_name: name of project
    :param author: author of project author of the project, User Object
    :return:
    """
    return Project.objects.create(name=project_name, author=author)  # return project created with perms


# TODO has been replaced by decorator
# Check if user is either in group, superuser, staff or has permission
def check_perm(user, perm):
    """
    method to check if user has specific perm, has perm through a group or is superuser or staff
    :param user: user object we are checking perm on
    :param perm: perm codename string
    :return:
    """
    perms_for_user = user.get_all_permissions()  # get all perms for user
    for permission in perms_for_user:  # for each permission in perms for user
        if permission == perm:  # check if perm equals perm required to access resource
            return True  # return true if so
    # else check if user is superuser, staff or has perm on user account object
    return user.is_superuser or user.is_staff or user.has_perm(perm) and not user.is_anonymous


def set_group_project_perms(project_id, id_of_project_perms_to_add, group_to_edit):
    """
    Update group perms on a project

    :param project_id => id of project that the group will  have perms on
    :param id_of_project_perms_to_add => id's of perms that the group will have on project
    :param group_to_edit => group object that we are adding perms to
    """
    project_to_edit = Project.objects.get(pk=project_id)
    perms_for_grp_proj = get_group_perms(group_to_edit, project_to_edit).values_list(
        'id',
        flat=True).exclude(
        codename='member')

    # if perm not in updated perm list from POST then remove
    for id_perm in perms_for_grp_proj:
        if id_perm not in map(int, id_of_project_perms_to_add):
            p = Permission.objects.get(pk=id_perm)
            remove_perm('Project.' + p.codename, group_to_edit, project_to_edit)

    # if perm not in Existing perms then add
    for id_perm in id_of_project_perms_to_add:
        if int(id_perm) not in map(int, perms_for_grp_proj):
            p = Permission.objects.get(pk=id_perm)
            # print('Project.' + p.codename)
            assign_perm('Project.' + p.codename, group_to_edit, project_to_edit)


def set_group_global_perms(global_perms_to_add, group_to_edit):
    """
    Changes global perms on a group
    :param group_to_edit => group object we are updating perms for
    :param global_perms_to_add => updated perms for group - array of global perm ID's
    """
    global_perms_already = group_to_edit.permissions.all()
    global_perms_already_arr = []
    for perm_obj in global_perms_already:
        global_perms_already_arr.append(perm_obj.pk)

    for perm_id in global_perms_already_arr:
        if int(perm_id) not in map(int, global_perms_to_add):
            p = Permission.objects.get(pk=perm_id)
            applabel = ContentType.objects.get(pk=p.content_type_id).app_label
            remove_perm(applabel + "." + p.codename, group_to_edit)
    for perm_id in global_perms_to_add:
        if int(perm_id) not in map(int, global_perms_already_arr):
            p = Permission.objects.get(pk=perm_id)
            applabel = ContentType.objects.get(pk=p.content_type_id).app_label
            assign_perm(applabel + "." + p.codename, group_to_edit)


# Get all project OBJS from DB that 'group' is member of
def get_group_project_membership(group):
    """
    Returns an array of projects that a specific group is a member of
    :param group: object of Group to check
    :return:
    """
    checker = ObjectPermissionChecker(group)
    projects = Project.objects.all()
    project_list = [project for project in projects if checker.has_perm('member', project)]
    return project_list


def update_user_group_membership(users_in_grp, users_to_add, group_to_edit, name):
    """
    helper method to update users in a group and the name of group

    :param users_in_grp => array of user id's that are already in the group
    :param users_to_add => array of updated user id's that are supposed to be in the group
    :param group_to_edit => object of group that we are updating members for
    :param name => name of the group
    """
    # if user is in group but not in updated group list
    for user in users_in_grp:
        if int(user) not in map(int, users_to_add):
            group_to_edit.user_set.remove(User.objects.get(pk=user))
    # if user is not in group already add to the group
    for user in users_to_add:
        if int(user) not in map(int, users_in_grp):
            group_to_edit.user_set.add(User.objects.get(pk=user))
    # change group name to set in post
    group_to_edit.name = name
    group_to_edit.save()


def update_group_project_membership(member_of_projects, updated_project_memberships, group_to_edit):
    for project in member_of_projects:
        if int(project) not in map(int, updated_project_memberships):
            # team is member but not in updated team project membership list .. remove
            remove_perm('member', group_to_edit, Project.objects.get(pk=project))
            member_of_projects.remove(project)  # update list used to auto select projects in Jquery

    for project in updated_project_memberships:
        if int(project) not in map(int, member_of_projects):
            # team is not member, and updated list has this team as member  in project
            assign_perm('member', group_to_edit, Project.objects.get(pk=project))
            member_of_projects.append(project)  # update list used to auto select projects in Jquery


# get list of all existing global perms
def get_global_perms():
    global_codenames = [
        # account
        'assign_create_group',
        'assign_create_project',
        # groups
        'add_perm_group',
        'edit_members_group',
        'report_generation_group',
        'handout_add_perm_group',
        'handout_edit_members_group',
        'handout_report_generation_group',
        'handout_view_group',
        'handout_change_group',
        'handout_change_group',
        'handout_add_group',
    ]
    perm = []
    for codename in global_codenames:
        perm.append(Permission.objects.get(codename=codename))
    return perm


@authentication_required
def ajax_load_group_info(request):
    """
    used to make ajax queries from template, in order to get more information about objects, dynamically
    instead of reloading page. Currently used to return Array of global perms a group has, as well as an array
    containing arr with k, v pair k = project_ID, v=perm.pk group has.
    :param request:
    :return:
    """

    try:
        grp_id = request.GET['group_id']
        group = Group.objects.get(pk=grp_id)
        project_objects = Project.objects.all()

        group_perms_on_projects = {}
        global_permissions = group.permissions.all().values_list('id', flat=True)

        for project in project_objects:
            print(get_group_perms(group, project).values_list('id', flat=True).exclude(codename='member'))
            group_perms_on_projects[project.id] = str(
                get_group_perms(group, project).values_list('id', flat=True).exclude(codename='member'))
        return JsonResponse({
            'group_perms_on_projects': group_perms_on_projects,
            'global_perms_preselect': list(global_permissions),
            # 'group_id_name': group_id_name
        })
    except MultiValueDictKeyError:
        return JsonResponse({'error': 'please supply group_id'})
