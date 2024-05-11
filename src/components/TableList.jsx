import { useEffect, useState } from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import { styled } from "@mui/material";

import { isEmptyValue } from "../common/utils";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  "&:nth-of-type(odd)": {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  "&:last-child td, &:last-child th": {
    border: 0,
  },
}));

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
              <StyledTableRow key={row.id}>
                <>
                  <StyledTableCell key={row.id + "_" + idx} align="center">
                    {idx + 1}
                  </StyledTableCell>
                  {column.map((col) => (
                    <StyledTableCell key={row.id + "_" + col} align="center">
                      {row[col]}
                    </StyledTableCell>
                  ))}
                </>
              </StyledTableRow>
            ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default TableList;
