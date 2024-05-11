import { useDispatch, useSelector } from "react-redux";
import { useEffect, useState } from "react";
import { Chip, Stack, Box } from "@mui/material";
import dayjs from "dayjs";

import { getRealEstate } from "../features/dataSlice";
import { extractColumn, getRowData } from "../common/utils";
import TableList from "../components/TableList";

const RealEstate = () => {
  const dispatch = useDispatch();
  const { realEstateData } = useSelector((state) => state.data);
  const [rows, setRows] = useState([]);
  const [columns, setColumns] = useState([]);
  const [selectedChip, setSelectedChip] = useState(null);

  const handleChipSelect = (e) => {
    const columnData = extractColumn(e.content);
    const rowData = getRowData(e.content);
    rowData.sort((a, b) => {
      return a.cost - b.cost;
    });

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
      <TableList columns={columns} rows={rows} />
    </Box>
  );
};

export default RealEstate;
