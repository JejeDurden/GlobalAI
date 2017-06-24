var express = require('express');
var https = require('https');
var exphbs = require('express-handlebars');
var Handlebars = require('handlebars');
var bodyParser = require('body-parser');
var xmlparser = require('express-xml-bodyparser');
var Client = require('node-rest-client').Client;
var fs = require('fs');
var app = express();
var client = new Client();
var options = {
		hostname: 'prodpromise12api.azurewebsites.net',
		path: '/api/job/run',
		cert: fs.readFileSync('Promise12.pem'),
		key: fs.readFileSync('Promise12.pem'),
	};
let Salesforce = require('salesforce_orm');
let username = 'your@salesforce-user.com';
let password = 'yourPassword';
let token = 'yourToken';
let wsdlPath = './SFpprod.wsdl';

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(xmlparser());
app.use(express.static('public'));

Handlebars.registerHelper('if', function(v1, options) {
	if (v1 === "Paired") {
		return options.fn(this);
	}
	return options.inverse(this);
});
Handlebars.registerHelper('ifPlay', function(v1, options) {
	if (v1 === "Ready") {
		return options.fn(this);
	}
	return options.inverse(this);
});


app.get('/', function (req, res) {
	res.render('home');
})

app.get('/user', function (req, res) {
	client.get("http://lvmhmonitoringapi.azurewebsites.net/api/device/track/" + req.query.id, function (data, response) {
		client.get("http://lvmhmonitoringapi.azurewebsites.net/api/device/track/" + req.query.id, function (data1, response1) {
			res.render('result', {salesforce : data, ddb : data1});
		})
	})
})

app.get('/job', function (req, res) {
		https.request(options, function (dat, resp) {
		console.log(dat);
		res.json(dat);
	})
})

app.listen(3000, function () {
	console.log('Running app');
})
