const percentage = {
    lines: 55,
    statements: 54,
    functions: 62,
    branches: 40
}
var summary = require('./karma/coverage/coverage-summary.json');

for (let res in summary.total) {
    if (summary.total[res].pct < percentage[res]) {
        throw new Error(
        `Coverage too low on ${res},
        expected: ${percentage[res]},
        got: ${summary.total[res].pct}`
        );
    }
}