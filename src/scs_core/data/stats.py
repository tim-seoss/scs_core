"""
Created on 3 Mar 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://en.wikipedia.org/wiki/Standard_deviation


example documents:
Stats:
{"tag": "scs-bgx-619", "val": {"VOC": {"cnc": {"count": 4320, "min": 397.7, "mean": 448.2, "median": 446.1,
"max": 498.9, "var": 375.6, "stdev": 19.4, "stdev2": 38.8, "stdev3": 58.2}}}}

StatsAnalysis:
{"tag": "scs-bgx-619", "val": {"VOC": {"cnc": {"min": 397.7, "mean": 448.2, "max": 498.9,
"l3": 387.9,  "l2": 407.3, "l1": 426.7, "u1": 465.5, "u2": 484.9, "u3": 504.3, "a1": 38.8, "a2": 77.6, "a3": 116.4}}}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Stats(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, values, prec=3):
        import statistics                               # late import

        minimum = round(min(values), prec)
        mean = round(statistics.mean(values), prec)
        median = round(statistics.median(values), prec)
        maximum = round(max(values), prec)

        variance = round(statistics.variance(values, xbar=mean), prec)

        stdev = round(statistics.stdev(values), prec)
        stdev2 = round(stdev * 2.0, prec)
        stdev3 = round(stdev * 3.0, prec)

        return cls(len(values), minimum, mean, median, maximum, variance, stdev, stdev2, stdev3)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        count = jdict.get('count')

        minimum = jdict.get('min')
        mean = jdict.get('mean')
        median = jdict.get('median')
        maximum = jdict.get('max')

        variance = jdict.get('var')

        stdev = jdict.get('stdev')
        stdev2 = jdict.get('stdev2')
        stdev3 = jdict.get('stdev3')

        return cls(count, minimum, mean, median, maximum, variance, stdev, stdev2, stdev3)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, count, minimum, mean, median, maximum, variance, stdev, stdev2, stdev3):
        """
        Constructor
        """
        self.__count = count                            # int

        self.__minimum = minimum                        # float
        self.__mean = mean                              # float
        self.__median = median                          # float
        self.__maximum = maximum                        # float

        self.__variance = variance                      # float

        self.__stdev = stdev                            # float
        self.__stdev2 = stdev2                          # float
        self.__stdev3 = stdev3                          # float


    def __len__(self):
        return self.count


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['count'] = self.count

        jdict['min'] = self.minimum
        jdict['mean'] = self.mean
        jdict['median'] = self.median
        jdict['max'] = self.maximum

        jdict['var'] = self.variance

        jdict['stdev'] = self.stdev
        jdict['stdev2'] = self.stdev2
        jdict['stdev3'] = self.stdev3

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def lower1(self):
        return self.median - self.stdev


    def lower2(self):
        return self.median - self.stdev2


    def lower3(self):
        return self.median - self.stdev3


    def upper1(self):
        return self.median + self.stdev


    def upper2(self):
        return self.median + self.stdev2


    def upper3(self):
        return self.median + self.stdev3


    def amp1(self):
        return self.upper1() - self.lower1()


    def amp2(self):
        return self.upper2() - self.lower2()


    def amp3(self):
        return self.upper3() - self.lower3()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def count(self):
        return self.__count


    @property
    def minimum(self):
        return self.__minimum


    @property
    def mean(self):
        return self.__mean


    @property
    def median(self):
        return self.__median


    @property
    def maximum(self):
        return self.__maximum


    @property
    def variance(self):
        return self.__variance


    @property
    def stdev(self):
        return self.__stdev


    @property
    def stdev2(self):
        return self.__stdev2


    @property
    def stdev3(self):
        return self.__stdev3


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Stats:{minimum:%s, mean:%s, median:%s, maximum:%s, variance:%s, stdev:%s, stdev2:%s, stdev3:%s}" %  \
               (self.minimum, self.mean, self.median, self.maximum, self.variance, self.stdev, self.stdev2, self.stdev3)


# --------------------------------------------------------------------------------------------------------------------

class StatsAnalysis(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        minimum = jdict.get('min')
        mean = jdict.get('mean')
        median = jdict.get('median')
        maximum = jdict.get('max')

        lower3 = jdict.get('l3')
        lower2 = jdict.get('l2')
        lower1 = jdict.get('l1')

        upper1 = jdict.get('u1')
        upper2 = jdict.get('u2')
        upper3 = jdict.get('u3')

        amp1 = jdict.get('a1')
        amp2 = jdict.get('a2')
        amp3 = jdict.get('a3')

        return cls(minimum, mean, median, maximum, lower3, lower2, lower1, upper1, upper2, upper3, amp1, amp2, amp3)


    @classmethod
    def construct_from_stats_jdict(cls, jdict):
        stats = Stats.construct_from_jdict(jdict)

        return cls(stats.minimum, stats.mean, stats.median, stats.maximum, stats.lower3(), stats.lower2(),
                   stats.lower1(), stats.upper1(), stats.upper2(), stats.upper3(), stats.amp1(), stats.amp2(),
                   stats.amp3())


    @classmethod
    def construct_from_stats(cls, stats, prec=1):
        return cls(stats.minimum, stats.mean, stats.median, stats.maximum, stats.lower3(), stats.lower2(),
                   stats.lower1(), stats.upper1(), stats.upper2(), stats.upper3(), stats.amp1(), stats.amp2(),
                   stats.amp3(), prec=prec)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, minimum, mean, median, maximum, lower3, lower2, lower1, upper1, upper2, upper3, amp1, amp2, amp3,
                 prec=1):
        """
        Constructor
        """
        self.__minimum = round(float(minimum), prec)
        self.__mean = round(float(mean), prec)
        self.__median = round(float(median), prec)
        self.__maximum = round(float(maximum), prec)

        self.__lower3 = round(float(lower3), prec)
        self.__lower2 = round(float(lower2), prec)
        self.__lower1 = round(float(lower1), prec)

        self.__upper1 = round(float(upper1), prec)
        self.__upper2 = round(float(upper2), prec)
        self.__upper3 = round(float(upper3), prec)

        self.__amp1 = round(float(amp1), prec)
        self.__amp2 = round(float(amp2), prec)
        self.__amp3 = round(float(amp3), prec)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['min'] = self.minimum
        jdict['mean'] = self.mean
        jdict['median'] = self.median
        jdict['max'] = self.maximum

        jdict['l3'] = self.lower3
        jdict['l2'] = self.lower2
        jdict['l1'] = self.lower1

        jdict['u1'] = self.upper1
        jdict['u2'] = self.upper2
        jdict['u3'] = self.upper3

        jdict['a1'] = self.amp1
        jdict['a2'] = self.amp2
        jdict['a3'] = self.amp3

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def minimum(self):
        return self.__minimum


    @property
    def mean(self):
        return self.__mean


    @property
    def median(self):
        return self.__median


    @property
    def maximum(self):
        return self.__maximum


    @property
    def lower3(self):
        return self.__lower3


    @property
    def lower2(self):
        return self.__lower2


    @property
    def lower1(self):
        return self.__lower1


    @property
    def upper1(self):
        return self.__upper1


    @property
    def upper2(self):
        return self.__upper2


    @property
    def upper3(self):
        return self.__upper3


    @property
    def amp1(self):
        return self.__amp1


    @property
    def amp2(self):
        return self.__amp2


    @property
    def amp3(self):
        return self.__amp3


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "StatsAnalysis:{minimum:%s, mean:%s, median:%s, maximum:%s, lower3:%s, lower2:%s, lower1:%s, " \
               "upper1:%s, upper2:%s, upper3:%s, amp1:%s, amp2:%s, amp3:%s}" % \
               (self.minimum, self.mean, self.median, self.maximum, self.lower3, self.lower2, self.lower1,
                self.upper1, self.upper2, self.upper3, self.amp1, self.amp2, self.amp3)
