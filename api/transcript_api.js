// Simplified Transcription API Storage
const fs = require('fs');
const path = require('path');
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

const jsonDir = path.join(__dirname, 'json_files');
if (!fs.existsSync(jsonDir)){
    fs.mkdirSync(jsonDir);
}

const transcriptsDB = path.join(__dirname, 'transcripts.json');
if (!fs.existsSync(transcriptsDB)){
    fs.writeFileSync(transcriptsDB, '{}');
}

// Save the transcript for future previews
app.post('/addTranscript', (req, res) => {
    const token = req.headers['authorization'];
    if (token !== 'CHANGE_YOUR_TOKEN_HERE') {
        return res.status(403).send('Wrong token');
    }
    try {
        const { html, ticket_id, ticket_key } = req.body;
        const filePath = path.join(transcriptsDir, `${ticket_id}.html`);
        fs.writeFileSync(filePath, html);
        const db = JSON.parse(fs.readFileSync(transcriptsDB));
        db[ticket_id] = { ticket_key, filePath };
        fs.writeFileSync(transcriptsDB, JSON.stringify(db));
        res.status(201).send('Added transcription correctly');
    } catch (error) {
        console.error('Error writing to the database:', error);
        res.status(500).send('Internal Server Error');
    }
});

// Return web transcript when requested
app.get('/getTranscript/:ticket_id', (req, res) => {
    const { ticket_id } = req.params;
    const db = JSON.parse(fs.readFileSync(transcriptsDB));
    const transcript = db[ticket_id];
    if (transcript && transcript.ticket_key === req.query.ticket_key) {
        const html = fs.readFileSync(transcript.filePath, 'utf8');
        res.send(html);
    } else {
        res.status(404).send('Transcription not found');
    }
});

app.listen(3000, () => console.log('Server running on 3000'));