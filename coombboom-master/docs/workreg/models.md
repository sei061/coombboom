# Models

> Auto-generated documentation for [workreg.models](..\..\workreg\models.py) module.

- [Coombboom](..\README.md#coombboom-index) / [Modules](..\MODULES.md#coombboom-modules) / [Workreg](index.md#workreg) / Models
    - [Entry](#entry)
        - [Entry().total_duration](#entrytotal_duration)

## Entry

[[find in source code]](..\..\workreg\models.py#L15)

```python
class Entry(models.Model):
```

Represent record a log created by user to track Project.

### Entry().total_duration

[[find in source code]](..\..\workreg\models.py#L43)

```python
@property
def total_duration():
```

Entry's property for the total duration alloted
