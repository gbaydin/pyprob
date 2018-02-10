from . import util


class Sample(object):
    def __init__(self, address, distribution, value):
        self.address = address
        self.distribution = distribution
        if distribution is None:
            self.address_suffixed = address
        else:
            self.address_suffixed = address + distribution.address_suffix
        self.value = util.to_variable(value)

    def __repr__(self):
        return 'Sample(address_suffixed:{}, distribution:{}, value:{})'.format(
            self.address_suffixed,
            str(self.distribution),
            self.value.data.cpu().numpy().tolist()
        )


class Trace(object):
    def __init__(self):
        self.observes = []
        self.observes_variable = None
        self.observes_embedding = None
        self.samples = []
        self.length = 0
        self.result = None
        self.log_prob = 0

    def __repr__(self):
        return 'Trace(length:{}, samples:[{}], observes_variable:{}, result:{}, log_prob:{})'.format(
            self.length,
            ', '.join([str(sample) for sample in self.samples]),
            self.observes_variable.data.cpu().numpy().tolist(),
            self.result.data.cpu().numpy().tolist(),
            float(self.log_prob)
        )

    def addresses(self):
        return '; '.join([sample.address for sample in self.samples])

    def addresses_suffixed(self):
        return '; '.join([sample.address_suffixed for sample in self.samples])

    def add_log_prob(self, p):
        self.log_prob += p

    def set_result(self, r):
        self.result = r

    def add_sample(self, s):
        self.samples.append(s)
        self.length += 1

    def add_observe(self, o):
        self.observes.append(o)

    def pack_observes_to_variable(self):
        self.observes_variable = util.pack_observes_to_variable(self.observes)
