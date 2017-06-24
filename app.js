const express = require('express');
const https = require('https');
const exphbs = require('express-handlebars');
const Handlebars = require('handlebars');
const PythonShell = require('python-shell');
const pyshell = new PythonShell('./scrapper/img_scrapper.py');
const app = express();

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');
app.use(express.static('public'));

app.get('/', function (req, res) {
	res.render('home');
})

app.get('/result', function (req, res) {

	pyshell.send(req.query.id);
	console.log(req.query.id);
	pyshell.on('message', function (message) {
  	// received a message sent from the Python script (a simple "print" statement)
  	console.log(message);
	});
	pyshell.end(function (err) {
  	if (err) throw err;
  	console.log('finished');
	});
	res.render('result');
});

app.listen(3000, function () {
	console.log('Running app');
})
