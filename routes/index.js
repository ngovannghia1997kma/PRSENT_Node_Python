var express = require('express');
var router = express.Router();

router.get('/encrypt', function (req, res, next) {
  const { spawn } = require('child_process');
  console.log(req.query);

  var process = spawn('python', [
    './encrypt.py',
    req.query.plain,
    req.query.key,
  ]);
  process.stdout.on('data', function (data) {
    data = JSON.parse(data.toString());
    res.render('encrypted', { result: data.cipher, sboxs: data.sboxs });
  });
});

router.get('/decrypt', function (req, res, next) {
  const { spawn } = require('child_process');
  var process = spawn('python', [
    './decrypt.py',
    req.query.cipher,
    req.query.key,
  ]);
  process.stdout.on('data', function (data) {
    data = JSON.parse(data.toString());
    res.render('decrypted', { result: data.decipher, sboxs: data.sboxs });
  });
});

/* GET encrypt page. */
router.get('/', function (req, res, next) {
  res.render('encrypt');
});

/* GET decrypt page. */
router.get('/decrypt-page', function (req, res, next) {
  res.render('decrypt');
});

module.exports = router;
