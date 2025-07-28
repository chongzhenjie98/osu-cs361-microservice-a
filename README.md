# Microservice A: Graph Generator

The Microservice A I will implement in Sprint 2 for my teammate will generate a calorie summary graph over a date range (e.g., past 7 days or past 30 days) using the user's food records. Each day's total calorie intake is calculated and visualized, regardless of meal type.

## Requesting data

Use ZeroMQ’s REQ socket to send a JSON payload with the following fields:
- **duration** (`int`): Number of past days to generate the graph, including today
- **json_path** (`str`): Path to JSON file containing the food records
- **output_format** (`Literal['ascii', 'png']`): Specify 'ascii' to return the graph as an ASCII string, or 'png' to save the graph as a PNG file and return its file path
- **png_save_path** (`Optional[str]`): Specify path of PNG file to save to if output_format='png', else defaults to 'graph.png' in current directory

Example call:
```python
import zmq


request = {
    'duration': 30,
    'json_path': 'food_record.json',
    'output_format': 'png',
    'png_save_path': 'test-graph.png'
}

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

```

## Receiving data

Use ZeroMQ's REP socket to listen for incoming connections, receive the JSON payload, process it, and send a JSON response back.

Example call:
```python
import zmq

from generate_graph import generate_graph


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

```

Example JSON response:
```python
# response for ASCII output format
{
  'ascii': '<placeholder_ascii_string>',
  'summary': {
    'average': 29,
    'min': 0,
    'max': 203
  }
}

# response for PNG output format
{
  'png_path': 'test-graph.png',
  'summary': {
    'average': 354,
    'min': 0,
    'max': 742
  }
}

```

## UML sequence diagram
