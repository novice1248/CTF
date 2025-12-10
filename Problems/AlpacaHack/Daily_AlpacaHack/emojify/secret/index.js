import express from "express";

const FLAG = process.env.FLAG ?? "Alpaca{REDACTED}";

express()
  // htsecret:1337/flagtp://
  .get("/flag", (req, res) => res.send(FLAG))
  .listen(1337);
