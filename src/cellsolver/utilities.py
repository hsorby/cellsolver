import json
import time


class TimeExecution(object):
    number = 10
    run_timeit = False

    def __init__(self, f):
        self._f = f

    def __call__(self, *args, **kwargs):

        if TimeExecution.run_timeit:
            ts = time.time()
            for _ in range(TimeExecution.number):
                self._f(*args, **kwargs)
            te = time.time()
            print('%r  average = %2.2f ms' %
                  (self._f.__name__, ((te - ts) * 1000) / TimeExecution.number))

        return self._f(*args, **kwargs)


def config_maker():
    d = {'plot_includes': ['sodium_channel_m_gate.m', 'sodium_channel_h_gate.h'], 'plot_excludes': ['intracellular_ions.nai', 'intracellular_ions.nass', 'intracellular_ions.cansr']}
    print(json.dumps(d))


def info_items_list(name_list):
    info_list = []
    for item in name_list:
        split_item = item.split('.')
        info_list.append({'name': split_item[1], 'component': split_item[0]})

    return info_list


def matching_info_items(item, match_items):
    for match_item in match_items:
        if item['name'] == match_item['name'] and item['component'] == match_item['component']:
            return True

    return False


def not_matching_info_items(item, match_items):
    return not matching_info_items(item, match_items)


def load_config(config_file):
    with open(config_file) as f:
        content = f.read()

    return json.loads(content)


def apply_config(config, y_info):
    indices = range(len(y_info))

    if 'parameter_includes' in config and len(config['parameter_includes']):
        info_items = info_items_list(config['parameter_includes'])
        indices = [x for x, z in enumerate(y_info) if matching_info_items(z, info_items)]
    elif 'parameter_excludes' in config and len(config['parameter_excludes']):
        info_items = info_items_list(config['parameter_excludes'])
        indices = [x for x, z in enumerate(y_info) if not_matching_info_items(z, info_items)]

    return indices
