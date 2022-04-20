# Views

> Auto-generated documentation for [invitation.views](..\..\invitation\views.py) module.

- [Coombboom](..\README.md#coombboom-index) / [Modules](..\MODULES.md#coombboom-modules) / [Invitation](index.md#invitation) / Views
    - [create_token](#create_token)
    - [disable_token](#disable_token)
    - [enable_token](#enable_token)
    - [encode_token](#encode_token)
    - [get_email_through_token](#get_email_through_token)
    - [invitation](#invitation)
    - [invite_exists](#invite_exists)
    - [verify_token](#verify_token)

## create_token

[[find in source code]](..\..\invitation\views.py#L79)

```python
def create_token(referer_id, recipient):
```

#### Arguments

- `referer_id`
- `recipient`

## disable_token

[[find in source code]](..\..\invitation\views.py#L17)

```python
def disable_token(token):
```

#### Arguments

- `token`

## enable_token

[[find in source code]](..\..\invitation\views.py#L29)

```python
def enable_token(email):
```

#### Arguments

- `email`

## encode_token

[[find in source code]](..\..\invitation\views.py#L67)

```python
def encode_token(email):
```

#### Arguments

- `email`

## get_email_through_token

[[find in source code]](..\..\invitation\views.py#L11)

```python
def get_email_through_token(token):
```

## invitation

[[find in source code]](..\..\invitation\views.py#L94)

```python
def invitation(request):
```

#### Arguments

- `request`

## invite_exists

[[find in source code]](..\..\invitation\views.py#L57)

```python
def invite_exists(email):
```

#### Arguments

- `email`

## verify_token

[[find in source code]](..\..\invitation\views.py#L41)

```python
def verify_token(token):
```

#### Arguments

- `token`
