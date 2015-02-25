import string
import uptimemonitor.agentplugin.exceptions as ex

_TYPES = ['int32', 'uint32', 'int64', 'uint64', 'double', 'string']
_VALID_CHARS = string.ascii_letters + string.digits + ':_.'
_MAX_METRICS = 10


class Status(object):
    def __init__(self, status='OK'):
        self._status = status
        self._metrics = []

    def _is_name_valid(self, name):
        for c in name:
            if c not in _VALID_CHARS:
                return False
        return True

    def add_metric(self, name, metric_type, value):
        if name is None or len(name) < 1 or not self._is_name_valid(name):
            raise ex.InvalidMetricNameError(name=name)

        if len(self._metrics) == _MAX_METRICS:
            raise ex.TooManyMetricsError(max_metrics=_MAX_METRICS)

        if metric_type not in _TYPES:
            raise ex.UnknownMetricTypeError(metric_type=metric_type)

        self._metrics.append((name, metric_type, str(value)))

    def __str__(self):
        results = [
            'status %s' % self._status
        ]

        for metric in self._metrics:
            results.append('metric %s %s %s' % metric)

        return '\n'.join(results)
