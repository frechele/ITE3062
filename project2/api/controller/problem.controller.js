const problems = require('../database/problems.json');
const { wrapWithErrorHander } = require('../util');

async function getProblem(req, res) {
    const index = Math.floor(Math.random() * problems.length);
    res.status(200).json(problems[index]);
}

module.exports = wrapWithErrorHander({
    getProblem
});
