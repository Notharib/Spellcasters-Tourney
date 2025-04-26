from flask import Flask, request, jsonify
from appFuncs import IPToHash

app = Flask(__name__)

activeServers = {}

@app.route('/pItHv',methods=["POST"])
def pItHv():
    global activeServers
    data = request.get_json()
    IPAddress = data.get('IPAddress')

    if not IPAddress:
        return jsonify({"error":"IP Address required"}), 400

    try:
        hashedKey = IPToHash(IPAddress)
        activeServers[hashedKey["hashedItem"]] = IPAddress
        return jsonify(hashedKey), 200

    except Exception as e:
        return jsonify({"error":str(e)}), 500

@app.route('/pHtIv',methods=["POST"])
def pHtIv():
    global activeServers
    data = request.get_json()
    hashedKey = data.get('hashedKey')

    if not hashedKey:
        return jsonify({"error":"hashedKey required"}), 400

    try:
        IPAddress = activeServers[hashedKey]
        IPAddressDict = {"IPAddress":IPAddress}
        return jsonify(IPAddressDict), 200

    except Exception as e:
        return jsonify({"error":str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)