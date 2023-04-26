import asyncio
import os
import hashlib
import settings
import json
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.exceptions import PubNubException
from pubnub.pubnub_asyncio import PubNubAsyncio
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from opponent import *
from dotenv import load_dotenv

class Network:
    def __init__(self, game):
        self.game = game

        seed = '%d' % os.stat(os.path.dirname(os.path.realpath(__file__))).st_mtime
        self.user_id = 'Dino-in-Donut-Dungeon-' + str(hashlib.md5(str(seed).encode("utf-8")).hexdigest()[16:])
        if name := os.environ.get('NAME'):
            self.user_id = f'Dino-in-Donut-Dungeon-{name}'

        load_dotenv()
        config = PNConfiguration()
        config.subscribe_key = os.environ.get('PN_SUB_KEY')
        config.publish_key = os.environ.get('PN_PUB_KEY')
        config.user_id = self.user_id
        config.subscribe_request_timeout = 5
        self.metadata = None
        self.channel = 'DinosDonutDungeon'
        self.loop = asyncio.get_event_loop()
        self.pn = PubNub(config)
        self.frame = 1
        self.connect()
        self.last_coords = None

    def connect(self):
        class StatusListener(SubscribeCallback):
            def __init__(self, network):
                self.network = network
                super().__init__()

            def status(self, pubnub, status):
                pass

            def presence(self, pubnub, presence):
                # print(f"Presence: {presence.__dict__}")

                if presence.event == 'leave':
                    self.network.game.opponents.remove(presence.uuid)
                if presence.event == 'join':
                    self.network.last_coords = None

            def message(self, pubnub, message):
                event = message.message
                if event['type'] == 'player_move':
                    if event['id'] != self.network.user_id:
                        self.network.game.opponents.update_opponent(event['id'], (event['pos_x'], event['pos_y']))
                if event['type'] == 'donut_update':
                    self.network.game.place_donut((event['pos_x'], event['pos_x']))


        self.listener = StatusListener(self)

        herenow = self.pn.here_now().channels(self.channel).sync()
        try:
            metadata = self.pn.get_channel_metadata().channel(self.channel).include_custom(True).sync()
            if metadata:
                metadata = metadata.result.data['custom']
        except PubNubException:
            metadata = False

        if herenow.result.channels[0].occupancy > 0 and metadata:
            self.get_map(metadata)
        else:
            self.set_map()

        self.pn.subscribe().channels(self.channel).with_presence().execute()
        self.pn.add_listener(self.listener)


    def disconnect(self):
        self.pn.remove_listener(self.listener)
        self.pn.unsubscribe_all()

    def set_map(self):
        self.metadata = {
            "map": json.dumps(self.game.map.mini_map),
            "donut": json.dumps({"x": self.game.donut.x, "y": self.game.donut.y}),
            "score": json.dumps([])
        }
        self.update_meta()
        print('push map and donut position to channel metadata')

    def get_map(self, metadata):
        # print(f'get_map:{metadata["donut"]}')
        donut = json.loads(metadata['donut'])
        # print(f'get_map.donut {donut}')
        self.game.place_donut((donut['x'], donut['y']))
        self.game.set_map(json.loads(metadata['map']))
        self.metadata = {
            'map': metadata['map'],
            'donut': metadata['donut'],
            'score': metadata['score'] if 'score' in metadata else json.dumps([]),
        }
        # print(self.metadata['donut'])
        print('pull map and donut position from channel metadata')

    def update_meta(self):
        self.pn.set_channel_metadata().channel(self.channel).custom(self.metadata).pn_async(lambda a, b: None)

    def update_donut(self, pos):
        x, y = self.game.donut.pos
        message = {
            'type': 'donut_update',
            'pos_x': x,
            'pos_y': y
        }
        self.metadata['donut'] = json.dumps({"x": x, "y": y})
        def cb(a, b):
            pass

        try:
            self.pn.publish().channel(self.channel).message(message).pn_async(cb)
            self.update_meta()
        except PubNubException as e:
            print(f'except: {e}')

    def update_score(self, pos):

        message = {
            'type': 'score_update'
        }
        def cb(a, b):
            pass

        try:
            self.pn.publish().channel(self.channel).message(message).pn_async(cb)
            self.update_meta()
        except PubNubException as e:
            print(f'except: {e}')


    def update(self):
        if (self.frame % settings.NET_UPDATE_INTERVAL == 0):
            self.frame = 1
            message = {
                'type': 'player_move',
                'id': self.user_id,
                'pos_x': self.game.player.x,
                'pos_y': self.game.player.y,
                # 'angle': self.game.player.angle
                # for now i don't need angle
            }
            if self.last_coords == (self.game.player.x, self.game.player.y, self.game.player.angle):
                # player AFK, don't update
                return None
            self.last_coords = (self.game.player.x, self.game.player.y, self.game.player.angle)

            # kek, callback for non-blocking publish ;D
            def cb(a, b):
                pass

            try:
                self.pn.publish().channel(self.channel).message(message).pn_async(cb)
            except PubNubException as e:
                print(f'except: {e}')

        self.frame += 1