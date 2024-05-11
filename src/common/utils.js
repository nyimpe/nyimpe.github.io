import _ from "lodash";
import { LAWD_CD } from "./code";
import { nanoid } from "@reduxjs/toolkit";
import dayjs from "dayjs";

export const isEmptyValue = (value) => {
  return _.isEmpty(value);
};

export const getRowData = (data) => {
  return data.map((item) => ({
    ...item,
    id: nanoid(),
    날짜: dayjs(item["년"] + "/" + item["월"] + "/" + item["일"]).format(
      "YYYY-MM-DD"
    ),
    지역: LAWD_CD.find(({ code }) => code.startsWith(item[["지역코드"]])).name,
    거래금액: (
      parseInt(item["거래금액"].replace(/,/g, ""), 10) * 10000
    ).toLocaleString(),
    cost: parseInt(item["거래금액"].replace(/,/g, ""), 10) * 10000,
  }));
};

export const extractColumn = (data) => {
  const desiredOrder = [
    "건축년도",
    "전용면적",
    "아파트",
    "층",
    "거래금액",
    "지번",
    "등기일자",
  ];

  const CUSTOM_COLUMN = [
    {
      field: "date",
      headerName: "날짜",
      valueGetter: (param, row) => {
        return row["월"] + "/" + row["일"];
      },
      flex: 0.5,
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
      flex: 1,
    },
  ];

  const columns = Object.keys(data[0])
    .filter(
      (e) =>
        ![
          "월",
          "일",
          "동",
          "년",
          "법정동",
          "해제사유발생일",
          "해제여부",
          "거래유형",
          "매도자",
          "매수자",
          "중개사소재지",
          "지역코드",
          "등기일자",
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
      if (e === "거래금액") {
        return {
          field: e,
          headerName: e,
          flex: 1,
          valueGetter: (param, row) => {
            const data =
              parseInt(row["거래금액"].replace(/,/g, ""), 10) * 10000;
            return data.toLocaleString();
          },
        };
      }
      return { field: e, headerName: e, flex: 1 };
    });

  return [...CUSTOM_COLUMN, ...columns];
};
