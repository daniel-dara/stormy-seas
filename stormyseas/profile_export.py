import io
import pstats
from cProfile import Profile


def to_csv(profile: Profile, filename: str, separator: str = ','):
    iostream = io.StringIO()
    pstats.Stats(profile, stream=iostream).strip_dirs().print_stats()

    result = iostream.getvalue()
    result = 'ncalls' + result.split('ncalls')[-1]
    result = '\n'.join([separator.join(line.rstrip().split(None, 5)) for line in result.split('\n')])

    with open(filename, 'w+') as f:
        f.write(result)
        f.close()
