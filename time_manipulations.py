import time
import calendar
import unittest

class TimeManipulations(unittest.TestCase):
    # This code works in CET timezone
    def test_seconds_to_tuple(self):
        seconds = 0  # Can come from time.time()
        self.assertEqual(time.gmtime(seconds), (1970, 1, 1, 0, 0, 0, 3, 1, 0))
        self.assertEqual(calendar.timegm(time.gmtime(seconds)), seconds)
        self.assertEqual(time.localtime(seconds), (1970, 1, 1, 1, 0, 0, 3, 1, 0))
        self.assertEqual(time.mktime(time.localtime(seconds)), seconds)

    def test_tuple_conversion_wrong_timezones(self):
        seconds = 0
        self.assertEqual(calendar.timegm(time.localtime(seconds)), seconds + 3600)
        self.assertEqual(time.mktime(time.gmtime(seconds)), -3600)

    def test_string_conversions(self):
        seconds = 0
        tp = time.gmtime(seconds)
        self.assertEqual(time.asctime(tp), 'Thu Jan  1 00:00:00 1970')

        parsed = time.strptime('Thu Jan  1 00:00:00 1970')
        self.assertEqual(tp.tm_year, parsed.tm_year)
        self.assertEqual(tp.tm_mon, parsed.tm_mon)
        self.assertEqual(tp.tm_mday, parsed.tm_mday)
        self.assertEqual(tp.tm_hour, parsed.tm_hour)
        self.assertEqual(tp.tm_min, parsed.tm_min)
        self.assertEqual(tp.tm_sec, parsed.tm_sec)
        self.assertEqual(tp.tm_wday, parsed.tm_wday)
        self.assertEqual(tp.tm_yday, parsed.tm_yday)
        self.assertEqual(tp.tm_isdst, 0)
        self.assertEqual(parsed.tm_isdst, -1)
        self.assertEqual(tp.tm_zone, 'UTC')
        self.assertEqual(parsed.tm_zone, None)

    def test_comparisons(self):
        # With the time module we don't really have freedom to check different timezones
        # We can check only UTC and local timezone
        # Let's consider the following 2 ways of comparing the time representations
        #
        # Seconds since epoch

        seconds = 0  # Not using time.time() as the tests will fail during DST
        gmt = time.gmtime(seconds)
        lcl = time.localtime(seconds)

        seconds_gmt = calendar.timegm(gmt)
        seconds_lcl = time.mktime(lcl)

        self.assertEqual(seconds_gmt, seconds_lcl)

        # Comparing the tuples directly
        # We see that even though they represent the same moment,
        # as they fall into different timezones, they don't adjust for it
        # when comparing
        self.assertGreater(lcl, gmt)
        # It works only if the tuple objects themselves are equal
        self.assertEqual(time.gmtime(seconds), time.gmtime(seconds))
        self.assertEqual(time.localtime(seconds), time.localtime(seconds))
        self.assertEqual(time.gmtime(seconds + 3600), time.localtime(seconds))

    def test_delta(self):
        # The struct_time properties are read-only
        # Hence we can't directly change these objects and we don't
        # have convenient APIs for directly manipulating them

        seconds = 0
        delta = 100

        gmt = time.gmtime(seconds)
        lcl = time.localtime(seconds)

        # Manipulating the gmt

        gmt_with_delta = time.gmtime(calendar.timegm(gmt) + delta)
        self.assertEqual(seconds + delta, calendar.timegm(gmt_with_delta))

        # Manipulating the lcl

        lcl_with_delta = time.localtime(time.mktime(lcl) + delta)
        self.assertEqual(seconds + delta, time.mktime(lcl_with_delta))

        # Just slightly hacking here, showing that the local struct_time
        # can be processed with the gm apis, the result will be correct, as
        # the UTC assumption goes in both ways and cancells itself.
        # But we also see that still we lose information about the timezone.
        # So if we have to use time python library, we should make sure we use
        # the right APIs.

        lcl_with_delta_with_gmt_processing = time.gmtime(calendar.timegm(lcl) + delta)
        self.assertEqual(seconds + delta, time.mktime(lcl_with_delta_with_gmt_processing))
        self.assertEqual(lcl_with_delta, lcl_with_delta_with_gmt_processing)
        self.assertEqual(lcl_with_delta.tm_zone, 'CET')
        self.assertEqual(lcl_with_delta_with_gmt_processing.tm_zone, 'UTC')



if __name__ == '__main__':
    unittest.main()
