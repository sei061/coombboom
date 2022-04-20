# Views

> Auto-generated documentation for [groups.views](..\..\groups\views.py) module.

- [Coombboom](..\README.md#coombboom-index) / [Modules](..\MODULES.md#coombboom-modules) / [Groups](index.md#groups) / Views
    - [add_new_group](#add_new_group)
    - [add_new_project](#add_new_project)
    - [add_perm_group](#add_perm_group)
    - [add_perm_to_group](#add_perm_to_group)
    - [add_perm_user](#add_perm_user)
    - [ajax_load_group_info](#ajax_load_group_info)
    - [change_group](#change_group)
    - [change_project](#change_project)
    - [check_perm](#check_perm)
    - [create_group](#create_group)
    - [create_project](#create_project)
    - [get_global_perms](#get_global_perms)
    - [get_group_project_membership](#get_group_project_membership)
    - [set_group_global_perms](#set_group_global_perms)
    - [set_group_project_perms](#set_group_project_perms)
    - [update_group_project_membership](#update_group_project_membership)
    - [update_user_group_membership](#update_user_group_membership)
    - [view_groups](#view_groups)
    - [view_projects](#view_projects)

## add_new_group

[[find in source code]](..\..\groups\views.py#L43)

```python
def add_new_group(request):
```

add new team, handles form & post data

#### Arguments

- `request`

## add_new_project

[[find in source code]](..\..\groups\views.py#L102)

```python
def add_new_project(request):
```

add new project, renders form & handles post

#### Arguments

- `request`

## add_perm_group

[[find in source code]](..\..\groups\views.py#L143)

```python
def add_perm_group(request):
```

add permission group, render form & handle post

#### Arguments

- `request`

## add_perm_to_group

[[find in source code]](..\..\groups\views.py#L302)

```python
def add_perm_to_group(request):
```

Add perm to existing group
Can add object based permission from group to project
can add global permission to group

#### Arguments

- `request`

## add_perm_user

[[find in source code]](..\..\groups\views.py#L190)

```python
def add_perm_user(request):
```

add permission to user

#### Arguments

- `request`

#### Returns

webpage

## ajax_load_group_info

[[find in source code]](..\..\groups\views.py#L550)

```python
def ajax_load_group_info(request):
```

used to make ajax queries from template, in order to get more information about objects, dynamically
instead of reloading page. Currently used to return Array of global perms a group has, as well as an array
containing arr with k, v pair k = project_ID, v=perm.pk group has.

#### Arguments

- `request`

## change_group

[[find in source code]](..\..\groups\views.py#L223)

```python
def change_group(request):
```

Edit group
Can edit Group name, members and project membership status

#### Arguments

- `request`

#### Returns

webpage

## change_project

[[find in source code]](..\..\groups\views.py#L375)

```python
def change_project(request):
```

## check_perm

[[find in source code]](..\..\groups\views.py#L431)

```python
def check_perm(user, perm):
```

method to check if user has specific perm, has perm through a group or is superuser or staff

#### Arguments

- `user`
- `perm`

## create_group

[[find in source code]](..\..\groups\views.py#L407)

```python
def create_group(group, author, is_perm_group):
```

creates new team or perm group, parms self-explanatory

#### Arguments

- `group`
- `author`
- `is_perm_group`

## create_project

[[find in source code]](..\..\groups\views.py#L420)

```python
def create_project(project_name, author):
```

creates new project with project_name as name and author as author in db

#### Arguments

- `project_name` - name of project
- `author` - author of project

## get_global_perms

[[find in source code]](..\..\groups\views.py#L527)

```python
def get_global_perms():
```

## get_group_project_membership

[[find in source code]](..\..\groups\views.py#L486)

```python
def get_group_project_membership(group):
```

Returns an array of projects that a specific group is a member of

#### Arguments

- `group`

## set_group_global_perms

[[find in source code]](..\..\groups\views.py#L467)

```python
def set_group_global_perms(global_perms_to_add, group_to_edit):
```

## set_group_project_perms

[[find in source code]](..\..\groups\views.py#L446)

```python
def set_group_project_perms(
    project_id,
    id_of_project_perms_to_add,
    group_to_edit,
):
```

## update_group_project_membership

[[find in source code]](..\..\groups\views.py#L512)

```python
def update_group_project_membership(
    member_of_projects,
    updated_project_memberships,
    group_to_edit,
):
```

## update_user_group_membership

[[find in source code]](..\..\groups\views.py#L498)

```python
def update_user_group_membership(
    users_in_grp,
    users_to_add,
    group_to_edit,
    name,
):
```

## view_groups

[[find in source code]](..\..\groups\views.py#L19)

```python
def view_groups(request):
```

returns view of all groups in db

#### Arguments

- `request`

## view_projects

[[find in source code]](..\..\groups\views.py#L30)

```python
def view_projects(request):
```

returns view of all projects

#### Arguments

- `request`
