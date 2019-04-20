"""
Peacock Common Module.
"""

import datetime
import gzip
import json
import os

from .logger import Logger


class JsonSerializer(object):
    """Serialize object to or from Json file.

    Attributes:
        _to_compress: whehter compress Json file by gzip,
            True to compress, False not to compress. If compressed
            the _compression_suffix auto appended to filename.
        _compression_suffix: suffix to indicate compress type.
    """

    def __init__(self, compress: bool = False, encoding: str = 'utf-8'):
        self._logger = Logger('jsonserailizer_%s.log' %
                              datetime.datetime.now().strftime('%y%m%d%H%M'),
                              buffer_size=1)
        self._to_compress = compress
        self._compression_suffix = '.gz'   # indecate gzip
        self._encoding = encoding

    def to_file(self, obj, filename: str, no_blocking: bool = False):
        """(API) Serialize obj to json file.

        Args:
            obj: the python obj to be serialized.
            filename: the name of json file contains serialized obj,
                the filename do not contains compression suffix.
            no_blocking: indecate whether or not to not block the
                current execution during serailization.
        """
        if self._to_compress:
            # append compression suffix
            filename += self._compression_suffix

        if no_blocking:
            self._to_file_no_blocking(obj, filename)
        else:
            self._logger.append('serialize object %s to file %s' % (
                                obj.__class__, filename))
            self._save_file(obj, filename)

    def from_file(self, filename: str):
        """(API) Serialize object from file,
        or from compressed file if compression is required.

        Hints:
            filename do not contains compression suffix.
        """
        if self._to_compress:
            # append compression suffix
            filename += self._compression_suffix
            with gzip.open(filename, 'rt', encoding=self._encoding) as fp:
                return json.load(fp)
        else:
            with open(filename, 'r', encoding=self._encoding) as fp:
                return json.load(fp)

    def _to_file_no_blocking(self, obj, filename: str):
        """Serialize obj to json file without blocking execution.

        Serialize obj in seperate process rather than thread,
        as python's thread is not truly concurrent.
        """
        res = os.fork()
        if res != 0:
            os.waitpid(-1, os.WNOHANG)  # reap child process
            return
        else:
            # serialize to file in sub process
            self._logger.append('in [pid %d], serialize object %s to file %s' % (
                                os.getpid(), obj.__class__, filename))
            self._save_file(obj, filename)
            # exit the sub process
            os._exit(0)

    def _save_file(self, obj, filename: str):
        """Save to compressed file if compress is required.
        Otherwise, to normal file.
        """
        if self._to_compress:
            with gzip.open(filename, mode='wt', encoding=self._encoding) as fp:
                json.dump(obj,
                          fp,
                          indent=2,
                          default=self._serialize,
                          sort_keys=False)
        else:
            with open(filename, mode='w', encoding=self._encoding) as fp:
                json.dump(obj,
                          fp,
                          indent=2,
                          default=self._serialize,
                          sort_keys=False)

    def _serialize(self, obj):
        """Serialize json lib unsupported object"""

        if type(obj).__name__ == 'MarketSnapshot':
            return obj.instruments
        if type(obj).__name__ == 'MessageMapContainer':
            return {k: v for k, v in obj.items()}
        if type(obj).__name__ == 'InstrumentSnapshot':
            return {'timestamp': obj.timestamp, 'price': obj.price, 'volume': obj.volume, 'total_bid_volume': obj.total_bid_volume, 'total_ask_volume': obj.total_ask_volume, 'bids': obj.bids, 'asks': obj.asks}
        if type(obj).__name__ == 'RepeatedCompositeContainer':
            return [v for v in obj]
        if type(obj).__name__ == 'QuoteInfo':
            return {'price': obj.price, 'volume': obj.volume}

        # raise error for unexpected obj
        raise TypeError(type(obj).__name__ + ' is not JsonSerializer supported')
