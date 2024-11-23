# py-service-object

A Python implementation of the Service Object pattern, inspired by Ruby's SimpleCommand gem.

## Installation

```bash
pip install py-service-object
```

## Usage

```python
from py_service_object import ServiceObject

class CreateUser(ServiceObject):
    def init(self, user_params):
        self.user_params = user_params
        super().init()

    def call(self):
        try:
            user = User.create(self.user_params)
            return user
        except Exception as e:
            self.errors.append({"message": str(e)})
            return None
```

## Using the ServiceObject

```python
service = CreateUser(user_params)
if service.success:
    user = service.result
else:
errors = service.errors
```

## Features

- Encapsulates business logic in dedicated classes
- Built-in error handling
- Result caching
- Clean and consistent interface
- Type hints support
