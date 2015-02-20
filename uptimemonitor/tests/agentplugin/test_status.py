from uptimemonitor.agentplugin.status import Status
import uptimemonitor.agentplugin.exceptions as ex
import unittest


class TestStatus(unittest.TestCase):

    def test_create_default(self):
        result = Status()
        self.assertEquals('OK', result._status)
        self.assertIsInstance(result._metrics, list)
        self.assertEquals(0, len(result._metrics))

    def test_create_with_status(self):
        result = Status('Fail')
        self.assertEquals('Fail', result._status)
        self.assertIsInstance(result._metrics, list)
        self.assertEquals(0, len(result._metrics))

    def test_to_str_no_metrics(self):
        result = Status('Fail')
        self.assertEquals('status Fail', str(result))

    def test_to_str(self):
        result = Status('SUCCESS')
        expected = 'status SUCCESS'
        for i in range(10):
            result.add_metric('ping_time_ms_%d' % (i + 1), 'uint64', 325)
            expected += '\nmetric ping_time_ms_%d uint64 325' % (i + 1)

        self.assertEquals(expected, str(result))

    def test_add_metric(self):
        result = Status()
        result.add_metric('ping_time_ms', 'uint64', 325)
        self.assertEquals(1, len(result._metrics))
        self.assertIn(('ping_time_ms', 'uint64', '325'), result._metrics)

    def test_add_metric_name_none(self):
        result = Status()
        self.assertRaisesRegexp(ex.InvalidMetricNameError,
                                'Invalid name: cannot be <None>',
                                result.add_metric,
                                None, 'uint64', 325)

    def test_add_metric_name_empty(self):
        result = Status()
        self.assertRaisesRegexp(ex.InvalidMetricNameError,
                                'Invalid name: cannot be <empty>',
                                result.add_metric,
                                '', 'uint64', 325)

    def test_add_metric_bad_name(self):
        result = Status()
        self.assertRaisesRegexp(ex.InvalidMetricNameError,
                                'Invalid name: Money\$Bills',
                                result.add_metric,
                                'Money$Bills', 'uint64', 325)

    def test_add_metric_bad_type(self):
        result = Status()
        self.assertRaisesRegexp(ex.UnknownMetricTypeError,
                                'Invalid type: corn',
                                result.add_metric,
                                'ping_time_ms', 'corn', 325)

    def test_add_too_many_metrics(self):
        result = Status()
        for i in range(10):
            result.add_metric('ping_time_ms_%d' % (i + 1), 'uint64', 325)

        self.assertRaisesRegexp(ex.TooManyMetricsError,
                                'Maximum of 10 metrics allowed',
                                result.add_metric,
                                'ping_time_ms_11', 'uint64', 325)
