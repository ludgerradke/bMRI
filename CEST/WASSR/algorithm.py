import abc


class Algorithm(abc.ABC):
    def __init__(self, *args, **kwargs):
       super(Algorithm, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def calculate(self, ppms, values):
        pass
