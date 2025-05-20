from flask import Flask, request, jsonify
from appFuncs import IPToHash, fullServer, createPlayerID

app = Flask(__name__)

# activeServers = {"exampleServerID":{
#     "IPAddress": "127.0.0.1",
#     "playerIDs": []
# }}
activeServers = {}
serverFull = False

@app.route('/pItHv',methods=["POST"])
def pItHv():
    global activeServers
    data = request.get_json()
    IPAddress = data.get('IPAddress')

    if not IPAddress:
        return jsonify({"error":"IP Address required"}), 400

    try:
        hashedKey = IPToHash(IPAddress)
        activeServers[hashedKey["hashedItem"]] = {}
        activeServers[hashedKey["hashedItem"]]["IPAddress"] = IPAddress
        activeServers[hashedKey["hashedItem"]]["playerIDs"] = []
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
        IPAddress = activeServers[hashedKey]["IPAddress"]
        IPAddressDict = {"IPAddress":IPAddress}
        return jsonify(IPAddressDict), 200

    except Exception as e:
        return jsonify({"error":str(e)}), 500

@app.route('/serverFull', methods=["POST"])
def serverFull():
    global serverFull
    data = request.get_json()
    fullValue = data.get("fullValue")

    if not fullValue:
        return jsonify({"error:fullValue required"}), 400
    else:
        fullValue = int(fullValue)

    try:
        serverFull = fullServer(fullValue)
        confirmMesage = {"msg":"Value Changed Successfully!"}
        return jsonify(confirmMesage), 200

    except Exception as e:
        return jsonify({"error":str(e)}), 500

@app.route('/serverFullCheck', methods=["GET"])
def serverFullCheck():
    global serverFull
    try:
        if serverFull:
            return jsonify({"msg":"Server Full","quickMsg":1}), 200
        else:
            return jsonify({"msg":"Server Not Full","quickMsg":0}), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500

@app.route('/playerID', methods=["POST"])
def playerID():
    global activeServers
    data = request.get_json()
    playerInfo = data.get("playerInfo")

    playerIDs = activeServers[playerInfo["serverKey"]]["playerIDs"]

    if not playerInfo:
        return jsonify({"msg":"playerInfo required"}), 400

    try:
        uniquePlayerID = createPlayerID(playerInfo, playerIDs)
        activeServers[playerInfo["serverKey"]]["playerIDs"].append(uniquePlayerID)
        playerIDMessage = {"msg":"playerID created", "playerID":uniquePlayerID}
        return jsonify(playerIDMessage), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)