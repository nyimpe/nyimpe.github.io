import Box from "@mui/material/Box";
import { DataGrid } from "@mui/x-data-grid";
import { nanoid } from "@reduxjs/toolkit";

import data from "../../data.json";
import { LAWD_CD } from "../common/code";

const rows = data.map((e) => {
  return { ...e, id: nanoid() };
});

const desiredOrder = [
  "건축년도",
  "전용면적",
  "아파트",
  "층",
  "거래금액",
  "지번",
  "등기일자",
];
const columns = Object.keys(data[0])
  .filter(
    (e) =>
      ![
        "월",
        "일",
        "동",
        "해제사유발생일",
        "해제여부",
        "거래유형",
        "매도자",
        "매수자",
        "중개사소재지",
        "지역코드",
      ].includes(e)
  )
  .sort((a, b) => {
    const indexA = desiredOrder.indexOf(a);
    const indexB = desiredOrder.indexOf(b);

    if (indexA === -1 && indexB === -1) return 0;
    if (indexA === -1) return 1;
    if (indexB === -1) return -1;
    return indexA - indexB;
  })
  .map((e) => {
    return { field: e, headerName: e };
  });

const RealEstate = () => {
  const customCol = [
    {
      field: "date",
      headerName: "날짜",
      valueGetter: (param, row) => {
        return row["월"] + "/" + row["일"];
      },
    },
    {
      field: "town",
      headerName: "지역",
      valueGetter: (param, row) => {
        const townName = LAWD_CD.find((e) =>
          e.code.startsWith(row["지역코드"])
        );
        return townName.name;
      },
    },
  ];
  return (
    <Box>
      <DataGrid rows={rows} columns={[...customCol, ...columns]} autoHeight />
    </Box>
  );
};

export default RealEstate;
