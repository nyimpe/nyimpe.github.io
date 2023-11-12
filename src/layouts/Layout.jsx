import { Outlet } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { Box, CssBaseline } from "@mui/material";

import Sidebar from "../components/Sidebar";
// import Breadcrum from "../components/Breadcrum";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

const Layout = () => {
  return (
    <ThemeProvider theme={darkTheme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <Sidebar />
        {/* <Breadcrum /> */}
        <Outlet />
      </Box>
    </ThemeProvider>
  );
};

export default Layout;
