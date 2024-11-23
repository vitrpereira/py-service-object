from abc import ABC, abstractmethod
from functools import lru_cache, cached_property
from typing import Any, List, Dict

# flake8: noqa: E501
class ServiceObject(ABC):
    """
    ServiceObject is an abstract base class that provides a standardized way to encapsulate business logic.
    It follows the Service Object pattern, where each concrete implementation represents a single business operation.

    The class provides error handling, result caching, and a consistent 
    interface through the following key methods:
    - call(): Abstract method that contains the main business logic
    - result(): Cached property that executes and returns the result of call()
    - success(): Property that indicates if the operation completed without errors
    - errors(): Property that returns any errors that occurred during execution

    Example:
        class CreateUser(ServiceObject):
            def __init__(self, user_params):
                self.user_params = user_params
                super().__init__()
            
            def call(self):
                try:
                    user = User.create(self.user_params)
                    return user
                except Exception as e:
                    self.errors.append({"message": str(e)})
                    return None

    Usage:
        service = CreateUser(user_params)
        if service.success:
            user = service.result
        else:
            errors = service.errors
    """
    
    class ServiceObjectError(Exception):
        """Base exception for all service object errors."""
        pass

    class InvalidErrorType(ServiceObjectError):
        def __init__(self, error: Any):
            self.error = error

        def __str__(self):
            err_message = "Invalid error type. Valid error types are dictionaries. "
            err_message += f"Received type '{self.error.__class__.__name__}'"

            return err_message

    def __init__(self):
        self._errors = []

    @lru_cache
    @abstractmethod
    def call(self) -> Any:
        """
        Abstract method that contains the main business logic of the service object.
        This method must be implemented by all subclasses.

        Returns:
            Any: The result of executing the service object's business logic.

        Example:
            def call(self):
                try:
                    result = perform_business_logic()
                    return result
                except Exception as e:
                    self.errors.append({"message": str(e.message)})
                    return None
        """
        pass

    @cached_property
    def result(self) -> Any:
        """
        Returns the result of executing the service object by calling the `call` method.
        The result is cached using @cached_property to avoid multiple executions.

        Returns:
            Any: The return value from the `call` method implementation.
        """
        return self.call()

    @property
    def success(self) -> bool:
        """
        Returns whether the service object execution was successful.
        A service object is considered successful if it has no errors.

        Returns:
            bool: True if no errors occurred, False otherwise.
        """
        return len(self.errors) == 0
    
    @property
    def errors(self) -> List[Dict[str, str]]:
        """
        Returns the list of errors that occurred during service object execution.
        Each error should be a dictionary with a 'message' key containing the error description.

        Returns:
            list: A list of error dictionaries. Empty list if no errors occurred.

        Raises:
            InvalidErrorType: If any error in the list is not a dictionary.
        """
        if not (errors := self._errors):
            return errors
        
        for error in self._errors:
            if not isinstance(error, dict):
                raise self.InvalidErrorType(error)
            
        return errors
