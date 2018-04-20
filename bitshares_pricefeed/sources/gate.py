import requests
from . import FeedSource, _request_headers

class Gate(FeedSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _fetch(self):
        feed = {}
        url = "https://data.gate.io/api2/1/ticker/{quote}_{base}"
        try:
            for base in self.bases:
                feed[base] = {}
                if hasattr(self, "baseAlias") and base in self.baseAlias:
                    basefetch=self.baseAlias[base]
                else:
                    basefetch=base
                for quote in self.quotes:
                    if base == quote:
                        continue

                    response = requests.get(url=url.format(
                        quote=quote.lower(),
                        base=basefetch.lower()
                    ), headers=_request_headers, timeout=self.timeout)
                    result = response.json()
                    if hasattr(self, "quoteNames") and quote in self.quoteNames:
                            quote = self.quoteNames[quote]
                    feed[base][quote] = {"price": (float(result["last"])), "volume": (float(result["quoteVolume"])* self.scaleVolumeBy)}

        except Exception as e:
            raise Exception("\nError fetching results from {1}! ({0})".format(str(e), type(self).__name__))
        return feed
