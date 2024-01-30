import re

from functools import wraps
from allure_commons import plugin_manager
from allure_commons.utils import uuid4, func_parameters


def step(title, display_params=False):
    if callable(title):
        func = title
        name: str = title.__name__
        display_name = re.sub(r'_+', ' ', name)
        return StepContext(
            display_name,
            {},
            display_params=display_params)(func)
    else:
        return StepContext(title, {})


class StepContext:

    def __init__(self, title, params, display_params=True):
        self.title = title
        self.params = params
        self.uuid = uuid4()
        self.display_params = display_params

    def __enter__(self):
        plugin_manager.hook.start_step(
            uuid=self.uuid,
            title=self.title,
            params=self.params)

    def __exit__(self, exc_type, exc_val, exc_tb):
        plugin_manager.hook.stop_step(
            uuid=self.uuid,
            title=self.title,
            exc_type=exc_type,
            exc_val=exc_val,
            exc_tb=exc_tb)

    def __call__(self, func):
        @wraps(func)
        def impl(*args, **kw):
            __tracebackhide__ = True

            params = func_parameters(func, *args, **kw)
            params_values = list(params.values())
            stringified_params = ', '.join(params_values)

            def params_to_display():
                if not params_values:
                    return ''
                if len(params_values) == 1:
                    return ' ' + params_values[0]
                return ': ' + stringified_params

            name_to_display = \
                self.title + \
                (params_to_display() if self.display_params else '')

            with StepContext(name_to_display, params):
                return func(*args, **kw)

        return impl
