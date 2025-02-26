from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Get channel data from GitHub
JSON_URL = "https://raw.githubusercontent.com/Jeshan-akand/Toffee-Channels-Link-Headers/main/toffee_channel_data.json"

@app.route('/getStream', methods=['GET'])
def get_stream():
    # Fetch the channel data from the JSON URL
    try:
        response = requests.get(JSON_URL)
        data = response.json()

        # Extract channel list
        channels_data = data.get("channels", [])

        if not channels_data:
            return jsonify({"error": "No channels found."}), 404
        
        # Get channel index from query param, default to 0 if not provided
        channel_index = int(request.args.get('channel', 0))

        # Ensure the channel index is within valid range
        if channel_index < 0 or channel_index >= len(channels_data):
            return jsonify({"error": "Invalid channel index."}), 400
        
        # Get selected channel data
        selected_channel = channels_data[channel_index]
        link = selected_channel.get("link")
        headers = selected_channel.get("headers")

        # If link or headers are missing, return an error
        if not link or not headers:
            return jsonify({"error": "Stream URL or headers missing for the selected channel."}), 400
        
        # Request to Toffee API to get the live stream URL
        request_server = requests.get(link, headers=headers)
        
        return jsonify({
            "streamUrl": request_server.text,
            "channelLink": link,
            "headers": headers
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
