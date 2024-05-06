import { useDispatch, useSelector } from "react-redux";
import { useEffect, useState } from "react";
import { Chip, Stack, Box } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { nanoid } from "@reduxjs/toolkit";
import dayjs from "dayjs";

import { getRealEstate } from "../features/dataSlice";
import { extractColumn } from "../common/utils";

const RealEstate = () => {
  const dispatch = useDispatch();
  const { realEstateData } = useSelector((state) => state.data);
  const [rows, setRows] = useState([]);
  const [columns, setColumns] = useState([]);
  const [selectedChip, setSelectedChip] = useState(null);

  const handleChipSelect = (e) => {
    const columnData = extractColumn(e.content);
    const rowData = e.content.map((item) => ({ ...item, id: nanoid() }));
    setRows(rowData);
    setColumns(columnData);
    setSelectedChip(e.path);
  };

  useEffect(() => {
    const latest = realEstateData[realEstateData.length - 1];
    if (realEstateData.length > 0) {
      handleChipSelect(latest);
    }
  }, [realEstateData]);

  useEffect(() => {
    dispatch(getRealEstate());
  }, [dispatch]);

  return (
    <Box sx={{ mt: 2 }}>
      <Box sx={{ my: 2 }}>
        <Stack direction="row" spacing={2}>
          {realEstateData.map((e, idx) => {
            const filePath = e.path.split("/")[2].replace(".json", "");
            const label = dayjs(filePath).format("YYYY-MM");
            return (
              <Chip
                key={idx}
                variant={e.path === selectedChip ? "" : "outlined"}
                label={label}
                onClick={() => handleChipSelect(e)}
                clickable
              />
            );
          })}
        </Stack>
      </Box>
      <DataGrid columns={columns} rows={rows} autoHeight />
    </Box>
  );
};

export default RealEstate;
