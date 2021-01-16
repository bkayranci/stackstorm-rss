import feedparser
from st2reactor.sensor.base import PollingSensor


class RssSensor(PollingSensor):

    def setup(self):
        self._last_entry_id = None

    def poll(self):
        feeds = feedparser.parse(self._config['feed_url'])
        entries = feeds.entries
        if len(entries) > 0 and self._last_entry_id != entries[0]:
            for entry in entries:
                if (self._last_entry_id == entries[0]):
                    break
                self._dispatch_trigger(entry)
            self._last_entry_id != entries[0].id


    def update_trigger(self):
        pass

    def add_trigger(self, trigger):
        pass

    def cleanup(self):
        pass

    def remove_trigger(self):
        pass

    def _dispatch_trigger(self, update):
        
        self._trigger_name = 'new_update'
        self._trigger_pack = 'rss_service'
        self._trigger_ref = '.'.join([self._trigger_pack, self._trigger_name])

        self._sensor_service.dispatch(self._trigger_ref, dict(update))
