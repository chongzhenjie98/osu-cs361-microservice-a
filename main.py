import signal

import zmq

from generate_graph import generate_graph


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    port_num = 5555
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f'tcp://*:{port_num}')
    print(f'Listening on port {port_num}...')

    while True:
        data = socket.recv_json()
        print('Received:')
        print(data)
        
        try:
            output = generate_graph(**data)
        except Exception as e:
            output = {'error': str(e)}

        socket.send_json(output)
