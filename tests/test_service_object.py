import pytest
from src.py_service_object import ServiceObject


# Test implementation of ServiceObject
class SuccessfulService(ServiceObject):
    def __init__(self, return_value=None):
        self.return_value = return_value
        super().__init__()

    def call(self):
        return self.return_value


class FailingService(ServiceObject):
    def call(self):
        self._errors.append({"message": "Something went wrong"})
        return None


class InvalidErrorService(ServiceObject):
    def call(self):
        self._errors.append("Invalid error format")
        return None


def test_cannot_instantiate_abstract_class():
    """Test that ServiceObject cannot be instantiated directly"""
    with pytest.raises(TypeError):
        ServiceObject()


def test_successful_service():
    """Test a service that executes successfully"""
    expected_value = {"data": "test"}
    service = SuccessfulService(expected_value)

    assert service.success is True
    assert service.result == expected_value
    assert service.errors == []


def test_failing_service():
    """Test a service that fails with proper error format"""
    service = FailingService()

    # Execute the service by accessing result
    assert service.result is None
    assert service.success is False
    assert len(service.errors) == 1
    assert service.errors[0] == {"message": "Something went wrong"}


def test_invalid_error_format():
    """Test that invalid error format raises InvalidErrorType"""
    service = InvalidErrorService()
    service.call()  # Execute the service

    with pytest.raises(ServiceObject.InvalidErrorType) as exc_info:
        _ = service.errors

    assert str(exc_info.value).startswith("Invalid error type")
    assert "str" in str(exc_info.value)


def test_result_caching():
    """Test that result is cached and call() is only executed once"""
    class CountingService(ServiceObject):
        def __init__(self):
            self.call_count = 0
            super().__init__()

        def call(self):
            self.call_count += 1
            return self.call_count

    service = CountingService()

    # Access result multiple times without calling call() directly
    assert service.result == 1
    assert service.result == 1
    assert service.result == 1

    # Verify call() was only executed once
    assert service.call_count == 1

    # Now verify that calling call() explicitly before accessing result
    # does not cause call() to be executed again when result is accessed
    service2 = CountingService()

    # Explicitly call the service once
    assert service2.call() == 1
    assert service2.call_count == 1

    # Accessing result should return the cached value without incrementing call_count
    assert service2.result == 1
    assert service2.result == 1
    assert service2.call_count == 1


def test_multiple_errors():
    """Test handling multiple errors"""
    class MultiErrorService(ServiceObject):
        def call(self):
            self._errors.append({"message": "Error 1"})
            self._errors.append({"message": "Error 2"})
            return None

    service = MultiErrorService()

    # Execute the service by accessing result
    assert service.result is None
    assert service.success is False
    assert len(service.errors) == 2
    assert service.errors[0] == {"message": "Error 1"}
    assert service.errors[1] == {"message": "Error 2"}


def test_empty_result():
    """Test service returning None explicitly"""
    service = SuccessfulService(None)

    assert service.success is True
    assert service.result is None
    assert service.errors == []


def test_error_property_caching():
    """Test that errors property doesn't cache results"""
    class DynamicErrorService(ServiceObject):
        def call(self):
            self._errors.append({"message": "Initial error"})
            return None

    service = DynamicErrorService()
    service.call()

    # Initial error check
    assert len(service.errors) == 1

    # Add another error
    service._errors.append({"message": "Second error"})

    # Should reflect the new error
    assert len(service.errors) == 2
