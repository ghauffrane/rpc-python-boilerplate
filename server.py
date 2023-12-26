from concurrent import futures
import grpc
import message_pb2
import message_pb2_grpc
import threading

class YourService(message_pb2_grpc.YourServiceServicer):
    def __init__(self):
        self.is_event_running = False

    def CheckStatus(self, request, context):
        return message_pb2.StatusResponse(status="Agent is connected and working")

    def TriggerEvent(self, request, context):
        if not self.is_event_running:
            self.is_event_running = True
            # Simulating event running for 5 seconds
            threading.Timer(5.0, self.finish_event).start()
            return message_pb2.EventResponse(response="Event triggered successfully")
        else:
            return message_pb2.EventResponse(response="Event is already running")

    def finish_event(self):
        self.is_event_running = False

def health_check(server):
    channel = grpc.insecure_channel('localhost:50051')
    stub = message_pb2_grpc.YourServiceStub(channel)
    response = stub.CheckStatus(message_pb2.StatusRequest())
    print("Health Check:", response.status)
    if response.status == "Agent is connected and working":
        response = stub.TriggerEvent(message_pb2.EventRequest())
        print("Event Triggered:", response.response)
    threading.Timer(30.0, health_check, args=[server]).start()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_YourServiceServicer_to_server(YourService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    # Start the health check after 30 seconds initially
    threading.Timer(30.0, health_check, args=[server]).start()

    server.wait_for_termination()

if __name__ == '__main__':
    serve()