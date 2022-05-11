const percentage = {
    lines: 99,
    statements: 94,
    functions: 97,
    branches: 97
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