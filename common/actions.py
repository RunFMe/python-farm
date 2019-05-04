from abc import ABCMeta, abstractmethod
from common.utils import cls_init


class SignalDecoder:
    signals = {}

    def __new__(cls, *args, **kwargs):
        raise NotImplementedError("Signal Decoder can not be instantiated")

    @classmethod
    def register_signal(cls, signal_code, signal_cls):
        if signal_code in cls.signals:
            raise AttributeError(
                "Signal {} is already registered".format(signal_code))

        cls.signals[signal_code] = signal_cls

    @classmethod
    def decode(cls, signal_code, signal_arguments):
        if signal_code not in cls.signals:
            raise AttributeError(
                "Signal {} is not registered".format(signal_code))

        return cls.signals[signal_code].decode(signal_arguments)


class Signal(metaclass=ABCMeta):
    @abstractmethod
    def encode(self):
        """
        Returns signal tuple (signal_name, signal_arguments)
        :return: encoded_signal
        """

    @staticmethod
    @abstractmethod
    def decode(cls, arguments):
        """
        Restores signal object from arguments
        :param cls:
        :param arguments:
        :return:
        """


@cls_init
class AuthSignal(Signal):
    @classmethod
    def cls_init(cls):
        cls.signal_code = 'auth'
        SignalDecoder.register_signal(cls.signal_code, cls)

    def encode(self):
        return self.signal_code, {'name': self.name}

    @staticmethod
    def decode(self, arguments):
        return AuthSignal(arguments['name'])

    def __init__(self, name):
        self.name = name

