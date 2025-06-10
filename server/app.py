from flask import Flask, request, jsonify
from appFuncs import IPToHash, fullServer, createPlayerID

app = Flask(__name__)

# activeServers = {"exampleServerID":{
#     "IPAddress": "127.0.0.1",
#     "playerIDs": [],
#     "serverPin: 5-digit PIN number
# }}
activeServers = {}
serverFull = False

'''
Name: pItHv
Parameters: None
Returns: string
Purpose: Recieves JSON data, and returns the IP Address, that should've been
given through the JSON data, in the form of a hashed key. Also creates a new place in the activeServers
dictionary with the server information
'''
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
        activeServers[hashedKey["hashedItem"]]["serverPin"] = hashedKey["PIN"]
        return jsonify(hashedKey), 200

    except Exception as e:
        return jsonify({"error":str(e)}), 500

'''
Name: pHtIv
Parameters: None
Returns: string
Purpose: Recieves JSON data, and returns the associated IP Address for that
hash key, assuming it was in the initally given JSON data
'''
@app.route('/pHtIv',methods=["POST"])
def pHtIv():
    global activeServers
    data = request.get_json()
    hashedKey = data.get('hashedKey')
    enteredPin = data.get('pinNo')

    if not hashedKey:
        return jsonify({"error":"hashedKey required"}), 400

    try:
        if activeServers[hashedKey] is None:
            return jsonify({"error": "entered server key doesn't exist!"})
        if activeServers[hashedKey]["IPAddress"] is None:
            return jsonify({"error": "Please DM notharib and tell him that this happened"})
        IPAddress = activeServers[hashedKey]["IPAddress"]
        if activeServers[hashedKey]["serverPin"] != enteredPin:
            return jsonify({"error":"Server Pin is not Correct!"}), 400
        IPAddressDict = {"IPAddress":IPAddress}
        return jsonify(IPAddressDict), 200

    except Exception as e:
        print(e)
        return jsonify({"error":str(e)}), 500

'''
Name: serverFull
Parameters: None
Returns: string
Purpose: Recieves JSON data, and if in the json data it is given a fullValue, 
it changes whether the public server is recognised as full or as not full 
'''
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

'''
Name: serverFullCheck
Parameters: None
Returns: string
Purpose: Recieves JSON data, and checks what the value of the global variable serverFull is,
and depending on what that value is, it tells the initial sender whether the public server is full
'''
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

'''
Name: playerID
Parameters: None
Returns: string
Purpose: Recieves JSON data, and returns a unique playerID, based upon what server the player is joining,
their character build, etc, etc.
'''
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