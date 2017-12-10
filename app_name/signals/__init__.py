# register all signals

from django.dispatch import Signal

# test
dummy_signal = Signal(providing_args=['param1'])
