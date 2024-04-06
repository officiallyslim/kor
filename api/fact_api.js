// This one part of the private api used in the bot.
// This is really simple and require more features/security on deploy like 
const bodyParser = require('body-parser');
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(bodyParser.json({ limit: '10gb' }));

app.use(express.static('public'));
app.get('/', (req, res) => {
    res.send('👋');
});

app.listen(3000, () => console.log('Server running on 3000'));
