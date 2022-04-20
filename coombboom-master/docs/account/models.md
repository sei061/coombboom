# Models

> Auto-generated documentation for [account.models](..\..\account\models.py) module.

- [Coombboom](..\README.md#coombboom-index) / [Modules](..\MODULES.md#coombboom-modules) / [Account](index.md#account) / Models
    - [DeletedUsers](#deletedusers)
    - [MyAccountManager](#myaccountmanager)
        - [MyAccountManager().create_superuser](#myaccountmanagercreate_superuser)
        - [MyAccountManager().create_user](#myaccountmanagercreate_user)
    - [User](#user)
        - [User().has_module_perms](#userhas_module_perms)
        - [User().has_perm](#userhas_perm)

## DeletedUsers

[[find in source code]](..\..\account\models.py#L79)

```python
class DeletedUsers(models.Model):
```

## MyAccountManager

[[find in source code]](..\..\account\models.py#L7)

```python
class MyAccountManager(BaseUserManager):
```

### MyAccountManager().create_superuser

[[find in source code]](..\..\account\models.py#L25)

```python
def create_superuser(email, username, password):
```

### MyAccountManager().create_user

[[find in source code]](..\..\account\models.py#L8)

```python
def create_user(email, username, password):
```

## User

[[find in source code]](..\..\account\models.py#L41)

```python
class User(AbstractUser):
```

### User().has_module_perms

[[find in source code]](..\..\account\models.py#L68)

```python
def has_module_perms(app_label):
```

### User().has_perm

[[find in source code]](..\..\account\models.py#L63)

```python
def has_perm(perm, obj=None):
```
