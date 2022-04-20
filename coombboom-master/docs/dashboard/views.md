# Views

> Auto-generated documentation for [dashboard.views](..\..\dashboard\views.py) module.

- [Coombboom](..\README.md#coombboom-index) / [Modules](..\MODULES.md#coombboom-modules) / [Dashboard](index.md#dashboard) / Views
    - [get_actual_line](#get_actual_line)
    - [get_ideal_and_goal_line](#get_ideal_and_goal_line)
    - [get_labels_for_chart](#get_labels_for_chart)
    - [get_maximum_storypoints](#get_maximum_storypoints)
    - [load_grps_proj](#load_grps_proj)
    - [percentage_done](#percentage_done)
    - [project](#project)
    - [team](#team)

## get_actual_line

[[find in source code]](..\..\dashboard\views.py#L76)

```python
def get_actual_line(workreg, labels):
```

get actual_line data from workreg sorted by date oldest to youngest

#### Arguments

- `workreg` - array of wokrerg registrations for project
- `labels` - is array of labels

## get_ideal_and_goal_line

[[find in source code]](..\..\dashboard\views.py#L50)

```python
def get_ideal_and_goal_line(tasks, labels, max_y_points):
```

Creates a list of 2 lists
list[0] creates array of data for the perfect ideal line for chart based on max Yaxes
points and how many labels exists

list[1] creates array of data for goal line in chart,, which is just [max_y_points, <---> ... ]

#### Arguments

- `tasks` - is for example Task.objects.filter(projects_id=2)
- `labels` - is array of labels
- `max_y_points` - maximum number for Yaxes

## get_labels_for_chart

[[find in source code]](..\..\dashboard\views.py#L14)

```python
def get_labels_for_chart(tasks):
```

Method to get labels for chart
Takes array of tasks for project
returns array with oldest date incrementing to youngest date for all tasks on project

#### Arguments

- `tasks` - is for example Task.objects.filter(projects_id=2)

## get_maximum_storypoints

[[find in source code]](..\..\dashboard\views.py#L38)

```python
def get_maximum_storypoints(tasks):
```

get maximum of number for Yaxes in chart

#### Arguments

- `tasks` - is for example Task.objects.filter(projects_id=2)

## load_grps_proj

[[find in source code]](..\..\dashboard\views.py#L193)

```python
def load_grps_proj(request):
```

## percentage_done

[[find in source code]](..\..\dashboard\views.py#L102)

```python
def percentage_done(workreg, max_y_points):
```

Get percentage done total time spent / total time planned
:param workreg array of workreg objects

#### Arguments

- `max_y_points` - maximum number for Yaxes

## project

[[find in source code]](..\..\dashboard\views.py#L121)

```python
def project(request):
```

display data in /dashboard/project?id=x
displays visual chart for project progress
displays progressbar with percent complete
displays tasks for project

#### Arguments

- `request` - is for example Task.objects.filter(projects_id=2)

## team

[[find in source code]](..\..\dashboard\views.py#L157)

```python
def team(request):
```
