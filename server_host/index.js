const dotenv = require("dotenv")

dotenv.config();

const Consumer = require('./task_consumer');

const queueName = process.env.SERVER_HOST_NAME || 'server-host';

const consumer = new Consumer(queueName);

process.on('exit', () => {
  console.log("Exiting...")
  consumer.close();
});

process.on('SIGINT', () => {
  console.log("Ctrl+C...")
  process.exit(2);
});

consumer.startConsumer();
