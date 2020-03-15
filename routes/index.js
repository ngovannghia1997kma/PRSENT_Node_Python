var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  const { spawn } = require('child_process');
  var process = spawn('python', ['./process.py', req.query.plain]);

  process.stdout.on('data', function(data) {
    // console.log(data.toString());

    res.send(data.toString());
  });

  // http://localhost:3000/?plain=0000000000000000
  // res.render('index', { title: 'Express' });
});

module.exports = router;
