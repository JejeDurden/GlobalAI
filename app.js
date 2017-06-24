const express = require('express');
const https = require('https');
const exphbs = require('express-handlebars');
const Handlebars = require('handlebars');
const app = express();


app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static('public'));

app.get('/', function (req, res) {
	res.render('home');
})

app.get('/result', function (req, res) {
	res.render('home');
})

app.listen(3000, function () {
	console.log('Running app');
})
