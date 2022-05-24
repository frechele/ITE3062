const lowProblems = require('../database/low_conf_problems.json');
const midProblems = require('../database/mid_conf_problems.json');
const highProblems = require('../database/high_conf_problems.json');
const { wrapWithErrorHander } = require('../util');

async function getProblem(req, res) {
    if (req.query.level == 'low') {
        const index = Math.floor(Math.random() * lowProblems.length);
        res.status(200).json(lowProblems[index]);
    } else if (req.query.level == 'mid') {
        const index = Math.floor(Math.random() * midProblems.length);
        res.status(200).json(midProblems[index]);
    } else if (req.query.level == 'high') {
        const index = Math.floor(Math.random() * highProblems.length);
        res.status(200).json(highProblems[index]);
    } else {
        res.status(400).json({ error: 'invalid problem level '});
    }
}

module.exports = wrapWithErrorHander({
    getProblem
});
