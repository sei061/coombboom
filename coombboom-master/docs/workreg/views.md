# Views

> Auto-generated documentation for [workreg.views](..\..\workreg\views.py) module.

- [Coombboom](..\README.md#coombboom-index) / [Modules](..\MODULES.md#coombboom-modules) / [Workreg](index.md#workreg) / Views
    - [DeleteEntryView](#deleteentryview)
    - [delete_entry](#delete_entry)
    - [list](#list)
    - [load_tasks](#load_tasks)
    - [new](#new)
    - [start_pause](#start_pause)
    - [stop](#stop)
    - [workreg_update_view](#workreg_update_view)

## DeleteEntryView

[[find in source code]](..\..\workreg\views.py#L203)

```python
class DeleteEntryView(DeleteView):
```

## delete_entry

[[find in source code]](..\..\workreg\views.py#L209)

```python
def delete_entry(request, pk):
```

## list

[[find in source code]](..\..\workreg\views.py#L120)

```python
def list(request):
```

A method that makes a list of all the registered workregs from all users. We can also use this to
make individual lists based on who created the workregs.

#### Arguments

- `request` - A request that collects the workreg inputs

#### Returns

returns a render of the html-page that shows list of all workregs

## load_tasks

[[find in source code]](..\..\workreg\views.py#L217)

```python
def load_tasks(request):
```

This method is used so we can have independency between projects and tasks. So if you choose a project
only tasks thats is created under that project will be shown.

#### Arguments

- `request` - A request that collects the projects inputs

#### Returns

returns a render of the html-page that lists all the tasks under specific projects

## new

[[find in source code]](..\..\workreg\views.py#L22)

```python
def new(request):
```

A method that lets user register their own timestamps for when working with a specific
project and task. Also makes you choose date from-end and timestamps from-end.

#### Arguments

- `request` - A request that collects the workreg inputs

#### Returns

returns a render of the html-page with a toast depending on the result

## start_pause

[[find in source code]](..\..\workreg\views.py#L178)

```python
def start_pause(request):
```

This is not in use. Plan was to make the user be able to stop and start specific workregs when
they went to lunsj etc.

#### Arguments

- `request` - A request that collects the workreg inputs

#### Returns

returns a render of the html-page that shows list of all workregs

## stop

[[find in source code]](..\..\workreg\views.py#L151)

```python
def stop(request):
```

This method is not in use. The plan was to make a stop button to let users stop the workreg when they
wanted to.

#### Arguments

- `request` - A request that collects the workreg inputs

#### Returns

returns a render of the html-page that shows list of all workregs

## workreg_update_view

[[find in source code]](..\..\workreg\views.py#L101)

```python
def workreg_update_view(request, pk):
```

A method that makes users edit their own workregs

#### Arguments

- `request` - A request that collects the workreg inputs
- `pk` - gets the PK of the logged in user

#### Returns

returns a render of the html-page with a toast depending on the result
