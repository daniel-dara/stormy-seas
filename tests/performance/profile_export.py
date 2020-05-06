import io
import pstats
from cProfile import Profile


def csv(profile: Profile, path: str, separator: str = ','):
    string_io = io.StringIO()
    pstats.Stats(profile, stream=string_io).strip_dirs().print_stats()

    result = string_io.getvalue()
    result = 'ncalls' + result.split('ncalls')[-1]
    result = '\n'.join([separator.join(line.rstrip().split(None, 5)) for line in result.split('\n')])

    with open(path, 'w+') as f:
        f.write(result)
        f.close()
