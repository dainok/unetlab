// utils/api.js
const API_BASE = "/api"; // Modifica con la base della tua API

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

export const api = {
    async get(endpoint) {
        return this._request("GET", endpoint);
    },

    async post(endpoint, body) {
        return this._request("POST", endpoint, body);
    },

    async put(endpoint, body) {
        return this._request("PUT", endpoint, body);
    },

    async patch(endpoint, body) {
        return this._request("PATCH", endpoint, body);
    },

    async delete(endpoint) {
        return this._request("DELETE", endpoint);
    },

    async _request(method, endpoint, body = null) {
        const options = {
            method,
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRFToken": getCsrfToken(),
            }
        };

        if (body) {
            options.body = JSON.stringify(body);
        }

        try {
            const response = await fetch(API_BASE + endpoint, options);

            if (!response.ok) {
                const errorText = await response.text();
                console.error(`❌ API ${method} ${endpoint} failed: ${response.status} ${response.statusText} - ${errorText}`);
                return null;
            }

            const data = await response.json();
            console.log(`✅ API ${method} ${endpoint} success`, data);
            return data;

        } catch (err) {
            console.error(`❌ API ${method} ${endpoint} error:`, err);
            return null;
        }
    }
};
