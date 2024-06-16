import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { Outlet } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { Box, Container, CssBaseline, Toolbar } from "@mui/material";

import SideBar from "../components/SideBar";
import Breadcrumb from "../components/Breadcrumb";
import Header from "../components/Header";
import { dataInitialize } from "../features/dataSlice";
import "../assets/css/global.css";

const Layout = () => {
  const dispatch = useDispatch();
  const [mode, setMode] = useState("dark");
  const [drawerToggle, setDrawerToggle] = useState(false);
  const darkTheme = createTheme({
    palette: {
      mode: mode,
    },
    typography: {
      fontFamily: "IBMPlexSansKR",
    },
    components: {
      MuiCssBaseline: {
        styleOverrides: {
          html: {
            fontFamily: "IBMPlexSansKR",
          },
          body: {
            fontFamily: "IBMPlexSansKR",
          },
        },
      },
    },
  });

  const modelToggle = () => {
    setMode(mode === "dark" ? "light" : "dark");
  };

  useEffect(() => {
    dispatch(dataInitialize());
  }, [dispatch]);

  return (
    <ThemeProvider theme={darkTheme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <Header handleMenuIcon={() => setDrawerToggle(true)} />
        <SideBar
          mode={mode}
          modeToggle={modelToggle}
          drawerToggle={drawerToggle}
          setDrawerToggle={setDrawerToggle}
        />
        <Container>
          <Toolbar
            sx={{
              display: { lg: "none", md: "none", sm: "block", xs: "block" },
            }}
          />
          <Breadcrumb />
          <Outlet />
        </Container>
      </Box>
    </ThemeProvider>
  );
};

export default Layout;
