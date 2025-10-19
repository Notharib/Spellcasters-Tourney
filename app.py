from flask import Flask, request, jsonify

from logger import addToLog, generateLogFile

app = Flask(__name__)


serverFullValue = False
pubLeader = {}

for i in range(1,11):
    pubLeader[str(i)] = None


'''
Name: serverFull
Parameters: None
Returns: string
Purpose: Recieves JSON data, and if in the json data it is given a fullValue, 
it changes whether the public server is recognised as full or as not full 
'''
@app.route('/serverFull', methods=["POST"])
def serverFull():
    global serverFull, logPath
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
        addToLog(logPath, "serverFull", e)
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
    global serverFullValue, logPath

    try:
        if serverFullValue:
            return jsonify({"msg":"Server Full","quickMsg":1}), 200
        else:
            return jsonify({"msg":"Server Not Full","quickMsg":0}), 200
    except Exception as e:
        addToLog(logPath, "serverfullcheck", e)
        return jsonify({"error":str(e)}), 500

'''
Name: publicLeaderCheck
Parameters: None
Returns: string
Purpose: Recieves the request, and returns the dictionary information for the
public server
'''
@app.route('/publicLeaderCheck',methods=['GET'])
def publicLeaderCheck():
    global pubLeader, logPath

    try:
        return jsonify({"msg":"leaderboard", "data":pubLeader}), 200
    except Exception as e:
        addToLog(logPath, "publeadcheck", e)
        return jsonify({"error":str(e)}), 500

'''
Name: publicServerUpd
Parameters: None
Returns: string
Purpose: Recieves JSON data, and then updates the amount of deaths stored for that player
'''
@app.route('/publicLeaderUpd',methods=['POST'])
def publicLeaderUpd():
    global pubLeader, logPath

    data = request.get_json()
    playerID = data.get("playerID")
    
    if not playerID:
        return jsonify({"msg":"Missing PlayerID"}), 400
    
    playerID = str(playerID)
    print(pubLeader[playerID])
    
    try:
        if pubLeader[playerID] is None:
            pubLeader[playerID] = 0
            return jsonify({"msg":"leaderboard updated"}), 200
        else:
            pubLeader[playerID] += 1
            return jsonify({"msg":"leaderboard updated"}), 200
    except Exception as e:
        print("Error",e)
        addToLog(logPath, "publeadupd", e)
        return jsonify({"error":str(e)}), 500

'''
Name: removePlayer
Parameters: None
Returns: string
Purpose: Recieves JSON data, and if in the json data it is given,
it converts the position in the leaderboard to None
'''
@app.route('/removePlayer', methods=['POST'])
def removePlayer():
    global pubLeader, logPath

    data = request.get_json()
    playerID = data.get("playerID")

    if not playerID:
        return jsonify({"error":"playerID required"}), 400

    try:
        pubLeader[playerID] = None
        return jsonify({"msg":"player removed successfully"}), 200
    except Exception as e:
        addToLog(logPath, "removePlayer", e)
        return jsonify({"error":str(e)}), 500

if __name__ == '__main__':
    logPath: str = generateLogFile("API")
    
    app.run(debug=True)
