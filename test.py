import argparse
import signal

import zmq

# Define two example requests
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

    # Parse command line arguments; mainly to select either requests above
    # This is only done for convenience during testing
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'request_type', 
        type=int,
        choices=[1, 2], 
        help='The request_type must be 1 or 2'
    )
    args = parser.parse_args()

    # Establish connection to microservice
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://localhost:5555')

    # Send JSON request
    print('Sending a request...')
    socket.send_json(requests[args.request_type])

    # Receive JSON response and print the data
    response = socket.recv_json()
    print('Server sent back:')
    if 'ascii' in response:
        print(response['ascii'])
        print(response['summary'])
    else:
        print(response)
