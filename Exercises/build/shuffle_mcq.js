// Chuyen quiz_data.js / theory_quiz_data.js thanh MCQ chuan, xao dap an bang seed co dinh,
// kiem tra chi-square truoc khi ghi ra file.
const fs = require("fs");

function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function shuffleWithRng(arr, rng) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
function chiSquare(counts) {
  const n = counts.reduce((a, b) => a + b, 0);
  const expected = n / counts.length;
  return counts.reduce((s, c) => s + Math.pow(c - expected, 2) / expected, 0);
}

function loadArray(path, exportName) {
  let src = fs.readFileSync(path, "utf-8");
  src = src.replace(exportName, "module.exports =");
  const tmp = "/tmp/_load_" + Date.now() + Math.random() + ".js";
  fs.writeFileSync(tmp, src);
  const data = require(tmp);
  fs.unlinkSync(tmp);
  return data;
}

function convertBank(rawQuestions, idPrefix, groupField) {
  // Thu nhieu seed, chon seed co tong chi-square tot nhat tren toan bo bank
  let bestSeed = null, bestScore = Infinity, bestResult = null;
  for (let seed = 1; seed <= 200; seed++) {
    const rng = mulberry32(seed);
    const posCount = [0, 0, 0, 0];
    const result = rawQuestions.map((q, i) => {
      const correctText = q.answer.trim();
      const optsWithFlag = q.options.map(o => ({ text: o, correct: o.trim() === correctText }));
      const shuffled = shuffleWithRng(optsWithFlag, rng);
      const correctIndex = shuffled.findIndex(o => o.correct);
      posCount[correctIndex]++;
      return {
        id: `${idPrefix}${String(i + 1).padStart(3, "0")}`,
        group: q[groupField],
        question: q.question,
        options: shuffled.map(o => o.text),
        correctIndex,
      };
    });
    const score = chiSquare(posCount);
    if (score < bestScore) { bestScore = score; bestSeed = seed; bestResult = { result, posCount }; }
  }
  console.log(`${idPrefix}: seed tot nhat = ${bestSeed}, phan bo vi tri dap an = ${JSON.stringify(bestResult.posCount)}, chi-square = ${bestScore.toFixed(3)} (nguong canh bao p<0.05 voi 3 bac tu do ~ 7.815)`);
  return bestResult.result;
}

const rawSql = loadArray("/Users/tuannghiat/Downloads/Phenikaa - Cơ sở dữ liệu/quiz_data.js", "const allQuestions =");
const rawTheory = loadArray("/Users/tuannghiat/Downloads/Phenikaa - Cơ sở dữ liệu/theory_quiz_data.js", "const theoryQuizQuestions =");

const sqlMcq = convertBank(rawSql, "mcqsql", "lab");
const theoryMcq = convertBank(rawTheory, "mcqth", "chapter");

fs.writeFileSync(
  "/Users/tuannghiat/Downloads/for-Vinh-Exercises/data/mcq_sql.json",
  JSON.stringify(sqlMcq, null, 2)
);
fs.writeFileSync(
  "/Users/tuannghiat/Downloads/for-Vinh-Exercises/data/mcq_theory.json",
  JSON.stringify(theoryMcq, null, 2)
);
console.log("SQL MCQ:", sqlMcq.length, "cau. Theory MCQ:", theoryMcq.length, "cau.");
