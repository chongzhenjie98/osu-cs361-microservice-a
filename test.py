import argparse
import signal

import zmq


request_1 = {
    'duration': 7,
    'json_path': 'food_record.json',
    'output_format': 'ascii'
}
request_2 = {
    'duration': 30,
    'json_path': 'food_record.json',
    'output_format': 'png',
    'png_save_path': 'test-graph.png'
}
requests = {1: request_1, 2: request_2}

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'request_type', 
        type=int,
        choices=[1, 2], 
        help='The request_type must be 1 or 2'
    )
    args = parser.parse_args()

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://localhost:5555')

    print('Sending a request...')
    socket.send_json(requests[args.request_type])

    response = socket.recv_json()
    print('Server sent back:')
    if 'ascii' in response:
        print(response['ascii'])
        print(response['summary'])
    else:
        print(response)
