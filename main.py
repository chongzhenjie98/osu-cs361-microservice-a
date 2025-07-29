import signal

import zmq

from generate_graph import generate_graph


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Bind socket to listen for connections
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5555')
    print('Listening on port 5555...')

    while True:
        # Receive JSON request
        data = socket.recv_json()
        print('Received:')
        print(data)
        
        # Process data from JSON request
        try:
            output = generate_graph(**data)
        except Exception as e:
            output = {'error': str(e)}

        # Send back JSON response
        socket.send_json(output)
