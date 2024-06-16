import Box from "@mui/material/Box";
import { DataGrid } from "@mui/x-data-grid";

const Grid = ({ columns, rows }) => {
  return (
    <Box sx={{ height: 600, width: "100%" }}>
      <DataGrid
        rows={rows}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: {
              pageSize: 100,
            },
          },
        }}
        pageSizeOptions={[1000]}
        checkboxSelection
        disableRowSelectionOnClick
      />
    </Box>
  );
};

export default Grid;
