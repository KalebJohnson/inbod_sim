import asyncio
import logging
from fastapi import APIRouter, HTTPException, Response, WebSocket
from fastapi.responses import HTMLResponse
import aiortc

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('yo')
    logging.debug('websocket init')
    await websocket.accept()
    # Create a logging object
    logger = logging.getLogger("aiortc")
    logger.setLevel(logging.DEBUG)
    # Create an RTCPeerConnection
    pc = aiortc.RTCPeerConnection()
    # Set up an event handler for when a new track is added to the RTCPeerConnection
    @pc.on("track")
    async def on_track(track):
        # Process the data from the track
        async for data in track:
            print(f"received data: {data}")
            logging.debug(f"received data: {data}")
            # Do something with the received data
            # ...
    # Set up an event handler for when the RTCPeerConnection's signaling state changes
    @pc.on("signaling_state_change")
    async def on_signaling_state_change(state):
        logger.info(f"signaling state changed: {state}")
        if state == "stable":
            # Send an offer to the client using the WebSocket connection
            offer = await pc.createOffer()
            await websocket.send_text(offer.sdp)
    # Set up an event handler for when a message is received over the WebSocket connection
    async def handle_messages():
        async for message in websocket.receive_text():
            # Process the message as a WebRTC signaling message
            try:
                await pc.setRemoteDescription(aiortc.RTCSessionDescription(sdp=message, type="offer"))
                await pc.addIceCandidate(aiortc.RTCIceCandidate(sdpMLineIndex=0, sdpMid="", candidate=""))
            except Exception as e:
                logger.error(f"Error processing WebRTC signaling message: {e}")
                # Close the WebSocket connection if an error occurs
                await websocket.close(code=1011)
    asyncio.ensure_future(handle_messages())
"""
@router.get("/", response_class=HTMLResponse)
def serve_static_page():
    html = 
    <!DOCTYPE html>
    <html>
      <head>
          <title>WebRTC Test</title>
      </head>
      <body>
          <h1>WebRTC Test</h1>
          <form id="form">
          <button type="submit" id="button">Send</button>
          </form>
      </body>
      <script>
        // Set up the WebSocket connection
        const socket = new WebSocket("");
        // Set up a RTCPeerConnection
        const pc = new RTCPeerConnection({
        iceServers: [{
            urls: "stun:stun.l.google.com:19302"
        }]
        });
        const dataChannel = pc.createDataChannel("test");
        dataChannel.addEventListener("open", () => {
            // The data channel is now open and ready to send data
        });
        // Set up an event handler for when the RTCPeerConnection's signaling state changes
        pc.onicecandidate = event => {
        if (event.candidate) {
            return;
        }
        const sdp = pc.localDescription.sdp;
        socket.send(sdp);
        };
        // Set up an event handler for when the WebSocket connection is opened
        socket.onopen = () => {
            // Create an offer and set it as the local description of the RTCPeerConnection
            pc.createOffer().then(offer => {
                pc.setLocalDescription(offer);
            });
        };
        // Set up an event handler for when a message is received over the WebSocket connection
        socket.onmessage = event => {
        // Process the message as a WebRTC signaling message
            pc.setRemoteDescription(new RTCSessionDescription({
                sdp: event.data,
                type: "answer"
            })).then(() => {
                    // Add an ice candidate to the RTCPeerConnection
                    pc.addIceCandidate(new RTCIceCandidate({
                    sdpMLineIndex: 0,
                    sdpMid: "",
                    candidate: ""
                }));
            });
        };
        const form = document.getElementById("form");
        const button = document.getElementById("button");
        let sending = false;
        form.addEventListener("submit", e => {
            e.preventDefault();
            if (!sending) {
                sending = true;
                button.textContent = "Stop";
                const sendHandler = e => {
                    const x = e.clientX;
                    const y = e.clientY;
                    dataChannel.send(`Mouse position: ${x}, ${y}`);
                };
                window.addEventListener("mousemove", sendHandler);
            } else {
                sending = false;
                button.textContent = "Send";
                window.removeEventListener("mousemove", sendHandler);
            }
        });
      </script>
    </html>

    return HTMLResponse(html)
"""
# ws://localhost/api/v1/rtc_test/ws
print('qwt')
@router.get("/", response_class=HTMLResponse)
def serve_static_page():
    html = """
<html>
  <head>
    <title>WebRTC Test</title>
  </head>
  <body>
    <h1>WebRTC Test</h1>
    <form id="form">
      <input type="text" id="message" value="Hello, World!">
      <input type="button" value="Send" onclick="sendMessage()">
    </form>
    <form id="data-form">
      <input type="text" id="data" value="Some data to send over the WebRTC connection">
      <input type="button" value="Send Data" onclick="sendData()">
    </form>
    <div id="output"></div>
        <script>
            const socket = new WebSocket("ws://localhost/api/v1/rtc_test/ws");

            socket.onopen = () => {
                console.log("WebSocket connection established");
            };

            socket.onmessage = (event) => {
                console.log(`Message received: ${event.data}`);
                const output = document.getElementById("output");
                const newLine = document.createElement("br");
                output.appendChild(document.createTextNode(event.data));
                output.appendChild(newLine);
            };

            socket.onclose = () => {
                console.log("WebSocket connection closed");
            };

            function sendMessage() {
                const message = document.getElementById("message").value;
                socket.send(message);
            }

            const dataChannel = new RTCDataChannel();

            dataChannel.onopen = () => {
                console.log("RTCDataChannel open");
            };

            dataChannel.onmessage = (event) => {
                console.log(`Message received over RTCDataChannel: ${event.data}`);
                const output = document.getElementById("output");
                const newLine = document.createElement("br");
                output.appendChild(document.createTextNode(event.data));
                output.appendChild(newLine);
            };

            dataChannel.onclose = () => {
                console.log("RTCDataChannel closed");
            };

            function sendData() {
                const data = document.getElementById("data").value;
                dataChannel.send(data);
            }
        </script>
  </body>
</html>
    """
    return HTMLResponse(html)
