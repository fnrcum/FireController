import logging

from gevent.pool import Pool
from valve.source.master_server import MasterServerQuerier
from valve.source.a2s import ServerQuerier, NoResponseError
from valve.source.messages import BrokenMessageError

MASTER_HOST = 'hl2master.steampowered.com'
MASTER_TIMEOUT = 60
SERVER_TIMEOUT = 5
pool = Pool(size=3)


def get_server_stats(address):
    server = ServerQuerier(address, timeout=SERVER_TIMEOUT)
    try:
        info = server.info()
        # rules = server.rules()
        logging.info(u'Updated {0}:{1} █ {player_count}/{max_players} players █ {server_name} █ {map} █ {server_type}'.format(
            address[0], address[1], **info)
        )
        # logging.info(u'Rules {rules} \n'.format(**rules))
        return True
    except (NotImplementedError, NoResponseError, BrokenMessageError):
        pass


def find_servers():
    count = 0
    max = 1
    _results = []
    master = MasterServerQuerier(
        address=(MASTER_HOST, 27011), timeout=MASTER_TIMEOUT
    )
    try:
        for address in master.find(region='rest',
                                   gamedir=u"ark_survival_evolved"):
            if str(address[0]) == "86.126.75.154":
                _results.append(pool.spawn(get_server_stats, address))
                count += 1
            if count == max:
                break
    except NoResponseError as e:
        # Protocol is UDP so there's no "end"
        if u'Timed out' not in e.message:
            logging.warning('Error querying master server: {0}'.format(e))
    finally:
        logging.info('Found {0} addresses'.format(count))
        return _results


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    results = find_servers()
    logging.info('Counting results...')
    results = [result.get() for result in results]
    # successes = filter(None, results)
    logging.info('Collected {0}'.format(len(results)))