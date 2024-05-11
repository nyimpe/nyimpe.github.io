import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { useEffect, useState } from "react";
import { isEmptyValue } from "../common/utils";

const TableList = ({ columns, rows }) => {
  const [column, setColumn] = useState([]);

  useEffect(() => {
    if (isEmptyValue(columns)) {
      return;
    }
    setColumn(columns.map((e) => e.headerName));
  }, [columns]);

  return (
    <TableContainer component={Paper} sx={{ maxHeight: "700px" }}>
      <Table stickyHeader size="small">
        <TableHead>
          <TableRow>
            <TableCell align="center">No</TableCell>
            {column?.map((e, idx) => (
              <TableCell key={idx} align="center">
                {e}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {column.length > 0 &&
            rows?.map((row, idx) => (
              <TableRow key={row.id}>
                <>
                  <TableCell key={row.id + "_" + idx} align="center">
                    {idx + 1}
                  </TableCell>
                  {column.map((col) => (
                    <TableCell key={row.id + "_" + col} align="center">
                      {row[col]}
                    </TableCell>
                  ))}
                </>
              </TableRow>
            ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default TableList;
