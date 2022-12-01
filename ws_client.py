import json
from functools import partial

import websocket
import rel


def get_sid():
    with open('output/sid_info.json', 'r') as f:
        sid = json.load(f)["SID"]
    return sid


def on_message(ws, message):
    message = json.loads(message)
    event, data = message[0], message[1]
    if event =="b":
        print('orderbook', data)
    elif event == "q":
        print('quotes', data)        
        

def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws, bonds):
    ws.send(json.dumps(['quotes', bonds[:2]]))
    ws.send(json.dumps(["orderBook", bonds[:2]]))


if __name__ == "__main__":
    
    bonds = ["TRNFP", "TATNP", "AAPL.SPB", "TATN", "SU52001RMFS3", "SU29011RMFS2", "SU26216RMFS0", "SU26215RMFS2", "SU26212RMFS9", "SU26207RMFS9", "SU25077RMFS7"]
    # websocket.enableTrace(True)
    URL = f'wss://wss.tradernet.ru?SID={get_sid()}'
    ws = websocket.WebSocketApp(URL,
                              on_open=partial(on_open, bonds=bonds),
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.run_forever(dispatcher=rel, reconnect=5)  
    rel.signal(2, rel.abort)  
    rel.dispatch()