#!/usr/bin/python

def time(func):
    # On Debian Linux, clock() has resolution at best of 0.01 seconds. time()
    # appears to resolve reliably in the microsecond range and certainly in the
    # millisecond time domain that small zlib compression calls invoke. Calling
    # an empty function, this uses up to 4 microseconds on an Athlon XP 2.1GHz,
    # safely orders of magnitude less than even a quick zlib.compress call.

    # On Windows, a different tradeoff exists and one might want to switch from
    # time.time() to time.clock(); per http://docs.python.org/library/time.html
    # the latter achieves microsecond accuracy on that platform. Finally, while
    # clock() various measures wall-clock time or execution time depending upon
    # the operating system, time.time() always measures wall time.

    # See http://mail.python.org/pipermail/python-list/2007-January/1121263.html
    # and http://stackoverflow.com/questions/85451/python-time-clock-vs-time-time-accuracy
    # for more information.
    from time import time
    begin = time()
    func(); func(); ret = func()
    return (time() - begin)/3, ret

# Map input strings to output (compressed) lengths.
def subprocess_invoke(args, stdin):
    # Generic adapter to capture size of stdout. This probably adds some timing
    # overhead, but that's unavoidable (since Python doesn't have libraries for
    # e.g. freearc or xmill)
    from subprocess import Popen, PIPE
    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=None, shell=False, universal_newlines=False)
    output_len = len(process.communicate(stdin)[0])
    process.stdin.close()

    assert process.wait() == 0
    return output_len

def gzip_size(raw, level):
    from zlib import compress
    return len(compress(raw, level))

def bzip2_size(raw, level):
    from bz2 import compress
    return len(compress(raw, level))

def xz_size(raw, level):
    return subprocess_invoke(['xz', '--stdout', '-%d'%level], raw)

def xz_extreme_size(raw, level):
    return subprocess_invoke(['xz', '--stdout', '-%d'%level, '--extreme'], raw)

def freearc_size(pathname, level):
    # Tested using version 0.666 generic Linux binary from website

    # FreeArc appears not to support stdin/out, so this becomes ugly.
    # The RuntimeWarning about tempnam being a security vulnerability is
    # legitimate but irrelevant here.
    from os import tempnam, stat, unlink
    from stat import ST_SIZE
    archive_name = tempnam()+'.arc'
    # Better not have any other 'arc' exectuables earlier in the path...
    subprocess_invoke(['arc', 'a', '-m%s'%level, '-lc', archive_name, pathname], '')
    size = stat(archive_name)[ST_SIZE]
    unlink(archive_name)
    return size

def xmill_zlib_size(raw, level):
    # Tested using version 0.91, compiled with -O2 -fomit-frame-pointer on g++ 4.3.2
    return subprocess_invoke(['xcmill', '-c', '-z', '-%d'%level], raw)

def xmill_bzip2_size(raw):
    # Tested using version 0.91, compiled with -O2 -fomit-frame-pointer on g++ 4.3.2
    return subprocess_invoke(['xcmill', '-c'], raw)

# Unavailable compressors can be elided.
compressors = [('raw', lambda _,__:len(_)), ('status_quo', lambda _,__:bzip2_size(_, 9))]
compressors += [('zlib_%d'%i, (lambda i:(lambda _,__:gzip_size(_, i)))(i))
                for i in xrange(1, 10)]
compressors += [('bzip2_%d'%i, (lambda i:(lambda _,__:bzip2_size(_, i)))(i))
                for i in xrange(1, 10)]
compressors += [('xmill_zlib_%d'%i, (lambda i:(lambda _,__:xmill_zlib_size(_, i)))(i))
                for i in xrange(1,10)]
compressors += [('xmill_bzip2', lambda _,__:xmill_bzip2_size(_))]

# My 1GiB RAM test machine can't use some -8 or -9 settings. They tend to consume
# at least 600-700MiB just for LZ dictionaries, etc; add that to compressed & uncompressed
# memory buffers and it's problematic. Could trade off speed for time at the input
# end and just be more efficient about getting output (no need to store it, really) at
# the other end of the pipeline, but any such compressors aren't actually usable in DC
# regardless. Thus, just disable both -8 and -9. (-8 I thought might be okay, but came
# back and discovered that the test machine had been rendered near-unresponsive by paging).

# The input-end time/space tradeoff that'd be most sensible is some sort of very fast-
# decompressing filetype (most likely LZO or low-compression gzip), since DC's native bzip2
# has near-symmetrical (de)compression times, which would slow the entire test run. Further
# issues include complicating (code, complexity, time, etc) testing any compressor not able
# to directly use piped-in input (FreeARC).

# On the output side, the required change would be to replace subprocess.communicate with
# something that simply read off stdout to prevent blocking on that side while also feeding
# stdin when the filter-compressor needs new data. Python uses threads (see subprocess.py),
# but possible other ways too. Regardless, it doesn't seem worthwhile.

# Finally, one could just remove the very largest (e.g. 270MiB uncompressed) filelists,
# but part of the point is to automate testing across any real filelists that people can
# find, and such large filelists evidently do exist, and it's important to know how they
# behave across different compressors.
compressors += [('xz_%d'%i, (lambda i:(lambda _,__:xz_size(_, i)))(i))
                for i in xrange(1, 9)]
compressors += [('xz_e_%d'%i, (lambda i:(lambda _,__:xz_extreme_size(_, i)))(i))
                for i in xrange(1, 9)]
compressors += [('freearc_%dx'%i, (lambda i:(lambda _,__:freearc_size(__, str(i)+'x')))(i))
                for i in xrange(1, 8)]
compressors += [('freearc_%d'%i, (lambda i:(lambda _,__:freearc_size(__, str(i))))(i))
                for i in xrange(1, 8)]
compressors += [('freearc_%dp'%i, (lambda i:(lambda _,__:freearc_size(__, str(i)+'p')))(i))
                for i in xrange(1, 8)]

# Write as it's being collected, to allow some additional robustness to interruption.
def collect_data(raw_dir):
    from csv import writer
    from os import path, listdir

    for filename in listdir(raw_dir):
        assert filename.endswith('.xml')
        basename = filename[:-4]
        pathname = path.join(raw_dir, filename)

        # One must have enough RAM to hold store the
        # uncompressed filelist and compressed filelist.
        raw = file(pathname, 'rb').read()
        raw_size = len(raw)

        comp_stats_file = [basename]
        # Iterate through compressors, accumulate results
        for comp_name, comp_size_func in compressors:
            comp_time, comp_size = time(lambda:comp_size_func(raw, pathname))
            comp_stats_file += [comp_size, comp_time]
        yield comp_stats_file

def dir_size(raw_dir):
    from os import path, listdir, stat
    from stat import ST_SIZE

    raw_sizes = [stat(path.join(raw_dir, filename))[ST_SIZE]
                 for filename in listdir(raw_dir) if filename.endswith('.xml')]
    return sum(raw_sizes), len(raw_sizes)

def fmt_int_padding(num, denom):
    n_l, d_l = map(lambda _:len(str(_)), [num, denom])
    assert num >= 0 and denom >= 0 and num <= denom and n_l <= d_l
    return '%s%d'%(' '*(d_l - n_l), num)

def fmt_int_ratio(num, denom):
    return '%s/%d'%(fmt_int_padding(num, denom), denom)

def fmt_percent(x):
    return '%5.2f%%'%(x*100)

def write_csv(raw_dir):
    from csv import writer
    from time import time
    from datetime import datetime, timedelta

    f = file('compressed_comparison.csv', 'wb')
    csv_file = writer(f)

    summary_line = ['filelist_name']
    for compressor_name, _ in compressors:
        summary_line += ['%s_size'%compressor_name, '%s_time'%compressor_name]
    csv_file.writerow(summary_line)

    total_raw_size, total_files = dir_size(raw_dir)
    finished_files = 0
    finished_raw_size = 0
    start_time = time()

    for comp_stats_file in collect_data(raw_dir):
        basename = comp_stats_file[0]
        # For this to work, 'raw' must be the first compressor. Could remove that
        # dependency, but *shrug*.
        finished_files += 1
        finished_raw_size += comp_stats_file[1]

        # This is just linear extrapolation. It should work fairly well.
        remaining_raw_size = total_raw_size - finished_raw_size
        est_remaining_time = (time() - start_time)*(float(remaining_raw_size)/finished_raw_size)
        est_completion = datetime.now() + timedelta(0, est_remaining_time)

        fmt = '%s; %s bytes (%s); est. done %s (%s)'
        print fmt%(fmt_int_ratio(finished_files, total_files), fmt_int_padding(finished_raw_size, total_raw_size), fmt_percent(float(finished_raw_size)/total_raw_size), est_completion.strftime('%m-%d %H:%M'), basename.split('.')[0])

        csv_file.writerow(comp_stats_file)

    f.close()

write_csv('raw')
