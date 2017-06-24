const express = require('express');
const https = require('https');
const exphbs = require('express-handlebars');
const Handlebars = require('handlebars');
const app = express();
const api = "http://fd6ba847.ngrok.io/api/get?url_input_page=";
const Client = require('node-rest-client').Client;
const client = new Client();

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');
app.use(express.static('public'));

app.get('/', function (req, res) {
	res.render('home');
})

app.get('/result', function (req, res) {
	client.get("http://fd6ba847.ngrok.io/api/get?url_input_page=" + req.query.id, function (data, response) {
		let object = JSON.parse(data);
		console.log(object);
		res.render('result', {json: object});
});
})

app.listen(3000, function () {
	console.log('Running app');
})
