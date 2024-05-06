/* eslint-disable no-undef */
import express from "express";
import axios from "axios";
import dotenv from "dotenv";
import dayjs from "dayjs";
import fs from "fs";
import path from "path";

import { SEOUL, GYEONGGI } from "./constants.js";

dotenv.config();

const app = express();
const PORT = 3000;
const cwd = process.cwd();
const RTMS_URL = process.env.RTMS_URL;
const ENC_KEY = process.env.ENC_KEY;
// const DEC_KEY = process.env.DEC_KEY;

app.get("/getRtms", async (req, res) => {
  try {
    const MONTH = dayjs().format("YYYYMM");
    console.log(`getRtms Start -> ${MONTH}`);
    const dataDir = path.join(cwd, "data");
    const filePath = path.join(dataDir, `${MONTH}.json`);
    let data = [];

    console.time("start");

    for (const code of [...SEOUL, ...GYEONGGI]) {
      const queryParams = `?serviceKey=${ENC_KEY}&LAWD_CD=${code}&DEAL_YMD=${MONTH}`;
      const res = await axios.get(RTMS_URL + queryParams);

      if (res?.data?.response?.body?.totalCount > 0) {
        const { item } = res.data.response.body.items;
        if (Array.isArray(item)) {
          data = [...data, ...item];
        } else {
          data.push(item);
        }
      }
    }

    fs.writeFile(filePath, JSON.stringify(data), (err) => {
      if (err) {
        console.error("Error writing file:", err);
      } else {
        console.log("File successfully written!");
      }
    });

    console.timeEnd("start");
    console.table(data);

    res.status(200).json(data);
  } catch (error) {
    console.error("Error fetching data:", error);
    res.status(500).json({ error: "Failed to fetch data" });
  }
});

app.get("/", (req, res) => {
  res.send("Hello World!");
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
