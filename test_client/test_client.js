function logMessage(msg) {
    const responseBox = document.getElementById("response");
    const timestamp = new Date().toLocaleString();
    const newMessage = `${timestamp}: ${msg}\n${responseBox.value}`;
    responseBox.value = newMessage;
}

function displayInElement(id, msg) {
    document.getElementById(id).value = msg;
    document.getElementById(id).innerHTML = msg;
}

function createRequestAndLog(type, url) {
    const xhr = new XMLHttpRequest();
    xhr.open(type, url);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onload = function () {
        if (xhr.status === 200) {
            logMessage(xhr.responseText);
        } else {
            logMessage(`Error: ${xhr.statusText}`);
        }
    };
    xhr.onerror = function () {
        logMessage("Error: Connection to server failed.");
    };
    return xhr;
}

function createRequestAndDisplayInElement(type, url, id, ...responseKeys) {
    const xhr = new XMLHttpRequest();
    xhr.open(type, url);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onload = function () {
        if (xhr.status === 200) {
            display = responseKeys.reduce((acc, key) => acc[key], JSON.parse(xhr.responseText));
            displayInElement(id, JSON.stringify(display));
        } else {
            logMessage(id, `Error: ${xhr.statusText}`);
        }
    }
    xhr.onerror = function () {
        logMessage("Error: Connection to server failed.");
    }
    return xhr;
}

// ==================== User functionality ====================

function registerUser() {
    const id = JSON.parse(document.getElementById("user VC").value);
    const data = { "credential": id };

    const xhr = createRequestAndLog("POST", `http://localhost:8000/user/register_user`);
    xhr.send(JSON.stringify(data));
}

function deregisterUser() {
    const xhr = createRequestAndLog("GET", `http://localhost:8000/user/deregister_user`);
    xhr.send();
}

function getHost() {
    const xhr = createRequestAndDisplayInElement("GET", `http://localhost:8000/user/get_host`, "ip_address", "ip_address");
    xhr.send();
}

function upload() {
    const id = document.getElementById("id").value;
    const fileInput = document.getElementById("file");
    const file = fileInput.files[0];
    const ip_address = JSON.parse(document.getElementById("ip_address").value);

    if (!file) {
        logMessage("Error: No file selected.");
        return;
    }

    const reader = new FileReader();
    reader.readAsBinaryString(file);
    reader.onload = function () {
        const binary = btoa(reader.result);
        const data = { id, binary };

        const xhr = createRequestAndLog("POST", `http://${ip_address}:8000/host/compute`);
        xhr.send(JSON.stringify(data));
    };
}

function getResult() {
    const id = document.getElementById("id").value;
    const ip_address = JSON.parse(document.getElementById("ip_address").value);
    const data = { id };

    const xhr = createRequestAndLog("POST", `http://${ip_address}:8000/host/get_result`);
    xhr.send(JSON.stringify(data));
}

// ==================== Host functionality ====================

function registerHost() {
    const id = JSON.parse(document.getElementById("host VC").value);
    const data = { "credential": id };

    const xhr = createRequestAndLog("POST", `http://localhost:8000/host/register_host`);
    xhr.send(JSON.stringify(data));
}

function deregisterHost() {
    const xhr = createRequestAndLog("GET", `http://localhost:8000/host/deregister_host`);
    xhr.send();
}

function createDID(type) {
    const id = document.getElementById(type + " public key").value;
    const data = { "publicKey": id };

    const xhr = createRequestAndDisplayInElement("POST", `http://localhost:8080/api/v1/did/create`, type + " DID", "result", "did");
    xhr.send(JSON.stringify(data));
}

function createVC(type) {
    const id = document.getElementById(type + " DID").value;
    const data = {
        "claimData": {
            "DID": id,
            "name": "Chai",
            "gender": "M",
            "age": 29
        },
        "cptId": 2000000,
        "issuer": "did:bdsv:0x52c328ef8b382b1d71cc262b868d803a137ab8d8"
    };

    const xhr = createRequestAndDisplayInElement("POST", `http://localhost:8080/api/v1/credential/create`, type + " VC", "result");
    xhr.send(JSON.stringify(data));
}