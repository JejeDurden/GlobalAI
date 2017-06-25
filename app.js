const express = require('express');
const https = require('https');
const exphbs = require('express-handlebars');
const Handlebars = require('handlebars');
const app = express();
const Client = require('node-rest-client').Client;
const client = new Client();
const PORT = process.env.PORT || 8080;

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');
app.use(express.static('public'));

app.get('/', function (req, res) {
	res.render('home');
})

app.get('/result', function (req, res) {
	client.get("http://127.0.0.1:5000/api/get?url_input_page=" + req.query.id, function (data, response) {
		let object = JSON.parse(data);
		console.log(object);
		res.render('result', {json: object, url: req.query.id});
});
})

app.listen(PORT, '0.0.0.0', function () {
	console.log('Running app');
})
