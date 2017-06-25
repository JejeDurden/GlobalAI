const express = require('express');
const https = require('https');
const exphbs = require('express-handlebars');
const Handlebars = require('handlebars');
const app = express();
const Client = require('node-rest-client').Client;
const client = new Client();

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');
app.use(express.static('public'));

app.get('/', function (req, res) {
	res.render('home');
})

app.get('/result', function (req, res) {
	client.get("http://08c3c559.ngrok.io/api/get?url_input_page=" + req.query.id, function (data, response) {
		let object = JSON.parse(data);
		console.log(object);
		res.render('result', {json: object, url: req.query.id});
});
})

app.listen(3000, function () {
	console.log('Running app');
})
