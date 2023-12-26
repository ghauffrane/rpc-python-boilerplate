import grpc
import message_pb2
import message_pb2_grpc

def send_status():
    channel = grpc.insecure_channel('localhost:50051')
    stub = message_pb2_grpc.YourServiceStub(channel)
    response = stub.CheckStatus(message_pb2.StatusRequest())
    print("Status:", response.status)

def send_event():
    channel = grpc.insecure_channel('localhost:50051')
    stub = message_pb2_grpc.YourServiceStub(channel)
    response = stub.TriggerEvent(message_pb2.EventRequest())
    print("Response:", response.response)

if __name__ == '__main__':
    send_status()  # To check agent status
    send_event()   # To trigger an event
