# Simple Blockchain

Implementation of a simple blockchain in python made as the final project of the Distributed Systems course in the Faculty of Engineering, Alexandria University.

## Usage

1. Clone repo and `cd` into the project directory
2. Install requirements
   ```
   pip install -r requirements.txt
   ```
4. To compile proto files run the following command:
   ```
   $ python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/blockchain.proto
   ```
5. Run `main.py` with flag `-h` for info on available commands and flags:
   ```
   $ python main.py -h
   ```
6. Configure peers file to include addresses of potential peers
7. Run client-server
 
Example for running a miner and client with a proof of work consensus:
   ```
   $ python main.py miner -p 9980 -c pow
   $ python main.py client -p 9980 -c pow
   ```
