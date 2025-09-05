// js/stores/wsStore.js
document.addEventListener("alpine:init", () => {
    Alpine.store("ws", {
        socket: null,
        url: `ws://${window.location.host}/ws/action/`,
        connected: false,
        reconnectDelay: 2000,
        messages: [],

        connect() {
            if (this.socket && this.connected) return; // Already connected

            this.socket = new WebSocket(this.url);

            this.socket.addEventListener("open", () => {
                console.log("✅ WebSocket connection established.");
                this.connected = true;
            });

            this.socket.addEventListener("close", () => {
                console.warn("⚠️ WebSocket connection closed unexpectedly, reconnecting...");
                this.connected = false;
                setTimeout(() => this.connect(), this.reconnectDelay);
            });

            this.socket.addEventListener("message", (event) => {
                let data;
                try {
                    data = JSON.parse(event.data);
                } catch {
                    console.error("❌ Failed to parse WebSocket message:", err);
                    data = { text: event.data };
                }

                this.messages.push(data);

                // Keep las 100 messages only
                if (this.messages.length > 100) {
                    this.messages.shift();
                }
            });
        },

        disconnect() {
            if (this.socket) {
                this.socket.close();
                this.socket = null;
                this.connected = false;
            }
        },

        send(payload) {
            if (this.connected && this.socket.readyState === WebSocket.OPEN) {
                this.socket.send(JSON.stringify(payload));
            } else {
                console.warn("❌ WebSocket disconnected");
            }
        }
    });
    Alpine.store("ws").connect();
});
