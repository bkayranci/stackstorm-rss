from enum import unique
import feedparser
from datetime import datetime
from time import mktime
import json

from st2reactor.sensor.base import PollingSensor


class RssSensor(PollingSensor):
    def __init__(self, sensor_service, config):
        super(RssSensor, self).__init__(sensor_service=sensor_service,
                                             config=config)
        self._trigger_name = 'new_update'
        self._trigger_pack = 'rss'
        self._trigger_ref = '.'.join([self._trigger_pack, self._trigger_name])
        self.config = config

    def setup(self):
        self._last_entry_id = None

    def poll(self):
        feeds = feedparser.parse(self.config['feed_url'])
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
        self._trigger_pack = 'rss'
        del update['published_parsed']
        del update['updated_parsed']
        del update['created_parsed']
        del update['expired_parsed']
        trigger = '.'.join([self._trigger_pack, self._trigger_name])
        self.sensor_service.dispatch(trigger, dict(json.loads(json.dumps(update))))
