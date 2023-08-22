from abc import ABC, abstractmethod


class ActionBase(ABC):
    @staticmethod
    @abstractmethod
    def setup(instance, **kwargs):
        """
        One time setup for parent run
        """

    @staticmethod
    @abstractmethod
    def before(instance, **kwargs):
        """
        Executes before each child run
        """

    @staticmethod
    @abstractmethod
    def on_success(instance, **kwargs):
        """
        Executes after each successful child run
        """

    @staticmethod
    @abstractmethod
    def on_failure(instance, **kwargs):
        """
        Executes after each failed child run
        """

    @staticmethod
    @abstractmethod
    def after(instance, **kwargs):
        """
        Executes after each child run
        """

    @staticmethod
    @abstractmethod
    def teardown(instance, **kwargs):
        """
        One time teardown for parent run
        """
