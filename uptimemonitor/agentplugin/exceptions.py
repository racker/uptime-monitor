class TooManyMetricsError(Exception):
    def __init__(self, max_metrics=10):
        msg = "Maximum of %d metrics allowed" % max_metrics
        super(TooManyMetricsError, self).__init__(msg)


class UnknownMetricTypeError(Exception):
    def __init__(self, metric_type):
        msg = "Invalid type: %s" % metric_type
        super(UnknownMetricTypeError, self).__init__(msg)


class InvalidMetricNameError(Exception):
    def __init__(self, name):
        if name is None:
            msg = "Invalid name: cannot be <None>"
        elif len(name) == 0:
            msg = "Invalid name: cannot be <empty>"
        else:
            msg = "Invalid name: %s" % name
        super(InvalidMetricNameError, self).__init__(msg)
