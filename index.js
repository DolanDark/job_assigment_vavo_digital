const express = require('express')
const {spawn} = require('child_process');
const app = express()
const port = 3000
const cron = require('node-cron')


// use cron expression('0 0 * * *') to run scheduler once a day, currently set to once every minute to test
cron.schedule('* * * * *', function() {
    const response = fetch('http://localhost:3000/runscript');
    const body = response.json();
    console.log('running a task every minute');
  });

// A request to route /runscript executes the python file
app.get('/runscript', (req, res) => {
 
 var dataToSend;
 const python = spawn('python', ['scrape_data.py']);
 python.stdout.on('data', function (data) {
  console.log('Pipe data from python script ...');
  dataToSend = data.toString();
 });
 python.on('close', (code) => {
 console.log(`child process close all stdio with code ${code}`);
 res.send(dataToSend)
 console.log("pipedata >>", dataToSend)
 });
 
})


app.listen(port, () => console.log(`Node app listening on port 
${port}!`))