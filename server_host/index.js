const dotenv = require("dotenv")
const { read } = require('./secret_reader');
const Consumer = require('./task_consumer');

dotenv.config();
const queueName = read('server_host_name') || process.env.SERVER_HOST_NAME || 'server-host';

const consumer = new Consumer(queueName);

process.on('exit', () => {
  console.log("Exiting...")
  consumer.close();
});

process.on('SIGINT', () => {
  console.log("Ctrl+C...")
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log("SIGTERM...")
  process.exit(0);
});

consumer.startConsumer();
