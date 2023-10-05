const fs = require('fs');

function read(secretName) {
    try {
        return fs.readFileSync(`/run/secrets/${secretName}`, 'utf8').trim();
    }
    catch (err) {
        console.error(err);
        return null;
    }
}

module.exports = { read };
