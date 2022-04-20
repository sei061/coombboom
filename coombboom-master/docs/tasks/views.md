# Views

> Auto-generated documentation for [tasks.views](..\..\tasks\views.py) module.

- [Coombboom](..\README.md#coombboom-index) / [Modules](..\MODULES.md#coombboom-modules) / [Tasks](index.md#tasks) / Views
    - [create_task](#create_task)
    - [display_task](#display_task)
    - [task](#task)

## create_task

[[find in source code]](..\..\tasks\views.py#L17)

```python
def create_task(request):
```

Method for creating a task. Tasks can be project-specific, if not they are global

#### Arguments

- `request` - A request that collects the task inputs

#### Returns

returns a render of the html-page with a toast depending on the result

## display_task

[[find in source code]](..\..\tasks\views.py#L54)

```python
def display_task(request):
```

Method for displaying tasks in a list. A task can be selected and edited if necessary.

#### Arguments

- `request` - A request that gets the selected task from the list.

#### Returns

returns a render of the html-page for task editing.

## task

[[find in source code]](..\..\tasks\views.py#L13)

```python
def task(request):
```
