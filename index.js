const express = require("express");
const path = require("path");

const app = express();
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(express.static(path.join(__dirname, "public")));
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
    res.render("main");
});

// GET quiz (because you navigate using link)
app.get("/quiz", (req, res) => {
    const category = req.query.cat;
    const difficulty = req.query.level;
    res.render("quiz", { category, difficulty });
});

// POST if submitting by form
app.post("/start-quiz", (req, res) => {
    const { category, difficulty } = req.body;
    res.render("quiz", { category, difficulty });
});

// result page
app.get("/result", (req, res) => {
    const score = req.query.score || 0; // fallback if empty
    res.render("result", { score });
});


app.listen(9000, () => console.log("Quiz app running on port 9000"));
